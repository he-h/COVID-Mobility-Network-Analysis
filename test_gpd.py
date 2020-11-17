import geopandas as gpd
import json


def get_xy(pt):
    return [pt.x, pt.y]


gdf = gpd.read_file('shape_file/cb_2018_us_cbsa_500k/cb_2018_us_cbsa_500k.shp')
gdf['GEOID'] = gdf['GEOID'].astype(str)
centroids = gdf['geometry'].centroid
lons, lats = [list(t) for t in zip(*map(get_xy, centroids))]
gdf['longitude'] = lons
gdf['latitude'] = lats
gdf.to_crs({"init": "epsg:4326"}).plot(color="white", edgecolor="grey", linewidth=0.5, alpha=0.75) #ax=ax
mx, my = gdf['longitude'].values, gdf['latitude'].values

pos = dict()
for i, elem in enumerate(gdf['GEOID']):
    pos[elem] = mx[i], my[i]

with open("data/pos.json", "w") as outfile:
    json.dump(pos, outfile)

