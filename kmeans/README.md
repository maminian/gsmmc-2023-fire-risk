### To Run
1. Run `clean_data.py`  to produce a pickle file with all the data.
2. Run `kmeans.ipynb` to apply k-means to the temperature, elevation, wind, and precipitation data.

### Data
By default, all the data is run within Colorado. The pickle file will contain a dictionary with keys as follows:
* `temp`
* `elev`
* `precip`
* `cf`
* `lat`
* `lon`
* `all_data`
Besides `all_data`, these keys map to 99x171(for Colorado) numpy arrays containing the temperature/elevation/precipitation/capacity factor/latitude/longitude at the point (longitude,latitude) in the array.
Then, `all_data` is a numpy array of size 99*171 x 6, reformatted to be used for the k-means in scikit-learn. It flattens the previous information organized by latitude and longitude, and contains a list of size 16929, where each list element is a 6-tuple in the form (latitude,longitude,elevation,precipitation,temperature,capacity factor). Furthermore, the elements in `all_data` are normalized so that the maximum temperature/elevation/precipitation/capacity factor is 1.