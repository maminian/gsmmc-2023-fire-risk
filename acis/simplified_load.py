
import acis_example as loader
import copy

# see 
# https://www.rcc-acis.org/docs_webservices.html 
# (section IV onwards) for parameter values.

params = {
    "state":["CO"],
    "sdate":"20191224", # low-tech YYYYMMDD
    "edate":"20231231",
    "grid":1,
    "output":"json",
    "elems":[{"name":"pcpn","smry":"sum"}],
    "meta":["ll", "elev"]
}
#Obtain data
data = loader.GridData(params, datatype="GridData2")

##########################

#params_info = copy.copy(params)
#params_info['info_only'] = "1"
#Obtain data
#data_info = loader.GridData(params_info)
