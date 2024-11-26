
import matplotlib.pyplot as plt
from itertools import cycle

def plot_density(ax,boundary_gdf, x_coords,y_coords,point_color,label,x_grid, y_grid, z, bounds, colormap, alpha=1):
    x_min, x_max, y_min, y_max = bounds
    
  
    ax.imshow(z, origin='lower', cmap=colormap, extent=(x_min, x_max, y_min, y_max), alpha=0.2, zorder=1)
    ax.scatter(x_coords, y_coords, s=10, color=point_color, label=label, alpha= 1)
    boundary_gdf.plot(ax=ax, edgecolor='white', facecolor='none', linewidth=1.5, label="Boundary" )
    
    

    

def configure_plot(ax, title, xlabel, ylabel):
    ax.set_facecolor('black')
    ax.set_title(title, color='white')
    ax.set_xlabel(xlabel, color='white')
    ax.set_ylabel(ylabel, color='white')
    ax.legend()
