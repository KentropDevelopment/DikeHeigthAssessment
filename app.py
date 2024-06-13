# Welcome to VIKTOR!
#
# First time using VIKTOR?
#   Keep this window open while we are activating your account.
#
#   You will see the following message in the window below when your Codespace has finished loading:
#  
#       The system check has been completed with the following conclusion:
#
#       V Your system is ready to use VIKTOR with isolation mode 'venv'
#
#   After that return to your VIKTOR environment where you will learn how to create your first app!
#   Keep this Codespace open as this is the place where you will write your code.

from viktor.parametrization import (
    ViktorParametrization,
    GeoPointField,
    NumberField,
    DynamicArray,
    Section,
    FileField,
    Step,
    OptionField,
    AnalyseButton,
    Tab,
    TextField,
)

from viktor import ViktorController
from viktor.views import (
    MapView,
    MapResult,
    GeoJSONResult,
    GeoJSONView, PlotlyView, PlotlyResult
)

import json
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import plotly.graph_objs as go
import rasterio
import rasterio.plot
from viktor.geometry import RDWGSConverter

import shp_helpers as shphelp


class Parametrization(ViktorParametrization):
    step_1 = Step("Trajectory and Height", description="Input the trajectory and height of the dike",
                  views=["get_map_view_1", "get_plotly_view"])

    step_1.section_1 = Section("Import Dike shp")
    step_1.section_1.file_field_1 = FileField("Shapefile of Dike", flex=50)
    step_1.section_1.number_field_1 = NumberField("Crest Height", flex=50, default=10)
    
    step_1.section_1.number_field_1 = NumberField("Crest Height", flex=50)

    step_1.section_2 = Section("Calculate Dike Height")
    step_1.section_2.dynamic_array_1 = DynamicArray("Interpolation Points",
                                                    description="Modify the interpolation points")
    step_1.section_2.dynamic_array_1.geo_point_field_1 = GeoPointField("Interpolation Point")
    step_1.section_2.dynamic_array_1.number_field_1 = NumberField("Dike height", flex=50,
                                                                  description="Crest height of the dike")

    step_2 = Step("Asses Design", description="Compare the design to the existing dike", views=["get_map_view_2"])
    step_2.tab_1 = Tab("Asses")
    step_2.tab_1.section_1 = Section("Get Height Data")
    step_2.tab_1.section_1.option_field_1 = OptionField("Show Features",
                                                        options=["Designed Dike", "Real Height", "Error"])
    step_2.tab_1.section_1.analyse_button_1 = AnalyseButton("Get height data", method="analyse_button_method_1",
                                                            longpoll=False)

    step_3 = Step("Report", description="Create a report of the different scenario's")
    step_3.text_field_1 = TextField("Tba")


class Controller(ViktorController):
    label = "My Entity Type"
    parametrization = Parametrization

    def analyse_button_method_1(self, params, **kwargs):
        return

    @GeoJSONView('Plane View', duration_guess=1)
    def get_map_view_1(self, params, **kwargs):

        geojson, list_of_tuples = shphelp.shp_to_geojson("sample_data/dike_trajectories/dike_trajectory_sample.shp")
        data_name = "sample_data/sample_ahn/sample_ahn.tif"
        with rasterio.open(data_name) as f:
            arr = f.read(1)
            height, width = f.height, f.width
            xmin = f.xy(0, 0)[0]
            ymax = f.xy(0, 0)[1]
        shapeline_lon = []
        shapeline_lat = []
        shapeline_z = []
        x_coords, y_coords = zip(*list_of_tuples)
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

        print(shapeline_lon)
        print(shapeline_lat)
        print(shapeline_z)

        dike_line = shphelp.shp_to_geojson('sample_data/dike_trajectories/dike_trajectory_sample.shp')[0]
        dike_points = shphelp.shp_to_geojson('sample_data/required_dike_height_points/points_sampled.shp')[0]
        print(json.dumps(dike_points, sort_keys=True, indent=4))
        # print(len(dike_line["features"][0]["geometry"]["coordinates"]))
        print(len(dike_points["features"]))

        dike_lon = []
        dike_lat = []
        dike_z = []
        for p in dike_points["features"]:
            x_point = p["geometry"]["coordinates"][0]
            y_point = p["geometry"]["coordinates"][1]
            z_point = p["properties"]["z1"]
            dike_lon.append(x_point)
            dike_lat.append(y_point)
            dike_z.append(z_point)



        dike_line_offset = shphelp.shp_to_geojson_offset('sample_data/dike_trajectories/dike_trajectory_sample.shp', 0,
                                                         100)
        # print(len(dike_line_offset["features"][0]["geometry"]["coordinates"]))

        l1_p1 = list(dike_line["features"][0]["geometry"]["coordinates"][0])
        l1_p2 = list(dike_line["features"][0]["geometry"]["coordinates"][1])
        l2_p1 = list(dike_line_offset["features"][0]["geometry"]["coordinates"][0])
        l2_p2 = list(dike_line_offset["features"][0]["geometry"]["coordinates"][1])
        coordinates = [
            l1_p1,
            l1_p2,
            l2_p2,
            l2_p1,
            l1_p1
        ]
        # print(coordinates)

        geojson_example = {
            "type": "FeatureCollection",
            "features": [
                {"type": "Feature",
                 "geometry": {
                     "type": "Polygon",
                     "coordinates":
                         [
                             coordinates
                         ]
                 },
                 "properties": {
                     "description": "Area",
                     "fill": "#FF0000"
                 }
                 }
            ]
        }

        geojson_shapeline = {"type": "FeatureCollection",
                             "features": [
                                 {"type": "Feature",
                                  "geometry": {"type": "Point", "coordinates": [
                                      5.80462559682704,
                                      51.92103553990242
                                  ]},
                                  "properties": {"prop0": "value0"}
                                  },
                                 {"type": "Feature",
                                  "geometry": {"type": "Point", "coordinates": [
                                      6.80462559682704,
                                      51.92103553990242
                                  ]},
                                  "properties": {"prop0": "value0"}
                                  },
                             ]
                             }

        geojson = shphelp.merge_geojson([dike_line, dike_points, dike_line_offset, geojson_example, geojson_shapeline])
        dike_line = shphelp.shp_to_geojson('sample_data/dike_trajectories/dike_trajectory_sample.shp')
        dike_points = shphelp.shp_to_geojson('sample_data/required_dike_height_points/points_sampled.shp')
        # print(dike_line)
        dike_poly = shphelp.linestring_to_polygon(dike_line, params.step_1.section_1.number_field_1)
        dike_poly = json.loads(dike_poly)
        geojson = shphelp.merge_geojson([dike_line, dike_points, dike_poly])

        return GeoJSONResult(geojson)

    @MapView('Dike Assesment', duration_guess=1)
    def get_map_view_2(self, params, **kwargs):
        return MapResult(features=[])

    @PlotlyView("Plotly view", duration_guess=1)
    def get_plotly_view(self, params, **kwargs):

        dike_points = shphelp.shp_to_geojson('sample_data/required_dike_height_points/points_sampled.shp')[0]

        dike_lon = []
        dike_lat = []
        dike_z = []
        for p in dike_points["features"]:
            x_point = p["geometry"]["coordinates"][0]
            y_point = p["geometry"]["coordinates"][1]
            z_point = p["properties"]["z1"]
            dike_lon.append(x_point)
            dike_lat.append(y_point)
            dike_z.append(z_point)

        fig = go.Figure(
            data=[go.Scatter(x=dike_lon, y=dike_z)],
            layout=go.Layout(title=go.layout.Title(text="A Figure Specified By A Graph Object"))
        )
        return PlotlyResult(fig.to_json())
