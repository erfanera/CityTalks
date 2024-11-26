
import osmnx as ox
import geopandas as gpd

def fetch_amenities(city, amenities, crs_epsg=25831):
    tags = {'amenity': amenities}
    amenities_gdf = ox.geometries_from_place(city, tags)
    amenities_gdf = amenities_gdf.to_crs(epsg=crs_epsg)
    return amenities_gdf

def fetch_boundary(city, crs_epsg=25831):
    boundary_gdf = ox.geocode_to_gdf(city)
    boundary_gdf = boundary_gdf.to_crs(epsg=crs_epsg)
    return boundary_gdf
