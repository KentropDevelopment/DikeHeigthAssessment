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
    list_of_tuples = []
    for feature in geojson['features']:
        new_coord = []

        if type(feature['geometry']['coordinates'][0]) == type([]):

            for coord in feature['geometry']['coordinates']:
                x = coord[0]
                y = coord[1]
                lat, lon = RDWGSConverter.from_rd_to_wgs((x, y))
                new_coord.append((lon, lat))
                list_of_tuples.append((x, y))
            feature['geometry']['coordinates'] = new_coord
        else:
            coord = feature['geometry']['coordinates']
            x = coord[0]
            y = coord[1]
            lat, lon = RDWGSConverter.from_rd_to_wgs((x, y))
            list_of_tuples.append((x, y))
            feature['geometry']['coordinates'] = [lon, lat]

    return geojson, list_of_tuples

# def shp_to_geojson(shp_path):
#     """
#     Convert a shapefile to GeoJSON format.
#     Parameters:
#     shp_path (str): The path to the input shapefile (.shp).
#     geojson_path (str): The path to the output GeoJSON file.
#     """
#     # Read the shapefile using GeoPandas
#     gdf = gpd.read_file(shp_path)
#     # Convert the GeoDataFrame to GeoJSON format
#     geojson_str = gdf.to_json()
#     geojson = json.loads(geojson_str)
#     list_of_tuples = []
#     for feature in geojson["features"]:
#         new_coord = []
#         for coord in feature["geometry"]["coordinates"]:
#             x = coord[0]
#             y = coord[1]
#             lon, lat = RDWGSConverter.from_rd_to_wgs((x, y))
#             new_coord.append((lat, lon))
#             list_of_tuples.append((x, y))
#         feature["geometry"]["coordinates"] = new_coord
#     return geojson, list_of_tuples


def shp_to_geojson_offset(shp_path, x_offset, y_offset):
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

        if type(feature['geometry']['coordinates'][0]) == type([]):

            for coord in feature['geometry']['coordinates']:
                x = coord[0] + x_offset
                y = coord[1] + y_offset
                lat, lon = RDWGSConverter.from_rd_to_wgs((x, y))
                new_coord.append((lon, lat))
            feature['geometry']['coordinates'] = new_coord
        else:
            coord = feature['geometry']['coordinates']
            x = coord[0] + x_offset
            y = coord[1] + y_offset
            lat, lon = RDWGSConverter.from_rd_to_wgs((x, y))
            feature['geometry']['coordinates'] = [lon, lat]

    return geojson

def merge_geojson(geojson_list):
    """
    Merge a list of GeoJSON objects into one GeoJSON object.

    Parameters:
    geojson_list (list): A list of GeoJSON objects (dictionaries).

    Returns:
    dict: A single merged GeoJSON object.
    """
    if not geojson_list:
        return {"type": "FeatureCollection", "features": []}

    merged_geojson = {"type": "FeatureCollection", "features": []}

    for geojson in geojson_list:
        if 'features' in geojson:
            merged_geojson["features"].extend(geojson["features"])
        else:
            if geojson["type"] == "Feature":
                merged_geojson["features"].append(geojson)
            else:
                raise ValueError("Invalid GeoJSON object: must be a Feature or contain a FeatureCollection")

    return merged_geojson

# check = shp_to_geojson('sample_data/required_dike_height_points/points_sampled.shp')

# print(check)
