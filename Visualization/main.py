
import matplotlib.pyplot as plt
from itertools import cycle
from data_fetcher import fetch_amenities, fetch_boundary
from kde_processor import compute_kde
from plotter import plot_density, configure_plot
from utils import create_colormap

def main():
    city = "Barcelona, Spain"
    amenities = ["bank"]
    colormap = create_colormap()
    point_colors = cycle(['white'])

    amenities_gdf = fetch_amenities(city, amenities)
    boundary_gdf = fetch_boundary(city)
    barcelona_polygon = boundary_gdf.iloc[0].geometry
    bounds = barcelona_polygon.bounds

    fig, ax = plt.subplots(figsize=(10, 8), facecolor='black')

    for amenity, point_color in zip(amenities, point_colors):
        amenity_gdf = amenities_gdf[amenities_gdf['amenity'] == amenity]

        x_coords = [geom.x for geom in amenity_gdf.geometry if geom.geom_type == 'Point']
        y_coords = [geom.y for geom in amenity_gdf.geometry if geom.geom_type == 'Point']

        if len(x_coords) > 0:
            x_grid, y_grid, z = compute_kde(x_coords, y_coords, bounds=bounds)
            plot_density(ax, boundary_gdf, x_coords, y_coords, point_color, f"{amenity.capitalize()} Locations", x_grid, y_grid, z, bounds, colormap)
            

            #plot_amenities(ax, x_coords, y_coords, point_color, f"{amenity.capitalize()} Locations")
       # ax.scatter(x_coords, y_coords, s=10, color=point_color, label=f"{amenity.capitalize()} Locations" )
    
    configure_plot(ax, "Amenity Density Heatmap within Barcelona Boundary", "Easting (meters)", "Northing (meters)")

    #plt.colorbar(ax.images[0], ax=ax, fraction=0.036, pad=0.04)
    plt.show()

if __name__ == "__main__":
    main()
