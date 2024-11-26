
from matplotlib.colors import LinearSegmentedColormap

def create_colormap():
    colors = [(1, 0.75, 0.8, 0), (1, 0.0, 0.0, 1)]
    return LinearSegmentedColormap.from_list("TransparentPink", colors)
