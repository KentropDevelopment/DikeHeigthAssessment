import shapely
import geopandas as gpd
from geopandas import GeoDataFrame
from shapely.geometry.geo import shape
from shapely.geometry import LineString
from shapely.geometry import Point, MultiPoint
from viktor.geometry import RDWGSConverter
import rasterio

import shp_helpers as shphelp
from shp_helpers import shp_to_geojson

import matplotlib.pyplot as plt

PATH_REQUIRED_HEIGHT_POINTS = r"sample_data\required_height\required_height.shp"
PATH_DIKE_TRAJECTORY = r"sample_data\dike_trajectories\dike_trajectory_sample.shp"


def get_length_coordinate_of_points(x, y, path_to_line: str = PATH_DIKE_TRAJECTORY):
    dike_trajectory_geo_json, _ = shp_to_geojson(path_to_line)

    # Translate coordiantes back to RD
    new_coords = []

    for coord in dike_trajectory_geo_json['features'][0]['geometry']['coordinates']:
        x_coord = coord[0]
        y_coord = coord[1]
        lat, lon = RDWGSConverter.from_wgs_to_rd((y_coord, x_coord))
        new_coords.append((lat, lon))
    dike_trajectory_geo_json['features'][0]['geometry']['coordinates'] = new_coords

    dike_trajectory_line_string = LineString(dike_trajectory_geo_json["features"][0]["geometry"]["coordinates"])

    l = []
    # hier!
    for x_i, y_i in zip(x, y):
        point = Point(x_i, y_i)
        l_i = dike_trajectory_line_string.project(point)
        l.append(dike_trajectory_line_string.project(point))

    return l


def process_current_height():
    geojson, list_of_tuples = shphelp.shp_to_geojson("sample_data/dike_trajectories/dike_trajectory_sample.shp")
    data_name = "sample_data/sample_ahn/sample_ahn.tif"
    with rasterio.open(data_name) as f:
        arr = f.read(1)
        # height, width = f.height, f.width
        xmin = f.xy(0, 0)[0]
        ymax = f.xy(0, 0)[1]
    shapeline_lon = []
    shapeline_lat = []
    shapeline_z = []
    # x_coords, y_coords = zip(*list_of_tuples)

    for xcoord, ycoord in list_of_tuples:
        try:
            index_x = int((xcoord - xmin) / 0.5)
            index_y = int((ymax - ycoord) / 0.5)
            if arr[index_y][index_x] > 10:
                pass
            else:
                lon, lat = RDWGSConverter.from_rd_to_wgs((xcoord, ycoord))
                shapeline_lon.append(lon)
                shapeline_lat.append(lat)
                shapeline_z.append((arr[index_y][index_x]))
        except:
            pass

    return shapeline_lon, shapeline_lat, shapeline_z


def get_current_height_in_rd():
    x, y, z = process_current_height()
    x_new = []
    y_new = []
    z_new = []

    for i in range(len(x)):
        # TODO: somehow some values for lon and lat are very large and cause problems
        if x[i] > 1000:
            continue
        x_new_i, y_new_i = RDWGSConverter.from_wgs_to_rd((x[i], y[i]))
        x_new.append(x_new_i)
        y_new.append(y_new_i)
        z_new.append(z[i])

    l = get_length_coordinate_of_points(x_new, y_new)
    plt.plot(l, z_new)
    plt.show()

    return x_new, y_new, z_new, l


def get_required_height_points(
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
    required_height_points_geo_json, _ = shp_to_geojson(path_points)
    dike_trajectory_geo_json, _ = shp_to_geojson(path_dike_trajectory)

    # Translate coordiantes back to RD
    new_coords = []

    for coord in dike_trajectory_geo_json['features'][0]['geometry']['coordinates']:
        x_coord = coord[0]
        y_coord = coord[1]
        lat, lon = RDWGSConverter.from_wgs_to_rd((y_coord, x_coord))
        new_coords.append((lat, lon))
    dike_trajectory_geo_json['features'][0]['geometry']['coordinates'] = new_coords

    dike_trajectory_line_string = LineString(dike_trajectory_geo_json["features"][0]["geometry"]["coordinates"])

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

