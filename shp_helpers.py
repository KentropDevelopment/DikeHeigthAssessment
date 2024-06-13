import geopandas as gpd
import json

from viktor.geometry import RDWGSConverter


def shp_to_geojson(shp_path):
    """
    Convert a shapefile to GeoJSON format.

    Parameters:
    shp_path (str): The path to the input shapefile (.shp).
    geojson_path (str): The path to the output GeoJSON file.
    """
    # Read the shapefile using GeoPandas
    gdf = gpd.read_file(shp_path)
    
    # Convert the GeoDataFrame to GeoJSON format
    geojson_str = gdf.to_json()
    geojson = json.loads(geojson_str)

    for feature in geojson['features']:
        new_coord = []
        for coord in feature['geometry']['coordinates']:
            x = coord[0]
            y = coord[1]
            lat, lon = RDWGSConverter.from_rd_to_wgs((x, y))
            new_coord.append((lat, lon))
        feature['geometry']['coordinates'] = new_coord

    return geojson

