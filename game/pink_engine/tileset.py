import json
from pink_engine.commons import MapElement
from collections import OrderedDict

pink_tileset_dict = {}


class Tileset:
    def __init__(self, tileset_json):
        """
        This class represents a single tileset. This class is designed to work with tileset .json files created through
        the use of the Tiled editor.

        :param str tileset_json: The path to the source json file to be loaded.
        """
        with open(tileset_json) as json_file:
            json_dict = json.load(json_file)

        self.name = json_dict.get('name')

        self.tiles = {}

        pink_tileset_dict[tileset_json] = self

        for tile_dict in json_dict.get('tiles'):
            if 'animation' in tile_dict:
                self.tiles[tile_dict.get('id')] = TilesetAnimatedTile(tile_dict=tile_dict, parent_tileset=self)
            else:
                self.tiles[tile_dict.get('id')] = TilesetTile(tile_dict=tile_dict, parent_tileset=self)

    def get_tile(self, tile_id):
        """
        Retrieves the tile object with the given ID.

        :param int tile_id:
        :return: The tile with the given ID.
        :rtype: TilesetTile
        """
        return self.tiles[tile_id]


class TilesetTile(MapElement):
    def __init__(self, tile_dict, parent_tileset):
        """
        This class represents a single Tile in a tileset.

        :param dict tile_dict: A json-derived dictionary that describes the contents of this tile
        """
        MapElement.__init__(self, tile_dict)
        self.tile_id = tile_dict["id"]
        self.parent = parent_tileset
        self._image = "pink_engine/tilesets/" + tile_dict["image"]
        self._image_width = tile_dict["imagewidth"]
        self._image_height = tile_dict["imageheight"]


class TilesetAnimatedTile(TilesetTile):
    def __init__(self, tile_dict, parent_tileset):
        TilesetTile.__init__(self, tile_dict, parent_tileset)

        self.animation = tile_dict['animation']
        self.frames = OrderedDict()

        ms_counter = 0
        for animation_dict in tile_dict['animation']:
            ms_counter += animation_dict['duration']
            self.frames[ms_counter] = animation_dict['tileid']

        self.animation_time = ms_counter

    def get_frame_image(self, st):
        """
        Get the image for the frame that should be displayed at the given st.
        :param float st: The given show time (in seconds)
        """
        time_in_animation = (st * 1000) % self.animation_time
        for key in self.frames:
            if key >= time_in_animation:
                tile_id = self.frames[key]
                current_tile = self.parent.get_tile(tile_id)
                return current_tile.image

        return self.image
