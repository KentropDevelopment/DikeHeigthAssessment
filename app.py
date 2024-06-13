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
    GeoJSONView
)


import shp_helpers as shphelp

class Parametrization(ViktorParametrization):
    step_1 = Step("Trajectory and Height", description="Input the trajectory and height of the dike", views=["get_map_view_1"])

    step_1.section_1 = Section("Import Dike shp")
    step_1.section_1.file_field_1 = FileField("Shapefile of Dike", flex=50)
    step_1.section_1.number_field_1 = NumberField("Crest Height", flex=50)
    
    step_1.section_2 = Section("Calculate Dike Height")
    step_1.section_2.dynamic_array_1 = DynamicArray("Interpolation Points", description="Modify the interpolation points")
    step_1.section_2.dynamic_array_1.geo_point_field_1 = GeoPointField("Interpolation Point")
    step_1.section_2.dynamic_array_1.number_field_1 = NumberField("Dike height", flex=50, description="Crest height of the dike")

    
    step_2 = Step("Asses Design", description="Compare the design to the existing dike", views=["get_map_view_2"])
    step_2.tab_1 = Tab("Asses")
    step_2.tab_1.section_1 = Section("Get Height Data")
    step_2.tab_1.section_1.option_field_1 = OptionField("Show Features", options=["Designed Dike", "Real Height", "Error"])
    step_2.tab_1.section_1.analyse_button_1 = AnalyseButton("Get height data", method="analyse_button_method_1", longpoll=False)
    
    
    step_3 = Step("Report", description="Create a report of the different scenario's")
    step_3.text_field_1 = TextField("Tba")


class Controller(ViktorController):
    label = "My Entity Type"
    parametrization = Parametrization

    def analyse_button_method_1(self, params, **kwargs):
        return

    @GeoJSONView('Plane View', duration_guess=1)
    def get_map_view_1(self, params, **kwargs):

        dike_line = shphelp.shp_to_geojson('sample_data/dike_trajectories/dike_trajectory_sample.shp')
        dike_points = shphelp.shp_to_geojson('sample_data/required_dike_height_points/points_sampled.shp')
        

        geojson = shphelp.merge_geojson([dike_line, dike_points])

        return GeoJSONResult(geojson)
    
    @MapView('Dike Assesment', duration_guess=1)
    def get_map_view_2(self, params, **kwargs):
        return MapResult(features=[])
    

