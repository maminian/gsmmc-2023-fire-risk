import numpy as np
import urllib.request
import json
import pickle
import geopandas
import pandas as pd
from sklearn.neighbors import KNeighborsRegressor

savefile = "co_data.pickle"  # CHANGE to save data to a different file
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

# obtain precipitation data
params = {
    "state":["CO"],
    "sdate":"20200101", # low-tech YYYYMMDD
    "edate":"20201231",
    "grid":1,
    "output":"json",
    "elems":[{"name":"pcpn","smry":"sum","smry_only":1}],  # annual summed precipitation
    "meta":["ll"]
}
precip_data = GridData(params, server="GridData")

#Obtain temperature and elevation data
params = {
    "state":["CO"],
    "sdate":"20200101", # low-tech YYYYMMDD
    "edate":"20201231",
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
gdf = geopandas.read_file('Western_Wind_Dataset')
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

############################## Organize and Save All Data into Pickle File #########################################

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
