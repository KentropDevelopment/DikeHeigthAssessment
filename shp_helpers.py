import geopandas as gpd
import json
from shapely.geometry import LineString, Polygon
from shapely.geometry.geo import mapping, shape, MultiPolygon
from shapely import affinity


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

        if type(feature['geometry']['coordinates'][0]) == type([]):

            for coord in feature['geometry']['coordinates']:
                x = coord[0]
                y = coord[1]
                lat, lon = RDWGSConverter.from_rd_to_wgs((x, y))
                new_coord.append((lon, lat))
            feature['geometry']['coordinates'] = new_coord
        else:
            coord = feature['geometry']['coordinates']
            x = coord[0]
            y = coord[1]
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


def linestring_to_polygon(geojson_linestring, dike_width):
    """
    Converts a GeoJSON LineString to a Polygon representing a road with a given width.

    Parameters:
    geojson_linestring (dict): A GeoJSON LineString object.
    road_width (float): The width of the road.

    Returns:
    dict: A GeoJSON Polygon object representing the road.
    """
    # print(geojson_linestring['type'])
    linestring = shape(geojson_linestring['features'][0]['geometry'])

    # Create a buffer around the linestring
    buffered_polygon = linestring.buffer(dike_width / 2, cap_style=2, join_style=2)
    polygon_geojson = mapping(buffered_polygon)
    print(polygon_geojson)

    # Create a GeoJSON Feature
    geojson = {
        "type": "Feature",
        "geometry": polygon_geojson,
        "properties": geojson_linestring.get('properties', {})
    }

    return geojson



# points = shp_to_geojson('sample_data/required_dike_height_points/points_sampled.shp')
# line = shp_to_geojson('sample_data/dike_trajectories/dike_trajectory_sample.shp')
# b = 10
# print(check)