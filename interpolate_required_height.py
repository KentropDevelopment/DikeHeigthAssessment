import shapely
import geopandas as gpd
from geopandas import GeoDataFrame
from shapely.geometry.geo import shape
from shapely.geometry import LineString
from shapely.geometry import Point, MultiPoint
from viktor.geometry import RDWGSConverter

from shp_helpers import shp_to_geojson

import matplotlib.pyplot as plt

PATH_REQUIRED_HEIGHT_POINTS = r"sample_data\required_height\required_height.shp"
PATH_DIKE_TRAJECTORY = r"sample_data\dike_trajectories\dike_trajectory_sample.shp"


def process_required_height_points(
        path_points: str = PATH_REQUIRED_HEIGHT_POINTS,
        path_dike_trajectory: str = PATH_DIKE_TRAJECTORY
):
    """Function is fit for a single line. Multilines are not possible"""
    # initiate empty lists
    x = []
    y = []
    z = []
    l = []

    # Process shape files
    required_height_points_geo_json = shp_to_geojson(path_points)
    dike_trajectory_geo_json = shp_to_geojson(path_dike_trajectory)

    # Translate coordiantes back to RD
    new_coords = []

    for coord in dike_trajectory_geo_json['features'][0]['geometry']['coordinates']:
        x_coord = coord[0]
        y_coord = coord[1]
        lat, lon = RDWGSConverter.from_wgs_to_rd((y_coord, x_coord))
        new_coords.append((lat, lon))
    dike_trajectory_geo_json['features'][0]['geometry']['coordinates'] = new_coords

    dike_trajectory_line_string = LineString(dike_trajectory_geo_json["features"][0]["geometry"]["coordinates"])
    print(dike_trajectory_line_string)

    # Loop to fill the lists
    for point_geo_json in required_height_points_geo_json["features"]:
        coord = point_geo_json['geometry']['coordinates']
        x_coord = coord[0]
        y_coord = coord[1]
        x_new, y_new = RDWGSConverter.from_wgs_to_rd((y_coord, x_coord))

        point_geo_json['geometry']['coordinates'] = [x_new, y_new]

        point = Point(point_geo_json["geometry"]["coordinates"])

        x.append(point.x)
        y.append(point.y)
        z.append(point_geo_json["properties"]["h_req"])

        l.append(dike_trajectory_line_string.project(point))

    return x, y, z, l

