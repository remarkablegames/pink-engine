# This file is for common classes and function that need to be loaded after other classes. The general commons
# file is for classes that need to load prior to other files.
import pink_engine.orthogonal_tiled_map as otm


def go_to_map(**kwargs):
    """Allows for dynamic loading of pink engine maps"""
    map_type = kwargs.get('map_type')
    if map_type == "otm":
        otm.go_to_map(target_map=kwargs.get('uni_target_map'), x_coord=kwargs.get('x_coord'),
                      y_coord=kwargs.get('y_coord'), orientation=kwargs.get('orientation'))
