import numpy as np
import urllib.request
import json
import pickle
import geopandas
import pandas as pd
from sklearn.neighbors import KNeighborsRegressor

base_url = "http://data.rcc-acis.org/"

############################# Web Scraping ##########################################

# Acis WebServices functions
def make_request(url,params) :
    data = json.dumps(params)
    data_bytes = bytes(data, 'utf-8') # one weird trick
    
    req = urllib.request.Request(url,
    data=data_bytes,
    headers={"Content-Type":"application/json"})
    try:
        response = urllib.request.urlopen(req)
        return json.loads(response.read())
    except urllib.request.HTTPError as error:
        if error.code == 400 : print(error.msg)
    print(urllib.request.HTTPError)

def GridData(params, server="GridData"):
    return make_request(base_url+server, params)

############################## Scrape Precipitation, Temperature, Elevation Data #########################################

def scrape_data(state,sdate="20200101",edate="20201231"):
# obtain precipitation data
    params = {
        "state":[state],
        "sdate":sdate, # low-tech YYYYMMDD
        "edate":edate,
        "grid":1,
        "output":"json",
        "elems":[{"name":"pcpn","smry":"sum","smry_only":1}],  # annual summed precipitation
        "meta":["ll"]
    }
    precip_data = GridData(params, server="GridData")

    #Obtain temperature and elevation data
    params = {
        "state":[state],
        "sdate":sdate, # low-tech YYYYMMDD
        "edate":edate,
        "grid":1,
        "output":"json",
        "elems":[{"name":"maxt","smry":"max","smry_only":1}],  # annual max temp
        "meta":["ll", "elev"]
    }
    temp_elev_data = GridData(params, server="GridData")

    # stack the precipitation, elevation, and temperature data with lat/lon
    precip = np.array(precip_data['smry'][0])
    shapex,shapey = precip.shape
    elev = np.array(temp_elev_data['meta']['elev'])
    lat, lon = np.array(temp_elev_data['meta']['lat']), np.array(temp_elev_data['meta']['lon'])
    temp = np.array(temp_elev_data['smry'][0])
    # Note: the lat and lon coordinates line up, so we only need to extract them from one of the jsons.
    all_data = np.reshape(np.dstack((lat,lon,elev,precip,temp)),(shapex*shapey,5))

############################## Process Wind Data #########################################

    # read in wind data
    gdf = geopandas.read_file('data/Western_Wind_Dataset')
    gdf["lon"] = gdf['geometry'].x
    gdf["lat"] = gdf['geometry'].y
    gdf = pd.DataFrame(gdf.drop(columns=['geometry']))
    df = pd.DataFrame(all_data,columns=["lat","lon","elev","precip","temp"])

    # interpolate wind data
    ll = np.dstack((gdf[['lat']],gdf[['lon']]))[:,0]
    nbrs = KNeighborsRegressor(n_neighbors=5).fit(ll,gdf[['CAPACITY F']])
    ll2 = np.dstack((df[['lat']],df[['lon']]))[:,0]
    df["cf"] = nbrs.predict(ll2)
    cf = np.array(df["cf"]).reshape((shapex,shapey))

    return shapex,shapey,precip,temp,elev,lat,lon,cf,all_data

############################## Organize and Save All Data into Pickle File #########################################

def pickle_dump(data,savefile):
    shapex,shapey,precip,temp,elev,lat,lon,cf,all_data = data
    # normalize entries for precip, elev, temp for kmeans
    precip_n = precip / np.amax(precip)
    elev_n = elev / np.amax(elev)
    temp_n = temp / np.amax(temp)
    cf_n = cf / np.amax(cf)
    all_data = np.reshape(np.dstack((lat,lon,elev_n,precip_n,temp_n,cf_n)),(shapex*shapey,6))

    # save all data as dictionary in a pickle file
    d = {"precip":precip,
        "temp":temp,
        "elev":elev,
        "lat":lat,
        "lon":lon,
        "cf":cf,
        "all_data":all_data
        }
    with open(savefile, 'wb') as handle:
        pickle.dump(d, handle, protocol=pickle.HIGHEST_PROTOCOL)
    return

def save_data(state):
    '''
    Main wrapper function to save to pickle file
    Input: state - all caps 2 letter abbreviation (ex. CO)
    Output: None - saves a pickle file (ex. data/co_data.pickle)
    '''
    savefile = "data/" + state.lower() + ".pickle"
    data = scrape_data(state)  # default sdate, edate: the entire year of 2020
    pickle_dump(data,savefile)
    return
