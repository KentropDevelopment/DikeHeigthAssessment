import geopandas as gpd

def shp_to_geojson(shp_path, geojson_path):
    """
    Convert a shapefile to GeoJSON format.

    Parameters:
    shp_path (str): The path to the input shapefile (.shp).
    geojson_path (str): The path to the output GeoJSON file.
    """
    # Read the shapefile using GeoPandas
    gdf = gpd.read_file(shp_path)
    
    # Convert the GeoDataFrame to GeoJSON format
    geojson = gdf.to_json()

    return geojson


chek = shp_to_geojson()