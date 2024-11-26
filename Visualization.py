import osmnx as ox
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.neighbors import KernelDensity
from shapely.geometry import Polygon
import osmnx as ox
from shapely.geometry import Point
from itertools import cycle
import matplotlib.patches as mpatches

amenities = ['bank']  # Add more amenities here as needed
colors = ['hot']  # Cycle through color maps for heatmaps
point_colors = cycle(['blue'])

from matplotlib.colors import LinearSegmentedColormap
colors = [(1, 0.75, 0.8, 0),   # Fully transparent pink (RGBA)
          (1, 0.0, 0.0, 1)]   # Fully opaque pink (RGBA)
custom_cmap = LinearSegmentedColormap.from_list("TransparentPink", colors)

# Step 1: Configure OSMnx
#os.environ["USE_CACHE"] = "true"  # Enable caching


# Step 2: Get bank locations in Barcelona
tags = {'amenity':amenities }
amenities_gdf = ox.geometries_from_place('Barcelona, Spain', tags)

# Step 3: Get the boundary outline of Barcelona
boundary_gdf = ox.geocode_to_gdf('Barcelona, Spain')

# Project both to UTM Zone 31N for metric accuracy in spatial analysis
amenities_gdf = amenities_gdf.to_crs(epsg=25831)
boundary_gdf = boundary_gdf.to_crs(epsg=25831)

# Extract the polygon boundary of Barcelona
barcelona_polygon = boundary_gdf.iloc[0].geometry


# Step 4: Extract coordinates for KDE within Barcelona
for amenity, color_map, point_color in zip(amenities, colors, point_colors):
    # Filter data for the current amenity
    amenity_gdf = amenities_gdf[amenities_gdf['amenity'] == amenity]

    # Extract coordinates for KDE within Barcelona
    x_coords = np.array([geom.x for geom in amenity_gdf.geometry if geom.geom_type == 'Point'])
    y_coords = np.array([geom.y for geom in amenity_gdf.geometry if geom.geom_type == 'Point'])

    # Perform KDE and normalize z values
xy = np.vstack([x_coords, y_coords]).T
kde = KernelDensity(bandwidth=200, metric='euclidean').fit(xy)

# Generate grid for heatmap over the entire Barcelona area
x_min, y_min, x_max, y_max = barcelona_polygon.bounds
x_grid, y_grid = np.meshgrid(np.linspace(x_min, x_max, 200), np.linspace(y_min, y_max, 200))
xy_sample = np.vstack([x_grid.ravel(), y_grid.ravel()]).T

# Estimate density values on the grid and reshape
z = np.exp(kde.score_samples(xy_sample))
z = z.reshape(x_grid.shape)

# Normalize z values to the range [0, 1] for better color scaling
#z = (z - z.min()) / (z.max() - z.min())

fig, ax = plt.subplots(figsize=(10, 8), facecolor='black')
ax.set_facecolor('black')

# Set up the figure with a black background
for amenity, cmap, point_color in zip(amenities, colors, point_colors):
    # Filter data for the current amenity
    amenity_gdf = amenities_gdf[amenities_gdf['amenity'] == amenity]

    # Extract coordinates for KDE within Barcelona
    x_coords = np.array([geom.x for geom in amenity_gdf.geometry if geom.geom_type == 'Point'])
    y_coords = np.array([geom.y for geom in amenity_gdf.geometry if geom.geom_type == 'Point'])

    # Only proceed if there are points for this amenity
    if len(x_coords) > 0:
        # Prepare data for Kernel Density Estimation (KDE)
        xy = np.vstack([x_coords, y_coords]).T
        kde = KernelDensity(bandwidth=200, metric='euclidean').fit(xy)

        # Estimate density values on the grid and reshape (without normalization)
        z = np.exp(kde.score_samples(xy_sample))
        z = z.reshape(x_grid.shape)

        # Display the heatmap for the current amenity
        ax.imshow(z, origin='lower', cmap=custom_cmap, extent=(x_min, x_max, y_min, y_max), alpha=1)

        # Plot the locations of the current amenity
        ax.scatter(x_coords, y_coords, s=10, color=point_color, label=f"{amenity.capitalize()} Locations")

# Plot the boundary of Barcelona for reference
boundary_gdf.plot(ax=ax, edgecolor='white', facecolor='none', linewidth=1.5, label="Barcelona Boundary")

# Titles and labels
ax.set_title("Amenity Density Heatmap within Barcelona Boundary", color='white')
ax.set_xlabel("Easting (meters)", color='white')
ax.set_ylabel("Northing (meters)", color='white')
ax.legend()

# Set colorbar for the first heatmap to represent density
cbar = plt.colorbar(ax.images[0], ax=ax, fraction=0.036, pad=0.04)
cbar.set_label("Density Estimate", color='white')
cbar.ax.yaxis.set_tick_params(color='white')
plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='white')

plt.show()
