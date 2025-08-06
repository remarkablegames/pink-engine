from pink_engine.tiled_game import TiledMapGame
import renpy  # noqa
import pygame  # noqa
import json


class TiledMapGameDisplay(TiledMapGame):
    def __init__(self, map_dict, path, **kwargs):
        TiledMapGame.__init__(self, map_dict, path, **kwargs)


def go_to_map(target_map, func, *args, **kwargs):
    map_file = renpy.exports.file("pink_engine/orthogonal_tiled_maps/" + target_map)
    map_dict = json.load(map_file)
    new_map = TiledMapGameDisplay(map_dict, "pink_engine/orthogonal_tiled_maps/" + target_map)

    renpy.store.pink_tmd_current_map = new_map
    renpy.exports.call('pink_tmd_call_map', func, *args, **kwargs)
