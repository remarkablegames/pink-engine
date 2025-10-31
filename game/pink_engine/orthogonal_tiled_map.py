import math
from math import sqrt, ceil, floor
import json
import random
import os
import heapq
from typing import List, Tuple, Optional, Dict, Union

from pink_engine.tiled_game import TiledMapGame, TiledMapGameObject, TiledMapSpriteCollection, \
    TiledMapGameObjectSpriteCollection, TiledMapGameLayer, TiledMapGameTile, TiledMapCamera, \
    TiledMapGameTileAnimated, LAYER_PRIORITY, Overlay, OverlayImage, OverlayText, OverlaySolid, OverlayManager
from pink_engine.orthogonal_tiled_map_commands import ControlCommand
from pink_engine.tileset import TilesetTile, TilesetAnimatedTile
import renpy  # noqa
import pygame  # noqa
from pink_engine.commons import Coord, Area


class OrthogonalTiledMapGameObjectBase(object):
    properties = {}
    width = 0
    height = 0
    arc_y_offset = 0

    @property
    def event_on_activate(self):
        """
        :return: The label of the event that should trigger when interacting with this object.
        :rtype: str|None
        """
        if 'event_on_activate' in self.properties:
            return self.properties['event_on_activate']
        else:
            return None

    @event_on_activate.setter
    def event_on_activate(self, value: str):
        self.properties['event_on_activate'] = value

    @property
    def event_on_activate_args(self):
        """
        :return: the list of args to pass along to the event_on_activate label
        :rtype: list
        """
        if 'event_on_activate_args' in self.properties:
            return eval(self.properties['event_on_activate_args'])
        else:
            return []

    @property
    def event_on_activate_kwargs(self):
        """
        :return: the dict of kwargs to pass along to the event_on_activate label
        :rtype: dict
        """
        if 'event_on_activate_kwargs' in self.properties:
            return eval(self.properties['event_on_activate_kwargs'])
        else:
            return {}

    @property
    def event_on_touch(self):
        """
        :return: The label of the event that should trigger when touching this object.
        :rtype: str|None
        """
        if 'event_on_touch' in self.properties:
            return self.properties['event_on_touch']
        else:
            return None

    @property
    def event_on_touch_args(self):
        """
        :return: the list of args to pass along to the event_on_touch label
        :rtype: list
        """
        if 'event_on_touch_args' in self.properties:
            return eval(self.properties['event_on_touch_args'])
        else:
            return []

    @property
    def event_on_touch_kwargs(self):
        """
        :return: the dict of kwargs to pass along to the event_on_touch label
        :rtype: dict
        """
        if 'event_on_touch_kwargs' in self.properties:
            return eval(self.properties['event_on_touch_kwargs'])
        else:
            return {}

    @property
    def code_on_activate(self):
        """
        :return: The code (in string form) that should run when interacting with this object.
        :rtype: str|None
        """
        if 'code_on_activate' in self.properties:
            return self.properties['code_on_activate']
        else:
            return None

    def run_code_on_activate(self):
        exec(self.code_on_activate)

    @property
    def code_on_touch(self):
        """
        :return: The code (in string form) that should run when touching this object.
        :rtype: str|None
        """
        if 'code_on_touch' in self.properties:
            return self.properties['code_on_touch']
        else:
            return None

    def run_code_on_touch(self):
        exec(self.code_on_touch)

    @property
    def code_on_add(self):
        """
        :return: code to run when the object is added to the map
        :rtype: str|None
        """
        if 'code_on_add' in self.properties:
            return self.properties['code_on_add']
        else:
            return None

    def run_code_on_add(self):
        """
        Runs the code_on_add on this object.
        """
        if self.code_on_add is not None:
            exec(self.code_on_add)

    @property
    def code_on_remove(self):
        """
        :return: code to run when the object is removed from the map
        :rtype: str|None
        """
        if 'code_on_remove' in self.properties:
            return self.properties['code_on_remove']
        else:
            return None

    def run_code_on_remove(self):
        """
        Runs the code_on_remove on this object.
        """
        if self.code_on_remove is not None:
            exec(self.code_on_remove)

    @property
    def event_conditional(self):
        """
        :return: The conditions under which this event should trigger. Similar to conditional, but run at the time of
        checking for the presence of events, rather than when rendering the map. Intended to be used for things like
        player orientation.
        :rtype: str
        """
        if "event_conditional" in self.properties:
            return self.properties["event_conditional"]
        else:
            return "True"

    @property
    def event_conditional_met(self):
        """
        :return: Whether or not the event conditional is currently met
        :rtype: bool
        """
        return eval(self.event_conditional)

    @property
    def code_conditional(self):
        """
        :return: The conditions under which this code should trigger. Similar to conditional, but run at the time of
        checking for the presence of code, rather than when rendering the map. Intended to be used for things like
        player orientation.
        :rtype: str
        """
        if "code_conditional" in self.properties:
            return self.properties["code_conditional"]
        else:
            return "True"

    @property
    def code_conditional_met(self):
        """
        :return: Whether or not the code conditional is currently met
        :rtype: bool
        """
        return eval(self.code_conditional)

    @property
    def base_offset_x_start(self):
        """
        :return: The x offset of the start of the object's base (where the object begins for mapping and event
        purposes in relation to where the image of the object begins)
        :rtype: int
        """
        if "base_offset_x_start" in self.properties:
            return self.properties["base_offset_x_start"]
        else:
            return 0

    @property
    def base_offset_x_end(self):
        """
        :return: The x offset of the end of the object's base (where the object ends for mapping and event
        purposes in relation to where the image of the object begins)
        :rtype: int
        """
        if "base_offset_x_end" in self.properties:
            return self.properties["base_offset_x_end"]
        else:
            return self.width

    @property
    def base_offset_y_start(self):
        """
        :return: The y offset of the start of the object's base (where the object begins for mapping and event
        purposes in relation to where the image of the object begins)
        :rtype: int
        """
        if "base_offset_y_start" in self.properties:
            return self.properties["base_offset_y_start"]
        else:
            return 0

    @property
    def base_offset_y_end(self):
        """
        :return: The y offset of the end of the object's base (where the object ends for mapping and event
        purposes in relation to where the image of the object begins)
        :rtype: int
        """
        if "base_offset_y_end" in self.properties:
            return self.properties["base_offset_y_end"]
        else:
            return self.height

    @property
    def move_from(self):
        """
        :return: The movement allowed from a square occupied by this object.
        :rtype: str|None
        """
        if "move_from" in self.properties:
            return self.properties["move_from"]
        else:
            return None

    @property
    def move_to(self):
        """
        :return: The movement allowed to a square occupied by this object.
        :rtype: str|None
        """
        if "move_to" in self.properties:
            return self.properties["move_to"]
        else:
            return None

    @property
    def override_go_right(self):
        """
        :return: the list of movements that overrides a normal go_right on this coordinate. Returned as string, so can
        be evaluated in context of the object carrying out the commands.
        :rtype: str|None
        """
        if "override_go_right" in self.properties:
            return self.properties["override_go_right"]
        else:
            return None

    @property
    def override_go_left(self):
        """
        :return: the list of movements that overrides a normal go_left on this coordinate. Returned as string, so can
        be evaluated in context of the object carrying out the commands.
        :rtype: str|None
        """
        if "override_go_left" in self.properties:
            return self.properties["override_go_left"]
        else:
            return None

    @property
    def override_go_up(self):
        """
        :return: the list of movements that overrides a normal go_up on this coordinate. Returned as string, so can
        be evaluated in context of the object carrying out the commands.
        :rtype: str|None
        """
        if "override_go_up" in self.properties:
            return self.properties["override_go_up"]
        else:
            return None

    @property
    def override_go_down(self):
        """
        :return: the list of movements that overrides a normal go_down on this coordinate. Returned as string, so can
        be evaluated in context of the object carrying out the commands.
        :rtype: str|None
        """
        if "override_go_down" in self.properties:
            return self.properties["override_go_down"]
        else:
            return None

    @property
    def override_go_right_condition(self):
        """
        :return: the conditions for overriding the movement on this coordinate.
        :rtype: str
        """
        if "override_go_right_condition" in self.properties:
            return self.properties["override_go_right_condition"]
        else:
            return None

    @property
    def override_go_left_condition(self):
        """
        :return: the conditions for overriding the movement on this coordinate.
        :rtype: str
        """
        if "override_go_left_condition" in self.properties:
            return self.properties["override_go_left_condition"]
        else:
            return None

    @property
    def override_go_up_condition(self):
        """
        :return: the conditions for overriding the movement on this coordinate.
        :rtype: str
        """
        if "override_go_up_condition" in self.properties:
            return self.properties["override_go_up_condition"]
        else:
            return None

    @property
    def override_go_down_condition(self):
        """
        :return: the conditions for overriding the movement on this coordinate.
        :rtype: str
        """
        if "override_go_down_condition" in self.properties:
            return self.properties["override_go_down_condition"]
        else:
            return None

    @property
    def override_go_right_coord_offsets(self) -> Optional[List[Tuple[int, int]]]:
        """
        return: The coordinate offsets for a special movement on this coordinate.
        """
        property_name = "override_go_right_coord_offsets"
        if property_name in self.properties:
            return eval(self.properties[property_name])
        else:
            return None

    @property
    def override_go_left_coord_offsets(self) -> Optional[List[Tuple[int, int]]]:
        """
        return: The coordinate offsets for a special movement on this coordinate.
        """
        property_name = "override_go_left_coord_offsets"
        if property_name in self.properties:
            return eval(self.properties[property_name])
        else:
            return None

    @property
    def override_go_up_coord_offsets(self) -> Optional[List[Tuple[int, int]]]:
        """
        return: The coordinate offsets for a special movement on this coordinate.
        """
        property_name = "override_go_up_coord_offsets"
        if property_name in self.properties:
            return eval(self.properties[property_name])
        else:
            return None

    @property
    def override_go_down_coord_offsets(self) -> Optional[List[Tuple[int, int]]]:
        """
        return: The coordinate offsets for a special movement on this coordinate.
        """
        property_name = "override_go_down_coord_offsets"
        if property_name in self.properties:
            return eval(self.properties[property_name])
        else:
            return None

    @property
    def override_go_right_g_inc(self) -> Optional[int]:
        """
        return: The g value increment for calculating smart movement cost
        """
        property_name = "override_go_right_g_inc"
        if property_name in self.properties:
            return self.properties[property_name]
        else:
            return None

    @property
    def override_go_left_g_inc(self) -> Optional[int]:
        """
        return: The g value increment for calculating smart movement cost
        """
        property_name = "override_go_left_g_inc"
        if property_name in self.properties:
            return self.properties[property_name]
        else:
            return None

    @property
    def override_go_up_g_inc(self) -> Optional[int]:
        """
        return: The g value increment for calculating smart movement cost
        """
        property_name = "override_go_up_g_inc"
        if property_name in self.properties:
            return self.properties[property_name]
        else:
            return None

    @property
    def override_go_down_g_inc(self) -> Optional[int]:
        """
        return: The g value increment for calculating smart movement cost
        """
        property_name = "override_go_down_g_inc"
        if property_name in self.properties:
            return self.properties[property_name]
        else:
            return None


class OrthogonalTiledMapGameTileAnimated(TiledMapGameTileAnimated, OrthogonalTiledMapGameObjectBase):
    def __init__(self, parent_map, parent_tile):
        """
        An animated tile in an orthogonal tiled map game.
        :param OrthogonalTiledMap parent_map: The map object that this object is displayed on.
        :param TilesetAnimatedTile parent_tile: The tileset object this tile is inheriting properties from.
        """
        TiledMapGameTileAnimated.__init__(self, parent_map, parent_tile)
        OrthogonalTiledMapGameObjectBase.__init__(self)


class OrthogonalTiledMapGameTile(TiledMapGameTile, OrthogonalTiledMapGameObjectBase):
    def __init__(self, parent_map, parent_tile):
        """
        An non-animated tile in an orthogonal tiled map game.
        :param OrthogonalTiledMap parent_map: The map object that this object is displayed on.
        :param TilesetTile parent_tile: The tileset object this tile is inheriting properties from.
        """
        TiledMapGameTile.__init__(self, parent_map, parent_tile)
        OrthogonalTiledMapGameObjectBase.__init__(self)


class OrthogonalTiledMapGameObject(TiledMapGameObject, OrthogonalTiledMapGameObjectBase):
    def __init__(self, parent_rpg_tile, x, y, width, height, layer, properties):
        """
        A map object in an orthogonal tiled map game.
        :param TilesetTile|TiledMapSpriteCollection parent_rpg_tile: The tileset object this tile is inheriting
        properties from.
        :param int x: Distance in pixels between the object's left side and the left border of the map.
        :param int y: Distance in pixels between the object's top side and the top border of the map.
        :param int width: Width of the object's image, in pixels.
        :param int height: Height of the object's image in pixels.
        :param TiledMapGameLayer layer: The layer this object should be placed on.
        :param dict properties: Dictionary of pink engine properties that applies to this object.
        """
        TiledMapGameObject.__init__(self, parent_rpg_tile, x, y, width, height, layer, properties)
        OrthogonalTiledMapGameObjectBase.__init__(self)

        # The ID of the object used in the base collection, can mutate as object is added and removed, objects that are
        # not visible have a base ID.
        self.base_id = None

        if type(self) is OrthogonalTiledMapGameObject and self.ref_name is not None:
            # Type comparison ensures this only happens at the end of the final loading
            setattr(renpy.store, self.ref_name, self)

    def is_on_map(self):
        """
        Returns whether or not this object is currently present on the map
        """
        if self.displayable_id is not None or self.base_id is not None:
            return True
        return False

    def pixel_to_centralize_on_coord(self, x_coord, y_coord):
        """
        Returns the x and y this object should be set to in order for its base to be centered on the given coordinates.
        :param int x_coord: The given x coordinate
        :param int y_coord: the given y coordinate
        """
        tile_width = self.parent.tile_size.x
        tile_height = self.parent.tile_size.y

        x_pixel = (x_coord * tile_width) + ceil(float(tile_width - self.base_width) / 2.0) - self.base_offset_x_start
        y_pixel = (y_coord * tile_height) + ceil(float(tile_height - self.base_height) / 2.0) - self.base_offset_y_start

        return x_pixel, y_pixel

    @property
    def base_offset_x_start(self):
        """
        :return: The x offset of the start of the object's base (where the object begins for mapping and event
        purposes in relation to where the image of the object begins)
        :rtype: int
        """
        if "base_offset_x_start" in self.properties:
            return floor(self.properties["base_offset_x_start"] * self.xzoom)
        else:
            return 0

    @property
    def base_offset_x_end(self):
        """
        :return: The x offset of the end of the object's base (where the object ends for mapping and event
        purposes in relation to where the image of the object begins)
        :rtype: int
        """
        if "base_offset_x_end" in self.properties:
            return floor(self.properties["base_offset_x_end"] * self.xzoom)
        else:
            return self.width

    @property
    def base_offset_y_start(self):
        """
        :return: The y offset of the start of the object's base (where the object begins for mapping and event
        purposes in relation to where the image of the object begins)
        :rtype: int
        """
        if "base_offset_y_start" in self.properties:
            return floor(self.properties["base_offset_y_start"] * self.yzoom)
        else:
            return 0

    @property
    def base_offset_y_end(self):
        """
        :return: The y offset of the end of the object's base (where the object ends for mapping and event
        purposes in relation to where the image of the object begins)
        :rtype: int
        """
        if "base_offset_y_end" in self.properties:
            return floor(self.properties["base_offset_y_end"] * self.yzoom)
        else:
            return self.height

    @property
    def camera_offset_x(self):
        """
        :return: By how many pixels to offset the camera on the horizontal axis when focused on this object.
        :rtype: int
        """
        if 'camera_offset_x' in self.properties:
            return self.properties['camera_offset_x']
        else:
            return 0

    @camera_offset_x.setter
    def camera_offset_x(self, value):
        """
        :param int value: New camera offset x value
        """
        self.properties['camera_offset_x'] = value

    @property
    def camera_offset_y(self):
        """
        :return: By how many pixels to offset the camera on the vertical axis when focused on this object.
        :rtype: int
        """
        if 'camera_offset_y' in self.properties:
            return self.properties['camera_offset_y']
        else:
            return 0

    @camera_offset_y.setter
    def camera_offset_y(self, value):
        """
        :param int value: New camera offset x value
        """
        self.properties['camera_offset_y'] = value

    @property
    def coords(self) -> List[Coord]:
        """
        :return: The list of coordinates covered by this object's base.
        """
        return self.parent.base_grid.map_elements[self.base_id].coords

    @property
    def central_coord(self):
        """
        :return: The coordinate covered by the center of this object's base.
        :rtype: Coord
        """
        return self.parent.base_grid.map_elements[self.base_id].central_coord

    @property
    def upper_left_coord(self):
        """
        :return: The map coordinate at which the upper left corner of this object's base resides.
        :rtype: Coord
        """
        return self.parent.base_grid.map_elements[self.base_id].upper_left_coord

    @property
    def upper_coord(self):
        """
        :return: The map coordinate at which the exact middle of the upper end of this object's base resides.
        :rtype: Coord
        """
        return self.parent.base_grid.map_elements[self.base_id].upper_coord

    @property
    def upper_right_coord(self):
        """
        :return: The map coordinate at which the upper right corner of this object's base resides.
        :rtype: Coord
        """
        return self.parent.base_grid.map_elements[self.base_id].upper_right_coord

    @property
    def right_coord(self):
        """
        :return: The map coordinate at which the exact middle of the right end of this object's base resides.
        :rtype: Coord
        """
        return self.parent.base_grid.map_elements[self.base_id].right_coord

    @property
    def lower_right_coord(self):
        """
        :return: The map coordinate at which the lower right corner of this object's base resides.
        :rtype: Coord
        """
        return self.parent.base_grid.map_elements[self.base_id].lower_right_coord

    @property
    def lower_coord(self):
        """
        :return: The map coordinate at which the exact middle of the bottom end of this object's base resides.
        :rtype: Coord
        """
        return self.parent.base_grid.map_elements[self.base_id].lower_coord

    @property
    def lower_left_coord(self):
        """
        :return: The map coordinate at which the lower left corner of this object's base resides.
        :rtype: Coord
        """
        return self.parent.base_grid.map_elements[self.base_id].lower_left_coord

    @property
    def left_coord(self):
        """
        :return: The map coordinate at which the exact middle of the left end of this object's base resides.
        :rtype: Coord
        """
        return self.parent.base_grid.map_elements[self.base_id].left_coord

    @property
    def base_x_start(self):
        """
        :return: The distance in pixels between the left side of the base of this object and the left border of the
        map.
        :rtype: int
        """
        return self.parent.base_grid.map_elements[self.base_id].base_x_start

    @property
    def base_x_end(self):
        """
        :return: The distance in pixels between the right side of the base of this object and the left border of the
        map.
        :rtype: int
        """
        return self.parent.base_grid.map_elements[self.base_id].base_x_end

    @property
    def base_y_start(self):
        """
        :return: The distance in pixels between the upper side of the base of this object and the upper border of the
        map.
        :rtype: int
        """
        return self.parent.base_grid.map_elements[self.base_id].base_y_start

    @property
    def base_y_end(self):
        """
        :return: The distance in pixels between the bottom side of the base of this object and the upper border of the
        map.
        :rtype: int
        """
        return self.parent.base_grid.map_elements[self.base_id].base_y_end

    @property
    def start_x_coord(self):
        """
        :return: The first X coordinate covered by this object's base
        :rtype: int
        """
        return self.parent.base_grid.map_elements[self.base_id].start_x_coord

    @property
    def end_x_coord(self):
        """
        :return: The last X coordinate covered by this object's base
        :rtype: int
        """
        return self.parent.base_grid.map_elements[self.base_id].end_x_coord

    @property
    def start_y_coord(self):
        """
        :return: The first Y coordinate covered by this object's base
        :rtype: int
        """
        return self.parent.base_grid.map_elements[self.base_id].start_y_coord

    @property
    def end_y_coord(self):
        """
        :return: The last Y coordinate covered by this object's base
        :rtype: int
        """
        return self.parent.base_grid.map_elements[self.base_id].end_y_coord

    @property
    def base_width(self):
        """
        :return: This object's base's width in pixels.
        :rtype: int
        """
        return self.base_offset_x_end - self.base_offset_x_start

    @property
    def base_height(self):
        """
        :return: This object's base's height in pixels.
        :rtype: int
        """
        return self.base_offset_y_end - self.base_offset_y_start

    @property
    def occultates_as_y(self):
        """
        :return: Which y coordinate this object occultates as.
        :rtype: int
        """
        if 'occultates_as_y' in self.properties:
            return self.properties['occultates_as_y']
        if self.parent.orientation == "orthogonal":
            return floor((self.y + self.base_offset_y_end - 1) / self.parent.tile_size.y)
        else:
            return self.y + self.height - 1

    @property
    def ignores_special_movement(self):
        """
        :return: Whether this object ignores special movement rules
        :rtype: bool
        """
        if 'ignores_special_movement' in self.properties:
            return self.properties['ignores_special_movement']
        else:
            return False


class OrthogonalTiledMapGameObjectMobile(OrthogonalTiledMapGameObject):
    movement_commands = {}

    def __init__(self, parent_rpg_tile, x, y, width, height, layer, properties):
        """
        A map object in an orthogonal tiled map game.
        :param TilesetTile|TiledMapSpriteCollection parent_rpg_tile: The tileset object this tile is inheriting
        properties from.
        :param int x: Distance in pixels between the object's left side and the left border of the map.
        :param int y: Distance in pixels between the object's top side and the top border of the map.
        :param int width: Width of the object's image, in pixels.
        :param int height: Height of the object's image in pixels.
        :param TiledMapGameLayer layer: The layer this object should be placed on.
        :param dict properties: Dictionary of pink engine properties that applies to this object.
        """
        OrthogonalTiledMapGameObject.__init__(self, parent_rpg_tile, x, y, width, height, layer, properties)

        self._last_gt = 0.0
        self._command_gt_start = 0.0

        if self.should_load_consistent(properties):
            old_incarnation = getattr(renpy.store, properties['ref_name'],
                                      None)  # type: OrthogonalTiledMapGameObjectMobile
            self.control_stack = old_incarnation.control_stack
            self.follower = old_incarnation.follower

            # Command handling variables
            self._current_command = old_incarnation._current_command  # type: ControlCommand
            self._command_gt_end = old_incarnation._command_gt_end - old_incarnation._last_gt
            self._command_x_start = old_incarnation.x  # type: int
            self._command_y_start = old_incarnation.y  # type: int
            self._command_arc_height = old_incarnation._command_arc_height  # type: int
            self.arc_y_offset = 0
            self.x = old_incarnation.x  # type: int
            self.y = old_incarnation.y  # type: int
            self._command_x_end = old_incarnation._command_x_end
            self._command_y_end = old_incarnation._command_y_end
            self.prev_coord = old_incarnation.prev_coord

        else:
            self.control_stack = self.default_control_stack
            self.follower = None

            # Command handling variables
            self._current_command = None
            self._command_gt_end = 0.0
            self._command_x_start = self.x
            self._command_y_start = self.y
            self._command_arc_height = 0  # arc height in pixels
            self.arc_y_offset = 0
            self._command_x_end = self.x
            self._command_y_end = self.y
            self.prev_coord = None

        # Saved Command handling variables
        self._save_x = self._command_x_end
        self._save_y = self._command_y_end
        self._saved_control_stack = []
        self._saved_repeat_commands = self.repeat_commands

        # Set to True if object should seize all movement.
        self.frozen = False

        if type(self) is OrthogonalTiledMapGameObjectMobile and self.ref_name is not None:
            # Type comparison ensures this only happens at the end of the final loading
            setattr(renpy.store, self.ref_name, self)

    @property
    def is_moving(self) -> bool:
        return len(self.control_stack) != 0 or self._current_command is not None

    def per_tick(self, gt):
        """
        What this object should do per game tick.
        :param float gt: The amount of seconds of game time that have passed.
        """
        if gt < self._last_gt:
            self.rebase_st(gt)
        if self.check_touch_every_frame and self.parent is renpy.store.pink_otm_current_map:
            # parent comparison is false during transitions
            if (
                    self.parent.player_object is not None and
                    self.parent.player_object.central_coord in self.coords and
                    self._command_gt_start != self._command_gt_end):
                self.parent.check_touch(self)
        if not self.frozen:
            if self._current_command is not None:
                self._update_command(gt)
            if self._current_command is None and len(self.control_stack) > 0:
                self._consume_command(gt)
        self._last_gt = gt

    def set_to_coords(self, x_coord, y_coord, **kwargs):
        """
        Instantly moves this object so that its base is centered on the given coordinates. Note that this overrides
        the saved x and saved y as well, so if used during a dynamic event, it will cause the object to not return
        to its starting location.
        :param int x_coord: The given x coordinate
        :param int y_coord: The given y coordinate.
        """
        x, y = self.pixel_to_centralize_on_coord(x_coord, y_coord)
        self.set_to_x_y(x, y, **kwargs)

    def set_to_x_y(self, x, y, override_prev_coord=True, **kwargs):
        """
        Instantly moves this object so that the left side of its image is x pixels from the left border of the map and
        the top side of its image is y pixels from the top right border of the map. Note that this overrides
        the saved x and saved y as well, so if used during a dynamic event, it will cause the object to not return
        to its starting location.
        :param bool override_prev_coord: Whether to override the previous coordinate
        :param int x: The given x
        :param int y: The given y
        """
        if self.is_conditional:  # So that enabling a conditional object and then immediately moving it is possible.
            self.parent.check_conditional_object(self)

        self.x, self.y = x, y
        self._save_x, self._save_y = x, y
        self._command_x_start = x
        self._command_y_start = y
        self._command_x_end = x
        self._command_y_end = y

        if self.displayable_id is not None:
            self.parent.move_element(self.displayable_id, x, y)
        if self.base_id is not None:
            self.parent.base_grid.move_element(self.base_id, x, y)

        if override_prev_coord and self.base_id is not None:
            self.prev_coord = self.central_coord

    def freeze(self):
        """
        Freezes this object (causing it to remain motionless in place until unfrozen)
        """
        self.frozen = True

    def unfreeze(self, increment_gt=True):
        """
        Unfreezes this object
        :param bool increment_gt: Whether or not to increment the GT. When unfreezing on game load, this should not be
        done. Otherwise, it should be done.
        """
        if increment_gt:
            self.increment_gt(self._last_gt)
        self.frozen = False

    def increment_gt(self, gt_diff):
        """
        Increments the movement start and end gt by the given amount. To be used after freezes.
        :param float gt_diff: The value by which to increment the gt.
        """
        self._command_gt_start += gt_diff
        self._command_gt_end += gt_diff

    def save(self):
        """
        Saves this object's current location and control stack, so it can be returned to using the load_and_continue
        function
        """
        self._save_x = self._command_x_end
        self._save_y = self._command_y_end
        self._saved_control_stack = self.control_stack[:]  # py2
        self._saved_repeat_commands = self.repeat_commands

    def save_and_halt(self):
        """
        Saves this object's current location and control stack, so it can be returned to using the load_and_continue
        function, and then causes it to halt (making it finish its current movement and then stand still until given
        new instructions)
        """
        self.save()
        self.control_stack = []

    def save_and_default_interaction(self):
        """
        Saves this object's current location and control stack, so it can be returned to using the load_and_continue
        function, and then causes it to execute its default interaction, after which it halts
        (making it finish its current movement and then stand still until given new instructions)
        """
        self.save()
        self.default_interaction()

    def default_interaction(self):
        """
        Makes this object execute its default interaction, and then halt (making it finish its current movement and
        then stand still until given new instructions)
        If interrupt_on_interaction is true, it does not finish its current movement, but will immediately interrupt
        it.
        """
        if self.interrupt_on_interaction:
            self.interrupt()
        self.control_stack = self.default_interaction_stack

    def load_and_continue(self):
        """
        Restores this object's saved location and control stack, and continues following it.
        """
        self.control_stack = self._saved_control_stack
        self.repeat_commands = self._saved_repeat_commands
        self.set_to_x_y(self._save_x, self._save_y, override_prev_coord=False)

    def _consume_command(self, gt):
        """
        Consumes and executes the top control on the control stack
        :param float gt: The current game time in seconds
        """
        command: ControlCommand = self.control_stack[0]
        self.movement_commands[command.type](self, command=command, gt=gt)

        if command.instant:  # TODO hardcode a limit?
            self._consume_command(gt)

    def _update_command(self, gt):
        """
        Updates this object's current x and y location depending on how far it is into the current control command
        :param float gt: The current game time in seconds
        """
        if gt >= self._command_gt_end:  # Command is done
            self._finish_executing_command()
        elif gt == self._command_gt_start:  # Command has just started
            self.x = self._command_x_start
            self.y = self._command_y_start
        elif gt > self._command_gt_start:  # anywhere in-between.
            proportion = (gt - self._command_gt_start) / (self._command_gt_end - self._command_gt_start)
            self.x = self._command_x_start + (self._command_x_end - self._command_x_start) * proportion
            self.y = self._command_y_start + (self._command_y_end - self._command_y_start) * proportion
            if self._command_arc_height != 0.0:
                # Used for hops and jumps.
                self.arc_y_offset = (
                    - math.pow((2 * math.sqrt(self._command_arc_height) * proportion) - math.sqrt(self._command_arc_height), 2) + self._command_arc_height)  # noqa
                self.y -= self.arc_y_offset
            else:
                self.arc_y_offset = 0
        self.parent.move_element(self.displayable_id, self.x, self.y)

    def rebase_st(self, gt):
        """
        To be called after gt has been reset for whatever reason, causing this object to rebase its current movement
        off the given new gt.
        :param float gt: The new game time in seconds
        """
        self._command_gt_start = float(gt)
        self._command_gt_end -= self._last_gt
        self._command_x_start = self.x
        self._command_y_start = self.y

    def _finish_executing_command(self):
        """
        Finishes executing the current ongoing control command.
        """
        self.x = self._command_x_end
        self.y = self._command_y_end
        self._command_x_start = self.x
        self._command_x_end = self.x
        self._command_y_start = self.y
        self._command_y_end = self.y
        self._command_arc_height = 0.0
        self.arc_y_offset = 0

        self._current_command = None

        if (
                self.parent.player_object is not None and
                self.parent.player_object.central_coord in self.coords and
                self._command_gt_start != self._command_gt_end
        ):
            self._command_gt_start = self._command_gt_end
            # Otherwise, doesn't finishing moving until after event has already started, which can cause glitches.
            self.parent.move_element(self.displayable_id, self.x, self.y)
            self.parent.check_touch(self)
        self._command_gt_start = self._command_gt_end

    def interrupt(self):
        """
        Finishes executing the current ongoing command, meant for usage during events.
        """
        self.x = self._command_x_end
        self.y = self._command_y_end
        self._command_x_start = self.x
        self._command_x_end = self.x
        self._command_y_start = self.y
        self._command_y_end = self.y
        self._command_arc_height = 0.0
        self.arc_y_offset = 0

        self._current_command = None

        if (
                self.parent.player_object is not None and
                self.parent.player_object.central_coord in self.coords and
                self._command_gt_start != self._command_gt_end
        ):
            self._command_gt_start = self._last_gt
            # Otherwise, doesn't finishing moving until after event has already started, which can cause glitches.
            self.parent.move_element(self.displayable_id, self.x, self.y)
        self._command_gt_start = self._last_gt

    def _play_movement_sound(self, can_move: bool) -> None:
        """
        Plays an appropriate movement sound for the character's current ongoing movement.
        """
        if self.movement_sound_function is not None:  # Sound for being able to move.
            central_coord = self.central_coord
            sound_function = getattr(renpy.store, self.movement_sound_function)
            sound_function(moving_npc=self, x_coord=central_coord.x, y_coord=central_coord.y, can_move=can_move)

    def _command_move_direction(self, command, gt, target_x, target_y, pop=True, turned=False):
        """
        Move a single square in a non-diagonal direction
        :param ControlCommand command: The control command which caused this movement
        :param float gt: The current game time in seconds
        :param int target_x: The x this object should have at the end of the given movement.
        :param int target_y: The y this object should have at the end of the given movement.
        :param bool pop: If True, removes the current top object from the control stack (affected by the command's
        pop_invalid_move value).
        """
        self._current_command = command

        # get movement_speed
        if command.movement_time is not None:
            movement_time = command.movement_time
        else:
            movement_time = self.movement_speed

        self._command_gt_start = gt
        self._command_gt_end = gt + movement_time
        self._command_x_start, self._command_y_start = self.x, self.y
        if (
                self.can_always_move or
                self.parent.base_grid.is_move_permitted(
                    self.base_id, target_x, target_y, ignore_elements=command.ignore_elements)
        ):
            self.prev_coord = self.central_coord
            self.parent.base_grid.move_element(self.base_id, target_x, target_y)
            self._command_x_end = target_x
            self._command_y_end = target_y
            self._command_arc_height = command.arc_height
            self._play_movement_sound(can_move=True)
            if pop:
                self.finish_command(command)
        else:
            if not turned:
                self._play_movement_sound(can_move=False)
            else:
                self._play_movement_sound(can_move=True)
            self._command_x_end, self._command_y_end = self.x, self.y
            interact_on_fail = command.interact_on_fail
            if pop and command.pop_invalid_move:
                self.finish_command(command)
            if interact_on_fail:
                renpy.store.pink_otm_current_map.player_interaction()

    def command_move_left(self, command, gt, pop=True, turned=False):
        """
        Move a single square to the left
        :param ControlCommand command: The control command which caused this movement
        :param float gt: The current game time in seconds
        :param bool pop: If True, removes the current top object from the control stack (affected by the command's
        pop_invalid_move value).
        :param bool turned: if True, indicates that the player has turned as part of the same movement as this. Used
        to prevent movement block sounds if a turn was successful
        """
        self._command_move_direction(
            command=command, gt=gt, target_x=self.x - self.parent.tile_size.x, target_y=self.y, pop=pop, turned=turned)

    def command_move_right(self, command, gt, pop=True, turned=False):
        """
        Move a single square to the right
        :param ControlCommand command: The control command which caused this movement
        :param float gt: The current game time in seconds
        :param bool pop: If True, removes the current top object from the control stack (affected by the command's
        pop_invalid_move value).
        :param bool turned: if True, indicates that the player has turned as part of the same movement as this. Used
        to prevent movement block sounds if a turn was successful
        """
        self._command_move_direction(
            command=command, gt=gt, target_x=self.x + self.parent.tile_size.x, target_y=self.y, pop=pop, turned=turned)

    def command_move_up(self, command, gt, pop=True, turned=False):
        """
        Move a single square up
        :param ControlCommand command: The control command which caused this movement
        :param float gt: The current game time in seconds
        :param bool pop: If True, removes the current top object from the control stack (affected by the command's
        pop_invalid_move value).
        :param bool turned: if True, indicates that the player has turned as part of the same movement as this. Used
        to prevent movement block sounds if a turn was successful
        """
        self._command_move_direction(
            command=command, gt=gt, target_x=self.x, target_y=self.y - self.parent.tile_size.y, pop=pop, turned=turned)

    def command_move_down(self, command, gt, pop=True, turned=False):
        """
        Move a single square down
        :param ControlCommand command: The control command which caused this movement
        :param float gt: The current game time in seconds
        :param bool pop: If True, removes the current top object from the control stack (affected by the command's
        pop_invalid_move value).
        :param bool turned: if True, indicates that the player has turned as part of the same movement as this. Used
        to prevent movement block sounds if a turn was successful
        """
        self._command_move_direction(
            command=command, gt=gt, target_x=self.x, target_y=self.y + self.parent.tile_size.y, pop=pop, turned=turned)

    def command_move_to(self, command, gt):
        """
        Executes and consumes a go_to command, causing an object to move towards a location. The command isn't
        finished until the object has reached the location
        :param ControlCommand command: The command being executed
        :param float gt: The current game time in seconds
        """
        target = command.target

        central_coord = self.central_coord
        if type(target) is str:  # noqa
            target_object = getattr(renpy.store, target)  # Py2
            if target_object is not None:
                target_coord = target_object.central_coord
                target = (target_coord.x, target_coord.y)
            else:
                self.finish_command(command)

        if central_coord.y < target[1]:
            self.command_move_down(command, gt, pop=False)
        elif central_coord.y > target[1]:
            self.command_move_up(command, gt, pop=False)
        elif central_coord.x < target[0]:
            self.command_move_right(command, gt, pop=False)
        elif central_coord.x > target[0]:
            self.command_move_left(command, gt, pop=False)

        # Updates coords after movement
        central_coord = self.central_coord

        # If single step is disabled, then the command isn't consumed until the object reaches the target.
        if (central_coord.x, central_coord.y) == target or command.single_step:
            self.finish_command(command)

    def command_move_random(self, command, gt):
        """
        Executes a move_random command, causing the object to move in a random direction.
        :param ControlCommand command: The command being executed.
        :param float gt: The current game time in seconds
        """
        directions = ["up", "down", "left", "right"]

        for coord in self.coords:
            if "right" in directions and coord.x >= command.max_x:
                directions.remove("right")
            if "left" in directions and coord.x <= command.min_x:
                directions.remove("left")
            if "down" in directions and coord.y >= command.max_y:
                directions.remove("down")
            if "up" in directions and coord.y <= command.min_y:
                directions.remove("up")

        if len(directions) == 0:
            # If no movement is permitted.
            self.finish_command(command)
        else:
            random_direction = random.choice(directions)

            if random_direction == "up":
                self.command_move_up(command, gt)
            elif random_direction == "down":
                self.command_move_down(command, gt)
            elif random_direction == "left":
                self.command_move_left(command, gt)
            if random_direction == "right":
                self.command_move_right(command, gt)

    def command_delay(self, command, gt):
        """
        Executes a delay command, causing the object to wait a number of seconds until consuming its next command.
        :param ControlCommand command: The command being executed.
        :param float gt: The current game time in seconds
        """
        delay_quantity = command.quantity
        if delay_quantity is None:  # Delays default to 1 second.
            delay_quantity = 1.0

        self._command_gt_start = gt
        self._command_gt_end = gt + delay_quantity
        self._current_command = command

        self.finish_command(command)

    def command_change_movement_speed(self, command, gt):
        """
        Executes and consumes a 'change_movement_speed' command, which changes the movement speed of the object.
        Defaults to a speed of 0.14 if no speed is provided.
        :param ControlCommand command: The command being executed.
        :param float gt: The current game time in seconds
        """
        self._current_command = command
        new_speed = command.quantity
        if new_speed is None:
            new_speed = 0.14

        self.movement_speed = new_speed

        if self.follower is not None:
            self.follower.control_stack.append(command)

        self._command_gt_start = gt
        self._command_gt_end = gt

        self.finish_command(command)

    def command_play_sound(self, command, gt):
        """
        Executes and consumes a 'play_sound' command, which causes a sound effect to play. Sound effect's path and the
        channel on which it is to be played are both specified in the command
        :param ControlCommand command: The command being executed.
        :param float gt: The current game time in seconds
        """
        renpy.store.pink_sound_manager.play_sound(
            sound_file=command.path,
            emitter=self,
            pan=command.pan_sound,
            scale=command.scale_sound,
            max_volume_distance=command.max_volume_distance,
            min_volume_distance=command.min_volume_distance,
            min_volume=command.min_volume,
            max_volume=command.max_volume,
            max_pan_distance=command.max_pan_distance,
            no_pan_distance=command.no_pan_distance,
            max_pan=command.max_pan,
            mixer=command.mixer
        )

        self._command_gt_start = gt
        self._command_gt_end = gt
        self.finish_command(command)

    def command_execute_code(self, command, gt):
        """
        Executes and consumes a 'execute_code' command, which executes an arbitrary piece of code.
        :param ControlCommand command: The command being executed.
        :param float gt: The current game time in seconds
        """
        self._command_gt_start = gt
        self._command_gt_end = gt
        self.finish_command(command)
        exec(command.code)

    def finish_command(self, command):
        """
        Finishes consuming the object on top of the control stack, popping it from the stack. Depending on this object's
        repeat_commands value and the never_repeat value of the given command, the popped command may be re-appended to
        the end of the control stack.
        :param ControlCommand command: The command being executed.
        """
        self.control_stack.pop(0)
        if self.repeat_commands and not command.never_repeat:
            self.control_stack.append(command)
        else:
            del command

    def interrupt_delay(self):
        """
        If this object is currently executing a delay command, that delay is set to end at this object's last gt.
        """
        if self._current_command is not None and self._current_command.type == "delay":
            self._command_gt_end = self._last_gt

    def interrupt_animation(self):
        """
        If this object is currently executing a play_animation command, that animation will be cut off and the object
        returned to its stand_animation.
        """
        if self._current_command is not None and self._current_command.type == "play_animation":
            self._command_gt_end = self._last_gt

    def interrupt_control(self):
        """
        Interrupts ongoing non-movement commands.
        """
        self.interrupt_delay()
        self.interrupt_animation()

    def in_place(self, x_coord=None, y_coord=None, orientation=None, finished_moving=True):
        """
        Returns True if the character is in the given location.
        :param int x_coord: the given x coordinate. None for wildcard.
        :param int y_coord: the given y coordinate. None for wildcard.
        :param str orientation: The given orientation. None for wildcard.
        :param bool finished_moving: Whether the control stack needs to be empty.
        :return:
        """
        if not self.is_on_map():  # Not currently on the map for whatever reason
            return False
        if x_coord is not None and self.central_coord.x != x_coord:
            return False
        if y_coord is not None and self.central_coord.y != y_coord:
            return False
        if finished_moving and (self.control_stack != [] or self._current_command is not None):
            return False
        return True

    @property
    def repeat_commands(self):
        """
        Returns a boolean that indicates whether this object repeats its command list.
        :return: a boolean that indicates whether this object repeats its command list.
        :rtype: bool
        """
        if 'repeat_commands' in self.properties:
            return self.properties['repeat_commands']
        else:
            return True

    @repeat_commands.setter
    def repeat_commands(self, value):
        """
        :param bool value: The given value to set the repeat commands to.
        """
        self.properties['repeat_commands'] = value

    @property
    def movement_speed(self):
        """
        Returns the current movement speed.
        :return: The current movement speed.
        :rtype: float
        """
        if 'movement_speed' in self.properties:
            return self.properties['movement_speed']
        else:
            return renpy.store.pink_otm_default_npc_move_speed

    @movement_speed.setter
    def movement_speed(self, value):
        """
        Sets the movement speed to the given value
        :param float value: The given value to set the movement speed to.
        """
        self.properties['movement_speed'] = value

    @property
    def default_control_stack(self):
        """
        :return: The default control stack for this object.
        :rtype: list
        """
        if 'default_control_stack' in self.properties:
            return eval(self.properties['default_control_stack'])
        else:
            return []

    @property
    def can_always_move(self):
        """
        :return: If true, this object can always move, even if its movement would normally be invalid.
        :rtype: bool
        """
        if 'can_always_move' in self.properties:
            return self.properties['can_always_move']
        else:
            return False

    @can_always_move.setter
    def can_always_move(self, value):
        """
        Changes the can_always_move value, allowing characters to move through anything.
        :param bool value: the new value
        """
        self.properties['can_always_move'] = value

    @property
    def default_interaction_stack(self):
        """
        :return: This object's default interaction stack (the list of control commands it should execute when interacted
        with unless otherwise specified by an event)
        :rtype: list
        """
        if "default_interaction_stack" in self.properties:
            return eval(self.properties["default_interaction_stack"])
        else:
            if "turn_on_interaction" in self.properties and self.properties['turn_on_interaction'] is False:
                return []
            else:
                return [ControlCommand("turn_to", target="pink_otm_current_pc", never_repeat=True)]

    @property
    def interrupt_on_interaction(self) -> bool:
        if "interrupt_on_interaction" in self.properties:
            return True
        else:
            return False

    @property
    def check_touch_every_frame(self):
        """
        :return: Whether to check for a touch event every frame, or only at the end of each movement. Useful for
        objects that must react to the player's touch.
        :rtype: bool
        """
        if 'check_touch_every_frame' in self.properties:
            return self.properties['check_touch_every_frame']
        else:
            return False

    @property
    def movement_sound_function(self) -> Optional[str]:
        """
        :return: The name of the function to call to play movement sounds for this object. The default valid values for
        this are 'pink_movement_sound_terrain' and 'pink_movement_sound_static'.
        """
        return self.properties.get('movement_sound_function')

    @movement_sound_function.setter
    def movement_sound_function(self, value: str):
        self.properties['movement_sound_function'] = value

    @property
    def movement_sound_blocked(self) -> Optional[str]:
        """
        :return: The filepath for the sound effect to play for unsuccessful movement.
        """
        return self.properties.get('movement_sound_blocked')

    @movement_sound_blocked.setter
    def movement_sound_blocked(self, value: str):
        self.properties['movement_sound_blocked'] = value

    @property
    def movement_sound(self) -> Optional[str]:
        """
        :return: The filepath for the sound effect to play for succesful movement. Only has an effect for objects
        with the movement sound function 'pink_movement_sound_static'.
        """
        return self.properties.get('movement_sound')

    @movement_sound.setter
    def movement_sound(self, value: str):
        self.properties['movement_sound'] = value

    @property
    def movement_sound_multiplier(self) -> float:
        """
        Multiplies the volume of the movement sound effects by the given value.
        """
        if 'movement_sound_multiplier' in self.properties:
            return self.properties.get('movement_sound_multiplier')
        else:
            return renpy.store.pink_otm_default_npc_movement_sound_multiplier

    @movement_sound_multiplier.setter
    def movement_sound_multiplier(self, value: float):
        self.properties['movement_sound'] = value

    @property
    def movement_sound_max_distance(self) -> int:
        """
        The maximum distance in tiles at which you can hear movement sounds from this object.
        """
        if 'movement_sound_max_distance' in self.properties:
            return self.properties.get('movement_sound_max_distance')
        else:
            return renpy.store.pink_otm_default_no_movement_volume_distance

    @movement_sound_max_distance.setter
    def movement_sound_max_distance(self, value: int):
        self.properties['movement_sound_max_distance'] = value


OrthogonalTiledMapGameObjectMobile.movement_commands = {
    "move_to": OrthogonalTiledMapGameObjectMobile.command_move_to,
    "move_left": OrthogonalTiledMapGameObjectMobile.command_move_left,
    "move_right": OrthogonalTiledMapGameObjectMobile.command_move_right,
    "move_up": OrthogonalTiledMapGameObjectMobile.command_move_up,
    "move_down": OrthogonalTiledMapGameObjectMobile.command_move_down,
    "move_random": OrthogonalTiledMapGameObjectMobile.command_move_random,
    "delay": OrthogonalTiledMapGameObjectMobile.command_delay,
    "change_movement_speed": OrthogonalTiledMapGameObjectMobile.command_change_movement_speed,
    "play_sound": OrthogonalTiledMapGameObjectMobile.command_play_sound,
    "execute_code": OrthogonalTiledMapGameObjectMobile.command_execute_code
}


class PathfindingNode(object):
    def __init__(self, parent, coord, direction, g, override, override_condition=None):
        self.parent = parent
        self.coord = coord
        self.direction = direction

        if self.parent is None:
            self.path = []
        else:
            self.path = parent.path[:]

        self.override = override
        self.override_condition = override_condition

        self.g = g
        self.h = 0
        self.f = 0

    def __gt__(self, other):
        return self.f > other.f

    def __eq__(self, other):
        """
        Returns equal if the coordinate is the same. The other values don't matter at all.
        """
        return self.coord == other.coord

    def eval_override_condition(self, override_condition):  # noqa cannot be static since self is used in the condition.
        """
        Evaluates the given override condition from the perspective of this node.
        """
        if override_condition is not None:
            return eval(override_condition)
        else:
            return True

    # TODO: All of these assume that the parent object is only one coord large. This is not necessarily true.

    @property
    def coords(self) -> List[Coord]:
        """
        A counterparty of the OrthogonalTiledGameObjectBase property, for the purposes of evaluating override_condition
        """
        return [self.coord]

    @property
    def central_coord(self) -> Coord:
        """
        A counterparty of the OrthogonalTiledGameObjectBase property, for the purposes of evaluating override_condition
        """
        return self.coord

    @property
    def upper_left_coord(self) -> Coord:
        """
        A counterparty of the OrthogonalTiledGameObjectBase property, for the purposes of evaluating override_condition
        """
        return self.coord

    @property
    def upper_coord(self) -> Coord:
        """
        A counterparty of the OrthogonalTiledGameObjectBase property, for the purposes of evaluating override_condition
        """
        return self.coord

    @property
    def upper_right_coord(self) -> Coord:
        """
        A counterparty of the OrthogonalTiledGameObjectBase property, for the purposes of evaluating override_condition
        """
        return self.coord

    @property
    def right_coord(self) -> Coord:
        """
        A counterparty of the OrthogonalTiledGameObjectBase property, for the purposes of evaluating override_condition
        """
        return self.coord

    @property
    def lower_right_coord(self) -> Coord:
        """
        A counterparty of the OrthogonalTiledGameObjectBase property, for the purposes of evaluating override_condition
        """
        return self.coord

    @property
    def lower_coord(self) -> Coord:
        """
        A counterparty of the OrthogonalTiledGameObjectBase property, for the purposes of evaluating override_condition
        """
        return self.coord

    @property
    def lower_left_coord(self) -> Coord:
        """
        A counterparty of the OrthogonalTiledGameObjectBase property, for the purposes of evaluating override_condition
        """
        return self.coord

    @property
    def left_coord(self):
        """
        A counterparty of the OrthogonalTiledGameObjectBase property, for the purposes of evaluating override_condition
        """
        return self.coord

    @property
    def start_x_coord(self) -> int:
        """
        A counterparty of the OrthogonalTiledGameObjectBase property, for the purposes of evaluating override_condition
        """
        return self.coord[0]

    @property
    def end_x_coord(self):
        """
        A counterparty of the OrthogonalTiledGameObjectBase property, for the purposes of evaluating override_condition
        """
        return self.coord[0]

    @property
    def start_y_coord(self):
        """
        A counterparty of the OrthogonalTiledGameObjectBase property, for the purposes of evaluating override_condition
        """
        return self.coord[1]

    @property
    def end_y_coord(self):
        """
        A counterparty of the OrthogonalTiledGameObjectBase property, for the purposes of evaluating override_condition
        """
        return self.coord[1]


class PathfindingQueue(object):
    def __init__(self):
        self.data = []

    def empty(self):
        """
        :return: Whether or not the heap is empty.
        :rtype: bool
        """
        return not self.data

    def add(self, item, priority):
        """
        :param PathfindingNode item: The item to add.
        :param float priority: The priority with which to push the item on the heap.
        """
        heapq.heappush(self.data, item)

    def get(self):
        """
        :return: the top node on the pathfinding heap.
        :rtype: PathfindingNode
        """
        return heapq.heappop(self.data)


class OrthogonalTiledMapGameObjectSpriteCollection(
    TiledMapGameObjectSpriteCollection, OrthogonalTiledMapGameObjectMobile
):
    movement_commands = {}

    def __init__(self, x, y, layer, properties, collection_path):
        """
        An object that uses a sprite collection on an Orthogonal Tiled Map.
        :param int x: Distance in pixels between the object's left side and the left border of the map.
        :param int y: Distance in pixels between the object's top side and the top border of the map.
        :param TiledMapGameLayer layer: The layer this object should be placed on.
        :param dict properties: Dictionary of pink engine properties that applies to this object.
        :param str collection_path: The path to the sprite collection to use.
        """
        if self.should_load_consistent(properties):
            old_incarnation = getattr(
                renpy.store, properties['ref_name'], None)  # type: OrthogonalTiledMapGameObjectSpriteCollection
            if old_incarnation.sprite_collection_path.startswith('renpy.store'):
                self._initiate_consistent_variable_sprite_collection(old_incarnation=old_incarnation)
            else:
                self.sprite_collection_path = old_incarnation.sprite_collection_path  # note can be a variable name
                self.sprite_collection = old_incarnation.sprite_collection
            self.hidden = old_incarnation.hidden
            self.sprite_collection.st_reset_frames(0.0)
            self.sprite_collection.latest_frame_gt = 0.0
        else:
            self.sprite_collection_path = collection_path
            if collection_path.startswith('renpy.store'):
                collection_path = eval(collection_path)
            self.sprite_collection = TiledMapSpriteCollection(renpy.exports.file(collection_path))
            self.hidden = False

        OrthogonalTiledMapGameObjectMobile.__init__(
            self, self.sprite_collection, x, y, self.sprite_collection.width, self.sprite_collection.height, layer,
            properties)
        TiledMapGameObjectSpriteCollection.__init__(self, x, y, layer, properties, collection_path)

        if type(self) is OrthogonalTiledMapGameObjectSpriteCollection and self.ref_name is not None:
            # Type comparison ensures this only happens at the end of the final loading
            setattr(renpy.store, self.ref_name, self)

    def per_tick(self, gt):
        OrthogonalTiledMapGameObjectMobile.per_tick(self, gt)
        if not self.is_moving:
            self._set_animation(self.stand_animation)

    @property
    def image(self):
        """
        Retrieves the renpy name for the image currently being portrayed by this object.
        :return: The path to the image currently being portrayed by this object.
        :rtype: str|None
        """
        if self.hidden or self.sprite_collection is None:
            return None
        else:
            return self.sprite_collection.image

    def hide(self):
        self.hidden = True

    def reveal(self):
        self.hidden = False

    def _set_animation(self, animation_name, speed=None):
        """
        This function is called to determine the object's current animation set. It calls an oriented animation
        (ex. walk_left) if one is available.
        :param str animation_name: Name of new animation
        :param float speed: Speed at which the animation should be played.
        """
        TiledMapGameObjectSpriteCollection._set_animation(self, animation_name, speed)
        # if self.is_on_map():  # updates display grid in case animation changes size
        #     self.parent.base_grid.move_element(self.base_id, self.x, self.y)
        #     TODO self.x and self.y are not valid because those are image coordinates, not base coordinates. Add
        #      recalculate base function

    def set_to_x_y(self, x, y, override_prev_coord=True, **kwargs):
        """
        Instantly moves this object so that the left side of its image is x pixels from the left border of the map and
        the top side of its image is y pixels from the top right border of the map. Note that this overrides
        the saved x and saved y as well, so if used during a dynamic event, it will cause the object to not return
        to its starting location. Accepts the keyword argument 'orientation', which sets the new orientation.
        :param bool override_prev_coord: Whether to override the previous coordinate
        :param int x: The given x
        :param int y: The given y
        """
        if 'orientation' in kwargs and kwargs['orientation'] is not None:
            self._orientation = kwargs['orientation']
            self._set_animation(self.stand_animation)
        OrthogonalTiledMapGameObjectMobile.set_to_x_y(self, x, y, override_prev_coord, **kwargs)

    def should_be_auto_centered(self):
        """
        Whether this object should be auto-centered.
        :rtype: bool
        """
        return (
                renpy.store.pink_otm_autocenter_sprites and not self.forbid_autocenter and
                (self.base_width % self.parent.tile_size.x != 0 or self.base_height % self.parent.tile_size.y != 0) and
                self.x % self.parent.tile_size.x == 0 and (self.y + self.height) % self.parent.tile_size.y == 0
        )

    def in_place(self, x_coord=None, y_coord=None, orientation=None, finished_moving=True):
        """
        Returns True if the character is in the given location.
        :param int x_coord: the given x coordinate. None for wildcard.
        :param int y_coord: the given y coordinate. None for wildcard.
        :param str orientation: The given orientation. None for wildcard.
        :param bool finished_moving: Whether the control stack needs to be empty.
        :return:
        """
        if not self.is_on_map():  # Not currently on the map for whatever reason
            return False
        central_coord = self.central_coord
        if x_coord is not None and central_coord.x != x_coord:
            return False
        if y_coord is not None and central_coord.y != y_coord:
            return False
        if orientation is not None and self._orientation != orientation:
            return False
        if finished_moving and (self.control_stack != [] or self._current_command is not None):
            return False
        return True

    def switch_sprite_collection(self, target_sprite_collection):
        """
        Switches to a new sprite collection, ensuring that coordinates and animation name are kept the same.
        :param str target_sprite_collection: Path of the new sprite collection.
        """
        target_coord = None
        if self.parent is not None and self.is_on_map():  # TODO fix to add and immediately switch sprite collection
            target_coord = self.central_coord

        if self.parent is not None:
            self.parent.animated_tiles.remove(self.sprite_collection)
        # Get non-directional version of animation name, in cause the new sprite collection doesn't have directional
        # animations
        old_orientation = self.orientation
        animation_name = self.current_animation_name.\
            replace("_left", "").replace("_right", "").replace("_up", "").replace("_down", "")
        start_time = self.sprite_collection.latest_frame_gt

        # Deal with variable sprite collections
        if target_sprite_collection.startswith('renpy.store'):
            self.sprite_collection_path = target_sprite_collection
            target_sprite_collection = eval(target_sprite_collection)
        elif not target_sprite_collection.startswith("pink_engine/sprite_collections/"):
            target_sprite_collection = "pink_engine/sprite_collections/" + target_sprite_collection
            self.sprite_collection_path = target_sprite_collection
        else:
            self.sprite_collection_path = target_sprite_collection

        if self.parent is not None and self.is_on_map():
            self.parent.remove_element(self)

        self.current_animation_name = None  # So new animation doesn't register as the same
        self.sprite_collection = TiledMapSpriteCollection(renpy.exports.file(target_sprite_collection), start_time)
        self._set_animation(animation_name)
        if self.parent is not None:
            self.parent.add_element(0, 0, self.layer, self)
            if self.is_on_map():
                if target_coord is None:
                    # Can happen in rare situations where asynchronous processing on a follower added this frame can
                    #  result in being added to the map halfway through.
                    target_coord = self.central_coord
                self.set_to_coords(target_coord.x, target_coord.y, orientation=old_orientation)  # noqa target_coord exists
            self.parent.animated_tiles.append(self.sprite_collection)

        # Regenerating followers ensures proper rendering synchronization, so that they won't become jittery when the
        # camera is moving.
        if renpy.store.pink_otm_current_pc is not None and self is renpy.store.pink_otm_current_pc:
            old_follower_objects = renpy.store.pink_otm_followers[:]  # py2
            remove_all_followers()
            renpy.store.pink_otm_followers = []
            for old_follower_object in old_follower_objects:
                new_follower = add_player_follower(old_follower_object.sprite_collection_path)
                new_follower.properties = old_follower_object.properties

    def freeze(self):
        """
        Freezes this object (causing it to remain motionless in place until unfrozen)
        """
        self.sprite_collection.pause_animation()
        OrthogonalTiledMapGameObjectMobile.freeze(self)

    def unfreeze(self, increment_gt=True):
        """
        Unfreezes this object
        :param bool increment_gt: Whether or not to increment the GT. When unfreezing on game load, this should not be
        done. Otherwise, it should be done.
        """
        self.sprite_collection.unpause_animation()
        if increment_gt:
            self.sprite_collection.increment_gt(self._last_gt)
        OrthogonalTiledMapGameObjectMobile.unfreeze(self, increment_gt)

    def force_stand(self):
        """
        Forces this object into its stand animation.
        """
        self._set_animation(self.stand_animation)

    def _command_move_direction(self, command, gt, target_x, target_y, pop=True, turned=False):
        """
        Move a single square in a non-diagonal direction
        :param ControlCommand command: The control command which caused this movement
        :param float gt: The current game time in seconds
        :param int target_x: The x this object should have at the end of the given movement.
        :param int target_y: The y this object should have at the end of the given movement.
        :param bool pop: If True, removes the current top object from the control stack (affected by the command's
        pop_invalid_move value).
        """
        self._current_command = command

        # get movement_speed
        if command.movement_time is not None:
            movement_time = command.movement_time
        else:
            movement_time = self.movement_speed

        self._command_gt_start = gt
        self._command_gt_end = gt + movement_time
        self._command_x_start, self._command_y_start = self.x, self.y
        if (
                self.can_always_move or
                self.parent.base_grid.is_move_permitted(
                    self.base_id, target_x, target_y, ignore_elements=command.ignore_elements)
        ):
            self.prev_coord = self.central_coord
            self.parent.base_grid.move_element(self.base_id, target_x, target_y)
            self._set_animation(self.move_animation)
            self._command_x_end = target_x
            self._command_y_end = target_y
            self._command_arc_height = command.arc_height
            self._play_movement_sound(can_move=True)
            if pop:
                self.finish_command(command)
        else:
            if not turned:
                self._play_movement_sound(can_move=False)
            else:
                self._play_movement_sound(can_move=True)
            self._command_x_end, self._command_y_end = self.x, self.y
            if command.animate_invalid_move:
                self._set_animation(self.move_animation)
            else:
                self._set_animation(self.stand_animation)
            interact_on_fail = command.interact_on_fail
            if pop and command.pop_invalid_move:
                self.finish_command(command)
            if interact_on_fail:
                renpy.store.pink_otm_current_map.player_interaction()

    def command_delay(self, command, gt):
        """
        Executes a delay command, causing the object to wait a number of seconds until consuming its next command.
        :param ControlCommand command: The command being executed.
        :param float gt: The current game time in seconds
        """
        OrthogonalTiledMapGameObjectMobile.command_delay(self, command, gt)
        self._set_animation(self.stand_animation)

    def _command_turn_direction(self, command, gt, direction, pop=True, instant=False):
        """
        Turn towards a given direction
        :param ControlCommand command: The command being executed.
        :param float gt: The current game time in seconds
        :param str direction: The new direction this character should face.
        :param bool pop: If True, removes the current top object from the control stack.
        :param bool instant: if True, makes the turn take no time.
        """
        self._current_command = command

        self._orientation = direction
        if command.stand_on_turn:
            self._set_animation(self.stand_animation)

        self._current_command = command
        self._command_gt_start = gt
        if instant:
            self._command_gt_end = gt
        else:
            self._command_gt_end = gt + self.movement_speed
        if pop:
            self.finish_command(command)

    def command_turn_left(self, command, gt, pop=True, instant=False):
        """
        Executes a turn_left command
        :param ControlCommand command: The command being executed.
        :param float gt: The current game time in seconds
        :param bool pop: If True, removes the current top object from the control stack
        :param bool instant: if True, makes the turn take no time.
        """
        self._command_turn_direction(command=command, gt=gt, direction="left", pop=pop, instant=instant)

    def command_turn_right(self, command, gt, pop=True, instant=False):
        """
        Executes a turn_right command
        :param ControlCommand command: The command being executed.
        :param float gt: The current game time in seconds
        :param bool pop: If True, removes the current top object from the control stack
        :param bool instant: if True, makes the turn take no time.
        """
        self._command_turn_direction(command=command, gt=gt, direction="right", pop=pop, instant=instant)

    def command_turn_up(self, command, gt, pop=True, instant=False):
        """
        Executes a turn_up command
        :param ControlCommand command: The command being executed.
        :param float gt: The current game time in seconds
        :param bool pop: If True, removes the current top object from the control stack
        :param bool instant: if True, makes the turn take no time.
        """
        self._command_turn_direction(command=command, gt=gt, direction="up", pop=pop, instant=instant)

    def command_turn_down(self, command, gt, pop=True, instant=False):
        """
        Executes a turn_down command
        :param ControlCommand command: The command being executed.
        :param float gt: The current game time in seconds
        :param bool pop: If True, removes the current top object from the control stack
        :param bool instant: if True, makes the turn take no time.
        """
        self._command_turn_direction(command=command, gt=gt, direction="down", pop=pop, instant=instant)

    def command_turn_clockwise(self, command, gt):
        """
        Executes and consumes a 'turn_clockwise' command, which causes the object to change its orientation in a
        clockwise manner.
        :param ControlCommand command: The command being executed.
        :param float gt: The current game time in seconds
        """
        if self._orientation == "up":
            self.command_turn_right(command, gt)
        elif self._orientation == "right":
            self.command_turn_down(command, gt)
        elif self._orientation == "down":
            self.command_turn_left(command, gt)
        elif self._orientation == "left":
            self.command_turn_up(command, gt)

    def command_turn_counter_clockwise(self, command, gt):
        """
        Executes and consumes a 'turn_counter_clockwise' command, which causes the object to change its orientation in a
        counter-clockwise manner.
        :param ControlCommand command: The command being executed.
        :param float gt: The current game time in seconds
        """
        if self._orientation == "up":
            self.command_turn_left(command, gt)
        elif self._orientation == "right":
            self.command_turn_up(command, gt)
        elif self._orientation == "down":
            self.command_turn_right(command, gt)
        elif self._orientation == "left":
            self.command_turn_down(command, gt)

    def command_turn_random(self, command, gt):
        """
        Executes and consumes a 'turn_random' command, which causes the object to change its orientation to a random
        direction.
        :param ControlCommand command: The command being executed.
        :param float gt: The current game time in seconds
        """
        directions = ["up", "down", "left", "right"]

        if command.exclude_current_direction and self._orientation in directions:
            directions.remove(self._orientation)

        random_direction = random.choice(directions)
        if random_direction == "up":
            self.command_turn_up(command, gt)
        elif random_direction == "right":
            self.command_turn_right(command, gt)
        elif random_direction == "down":
            self.command_turn_down(command, gt)
        elif random_direction == "left":
            self.command_turn_left(command, gt)

    def command_turn_to(self, command, gt, pop=True, instant=False):
        """
        Executes and consumes a 'turn_to' command, which causes the object to change its orientation to face a given
        coordinate or object.
        :param ControlCommand command: The command being executed.
        :param float gt: The current game time in seconds
        :param bool pop: If True, removes the current top object from the control stack
        :param bool instant: if True, makes the turn take no time.
        """
        target = command.target

        central_coord = self.central_coord
        if type(target) is str:  # noqa
            target_object = getattr(renpy.store, target)  # Py2
            if target_object is not None:
                target_coord = target_object.central_coord
                target = (target_coord.x, target_coord.y)
            else:
                self.finish_command(command)
                return
        elif issubclass(type(target), OrthogonalTiledMapGameObject):
            target = target.central_coord

        x_diff = central_coord.x - target[0]
        y_diff = central_coord.y - target[1]
        # If x and y difference are equal, prefers turning left and right. This makes follower movement on stairs
        #  look slightly better.
        if abs(x_diff) >= abs(y_diff) and x_diff > 0:
            self.command_turn_left(command, gt, pop=pop, instant=instant)
        elif abs(x_diff) >= abs(y_diff) and x_diff < 0:
            self.command_turn_right(command, gt, pop=pop, instant=instant)
        elif y_diff > 0:
            self.command_turn_up(command, gt, pop=pop, instant=instant)
        elif y_diff < 0:
            self.command_turn_down(command, gt, pop=pop, instant=instant)
        else:
            self._current_command = command
            self._command_gt_start = gt
            if instant:
                self._command_gt_end = gt
            else:
                self._command_gt_end = gt + self.movement_speed
            if pop:
                self.finish_command(command)

    def _command_go_direction(self, command, gt, direction, turn_func, move_func, pop=True):
        """
        Executes a go command for the given direction. Calls the appropriate turn command if not turned in the given
        direction, otherwise calls the movement command.
        :param ControlCommand command: The command being executed.
        :param float gt: The current game time in seconds
        :param str direction: The given direction
        :param func turn_func: The relevant turn function
        :param func move_func: The relevant movement function
        :param bool pop: Whether or not to pop the top command on the command stack. Should be disabled if the going is
        part of a broader command (as each command should only be popped once)
        """
        if command.turn_and_move:
            turned = False
            if self._orientation != direction:
                turned = True
                turn_func(command, gt, pop=False)
            move_func(command, gt, pop=pop, turned=turned)
        else:
            if self._orientation != direction:
                turn_func(command, gt, pop=pop)
            else:
                move_func(command, gt, pop=pop, turned=False)

    def command_go_left(self, command, gt, pop=True):
        """
        Executes a go_left command. Calls turn_left if the character is not oriented leftwards, and move_left
        otherwise. Does not consume the command, as that happens in its called functions.

        :param ControlCommand command: The command being executed.
        :param float gt: The current game time in seconds
        :param bool pop: Whether or not to pop the top command on the command stack. Should be disabled if the turning
        is part of a broader command (as each command should only be popped once)
        """
        for coord in self.coords:
            if self.ignores_special_movement:
                continue
            override = self.parent.base_grid.get_override_go_left(coord.x, coord.y)
            override_condition = self.parent.base_grid.get_override_go_left_condition(coord.x, coord.y)
            if override is not None and (
                    self.can_always_move or override_condition is None or eval(override_condition)
            ):
                if pop:
                    self.finish_command(command)
                for control in reversed(eval(override)):
                    self.control_stack.insert(0, control)
                break
            elif override is not None:
                self.command_turn_left(command, gt, pop=False)
                break
        else:
            self._command_go_direction(
                command=command, gt=gt, direction="left", turn_func=self.command_turn_left,
                move_func=self.command_move_left, pop=pop)

    def command_go_right(self, command, gt, pop=True):
        """
        Executes a go_right command. Calls turn_right if the character is not oriented rightwards, and move_right
        otherwise. Does not consume the command, as that happens in its called functions.

        :param ControlCommand command: The command being executed.
        :param float gt: The game timebase, in seconds.
        :param bool pop: Whether or not to pop the top command on the command stack. Should be disabled if the going is
        part of a broader command (as each command should only be popped once)
        """
        for coord in self.coords:
            if self.ignores_special_movement:
                continue
            override = self.parent.base_grid.get_override_go_right(coord.x, coord.y)
            override_condition = self.parent.base_grid.get_override_go_right_condition(coord.x, coord.y)
            if override is not None and (
                    self.can_always_move or override_condition is None or eval(override_condition)
            ):
                if pop:
                    self.finish_command(command)
                for control in reversed(eval(override)):
                    self.control_stack.insert(0, control)
                break
            elif override is not None:
                self.command_turn_right(command, gt, pop=False)
                break
        else:
            self._command_go_direction(
                command=command, gt=gt, direction="right", turn_func=self.command_turn_right,
                move_func=self.command_move_right, pop=pop)

    def command_go_up(self, command, gt, pop=True):
        """
        Executes a go_up command. Calls turn_up if the character is not oriented upwards, and move_up
        otherwise. Does not consume the command, as that happens in its called functions.

        :param ControlCommand command: The command being executed.
        :param float gt: The current game time in seconds
        :param bool pop: Whether or not to pop the top command on the command stack. Should be disabled if the going is
        part of a broader command (as each command should only be popped once)
        """
        for coord in self.coords:
            if self.ignores_special_movement:
                continue
            override = self.parent.base_grid.get_override_go_up(coord.x, coord.y)
            override_condition = self.parent.base_grid.get_override_go_up_condition(coord.x, coord.y)
            if override is not None and (
                    self.can_always_move or override_condition is None or eval(override_condition)
            ):
                if pop:
                    self.finish_command(command)
                for control in reversed(eval(override)):
                    self.control_stack.insert(0, control)
                break
            elif override is not None:
                self.command_turn_up(command, gt, pop=False)
                break
        else:
            self._command_go_direction(
                command=command, gt=gt, direction="up", turn_func=self.command_turn_up,
                move_func=self.command_move_up, pop=pop)

    def command_go_down(self, command, gt, pop=True):
        """
        Executes a go_down command. Calls turn_down if the character is not oriented downwards, and move_down
        otherwise. Does not consume the command, as that happens in its called functions.

        :param ControlCommand command: The command being executed.
        :param float gt: The current game time in seconds
        :param bool pop: Whether or not to pop the top command on the command stack. Should be disabled if the going is
        part of a broader command (as each command should only be popped once)
        """
        for coord in self.coords:
            if self.ignores_special_movement:
                continue
            override = self.parent.base_grid.get_override_go_down(coord.x, coord.y)
            override_condition = self.parent.base_grid.get_override_go_down_condition(coord.x, coord.y)
            if override is not None and (
                    self.can_always_move or override_condition is None or eval(override_condition)
            ):
                if pop:
                    self.finish_command(command)
                for control in reversed(eval(override)):
                    self.control_stack.insert(0, control)
                break
            elif override is not None:
                self.command_turn_down(command, gt, pop=False)
                break
        else:
            self._command_go_direction(
                command=command, gt=gt, direction="down", turn_func=self.command_turn_down,
                move_func=self.command_move_down, pop=pop)

    def command_go_to(self, command, gt):
        """
        Executes and consumes a go_to command, causing an object to move towards a location. The command isn't
        finished until the object has reached the location

        :param ControlCommand command: The command being executed
        :param float gt: The current game time in seconds
        """
        target = command.target

        central_coord = self.central_coord
        if type(target) is str:  # noqa
            target = 'renpy.store.' + target
            target_object = eval(target)
            if target_object is not None:
                if command.prev_coord and target_object.prev_coord is not None:
                    target_object_coord = target_object.prev_coord
                else:
                    target_object_coord = target_object.central_coord
                target_coord = (target_object_coord.x, target_object_coord.y)
            else:
                self.finish_command(command)
                return
        else:
            target_coord: Tuple[int, int] = target

        if central_coord.y < target_coord[1]:
            self.command_go_down(command, gt, pop=False)
        elif central_coord.y > target_coord[1]:
            self.command_go_up(command, gt, pop=False)
        elif central_coord.x < target_coord[0]:
            self.command_go_right(command, gt, pop=False)
        elif central_coord.x > target_coord[0]:
            self.command_go_left(command, gt, pop=False)
        else:
            self._set_animation(self.stand_animation)

        # Updates coords after movement
        central_coord = self.central_coord

        # If single step is disabled, then the command isn't consumed until the object reaches the target.
        if central_coord == target_coord or command.single_step:
            self.finish_command(command)

    def command_go_to_smart(self, command, gt):
        """
        Executes and consumes a go_to command, causing an object to move towards a location using a pathfinding
        algorithm. The command isn't finished until the object has reached the location

        :param ControlCommand command: The command being executed
        :param float gt: The current game time in seconds
        """
        target = command.target

        start_coords = self.coords
        if type(target) is str:  # noqa
            target = 'renpy.store.' + target
            target_object = eval(target)
            if target_object is not None:
                if command.prev_coord and target_object.prev_coord is not None:
                    target_coord = target_object.prev_coord
                else:
                    target_coord = target_object.central_coord
                target_coord = Coord(target_coord.x, target_coord.y)
            else:
                self.finish_command(command)
                return
        elif issubclass(type(target), OrthogonalTiledMapGameObject):
            target_coord = target.central_coord
        else:
            target_coord = Coord(target[0], target[1])

        # If no path has been determined, determine path
        if command.pathfinding_path is None or command.path_target != target_coord:
            path = self.get_pathfinding_path(command, target_coord, start_coords)
            command.pathfinding_path = path
            command.path_target = target_coord

        # If a path has been determined, try executing the next step along that path
        if len(command.pathfinding_path) > 0:
            next_direction = command.pathfinding_path[0]

            # Get movement override for position
            override = None
            for coord in start_coords:
                coord_override = self.parent.base_grid.get_override_go_direction(
                    coord.x, coord.y, direction=next_direction)
                if coord_override is not None:
                    # Only analyze the first override per coord
                    override = coord_override
                    break

            if (
                    next_direction == "left" and (
                        self.can_always_move or
                        override is not None or
                        self.parent.base_grid.is_move_permitted(
                            self.base_id, self.x - self.parent.tile_size.x, self.y,
                            ignore_elements=command.ignore_elements))):
                command.pathfinding_path.pop(0)
                self.command_go_left(command, gt, pop=False)
            elif (
                    next_direction == "right" and (
                        self.can_always_move or
                        override is not None or
                        self.parent.base_grid.is_move_permitted(
                            self.base_id, self.x + self.parent.tile_size.x, self.y,
                            ignore_elements=command.ignore_elements))):
                command.pathfinding_path.pop(0)
                self.command_go_right(command, gt, pop=False)
            elif (
                    next_direction == "up" and (
                        self.can_always_move or
                        override is not None or
                        self.parent.base_grid.is_move_permitted(
                            self.base_id, self.x, self.y - self.parent.tile_size.y,
                            ignore_elements=command.ignore_elements))):
                command.pathfinding_path.pop(0)
                self.command_go_up(command, gt, pop=False)
            elif (
                    next_direction == "down" and (
                        self.can_always_move or
                        override is not None or
                        self.parent.base_grid.is_move_permitted(
                            self.base_id, self.x, self.y + self.parent.tile_size.y,
                            ignore_elements=command.ignore_elements))):
                command.pathfinding_path.pop(0)
                self.command_go_down(command, gt, pop=False)
            else:
                # If the path can't be followed, turn to target and recalculate
                self.command_turn_to(command, gt, pop=False, instant=True)
                path = self.get_pathfinding_path(command, target_coord, start_coords)
                command.pathfinding_path = path
        elif target_coord in start_coords or command.pop_invalid_move:
            if command.pop_invalid_move:
                self.command_turn_to(command, gt, pop=False, instant=True)
            # If path is empty and target reached, pop the command
            command.pathfinding_path = None
            command.path_target = None

            self._set_animation(self.stand_animation)

            # Prevents a single frame of inactivity after finishing a go_smart command.
            self.finish_command(command)
            self._finish_executing_command()

            if len(self.control_stack) > 0 and self.control_stack[0] is not command:
                self._consume_command(gt)
        elif command.target_distance > 0:
            # Alternatively, if the goal is to stay a certain distance from a target, check if that target is
            # within reach.
            path = self.get_pathfinding_path(command, target_coord, start_coords)
            if len(path) == 0:
                # Target distance has been reached
                command.pathfinding_path = None
                command.path_target = None

                # Prevents a single frame of inactivity after finishing a go_smart command.
                self.finish_command(command)
                self._finish_executing_command()

                self.command_turn_to(command, gt, pop=False, instant=True)

                if len(self.control_stack) > 0 and self.control_stack[0] is not command:
                    self._consume_command(gt)
            else:
                self.command_turn_to(command, gt, pop=False, instant=True)
                path = self.get_pathfinding_path(command, target_coord, start_coords)
                command.pathfinding_path = path

        else:
            # If path is empty and target has not been reached, turn to target and calculate new path.
            self.command_turn_to(command, gt, pop=False, instant=True)
            path = self.get_pathfinding_path(command, target_coord, start_coords)
            command.pathfinding_path = path

    def _generate_pathfinding_path_children(
            self, node: PathfindingNode, directions: List[str]
    ) -> List[PathfindingNode]:
        """
        Generates all of a PathfindingNode's children, which are the nodes created by moving in the given directions
        from that node. Children will be returned in the same order as the directions given.
        :param node: The node for which to generate children
        :param directions: The list of directions. Determines the order in which the children are returned, allowing
        certain directions to be prioritized (used to keep followers standing behind the player, rather than to their
        side)
        """
        children = []
        for direction in directions:
            override_movement = self.parent.base_grid.get_override_go_direction(
                node.coord.x, node.coord.y, direction)

            if override_movement is not None:
                override_condition = self.parent.base_grid.get_override_condition_direction(
                    node.coord.x, node.coord.y, direction)
                coords = self.parent.base_grid.get_override_smart_coords(node.coord.x, node.coord.y, direction)
                g_increment = self.parent.base_grid.get_override_smart_g_increment(
                    node.coord.x, node.coord.y, direction)

                for coord in coords:
                    children.append(PathfindingNode(
                        parent=node,
                        coord=coord,
                        direction=direction,
                        override=True,
                        override_condition=override_condition,
                        g=node.g + g_increment))
            else:
                children.append(PathfindingNode(
                    parent=node,
                    coord=node.coord.direction(direction),
                    direction=direction,
                    override=False,
                    g=node.g + 1.0))

        return children

    def get_pathfinding_path(self, command: ControlCommand, target_coord: Coord, start_coords: List[Coord]):
        """
        Determines the pathfinding path for the command_go_to_smart function

        :param command: The command being executed
        :param target_coord: the final coord of the path
        :param start_coords: the first coords of the path (a list since an object can occupy more than one coord)
        """
        target = PathfindingNode(None, target_coord, direction=None, g=None, override=False)
        open_list = PathfindingQueue()
        closest_node = None
        closed_set = set()
        coord_cost_dict = {}

        # Ensures that followers will walk behind you, rather than by your side.
        directions = ["left", "right", "up", "down"]
        if command.target_distance > 0:
            command_target = command.target
            if type(command_target) is str:  # noqa
                command_target = 'renpy.store.' + command_target
                target_object = eval(command_target)
                if hasattr(target_object, "orientation"):
                    if target_object.orientation in {'left', 'right'}:
                        directions = ["up", "down", "left", "right"]
            elif issubclass(type(command_target), OrthogonalTiledMapGameObject):
                if command_target.orientation in {'left', 'right'}:
                    directions = ["up", "down", "left", "right"]

        # Start with a set of nodes consisting of the starting coordinates
        for start_coord in start_coords:
            start_node = PathfindingNode(None, start_coord, direction=None, g=0, override=False)
            start_node.h = self._coord_distance(start_node.coord, target.coord)
            open_list.add(start_node, start_node.f)
            closest_node = start_node

        while not open_list.empty():
            current_node = open_list.get()
            closed_set.add(current_node.coord)

            # Found the target, returns the path
            if current_node.coord == target_coord:
                return current_node.path[:-command.target_distance or None]
            elif (
                    command.target_distance > 0 and
                    self._coord_distance(current_node.coord, target_coord) <= command.target_distance):
                return current_node.path

            # search is too long, return best path
            if len(current_node.path) > command.max_path_length:
                break

            # Loop through children
            for child in self._generate_pathfinding_path_children(current_node, directions):
                if child.coord in closed_set:
                    continue

                if not child.override:
                    is_permitted = self.can_always_move or self.parent.base_grid.is_move_in_direction_permitted(
                        self.base_id, current_node.coord, child.direction, ignore_elements=command.ignore_elements)
                else:
                    is_permitted = (
                            self.can_always_move or
                            child.override_condition is None or
                            current_node.eval_override_condition(child.override_condition))

                if not is_permitted:
                    continue

                child.h = self._coord_distance(child.coord, target_coord)
                child.f = child.g + child.h

                if child.h < closest_node.h:
                    closest_node = child

                # If this is the cheapest way to get to the child coordinate, adds it to the open set.
                if child.coord not in coord_cost_dict or child.f < coord_cost_dict[child.coord]:
                    child.path.append(child.direction)
                    coord_cost_dict[child.coord] = child.f
                    open_list.add(child, child.f)
        return closest_node.path

    def can_move_in_direction(self, direction: str) -> bool:
        return self.can_always_move or self.parent.base_grid.is_move_in_direction_permitted(
            self.base_id, self.central_coord, direction)

    def can_move_ahead(self) -> bool:
        return self.can_always_move or self.parent.base_grid.is_move_in_direction_permitted(
            self.base_id, self.central_coord, self.orientation)

    @staticmethod
    def _coord_distance(coord, target) -> int:
        """
        The heuristics calculation for the pathfinding algorithm
        :param Coord coord:
        :param Coord target:
        """
        return abs(coord.x - target.x) + abs(coord.y - target.y)

    def command_go_random(self, command, gt, pop=True):
        """
        Executes a go_random command.

        :param ControlCommand command: The command being executed.
        :param float gt: The current game time in seconds
        :param bool pop: Whether or not to pop the top command on the command stack. Disabled if the move is
        part of a broader command.
        """
        directions = ["up", "down", "left", "right"]

        for coord in self.coords:
            if "right" in directions and coord.x >= command.max_x:
                directions.remove("right")
            if "left" in directions and coord.x <= command.min_x:
                directions.remove("left")
            if "down" in directions and coord.y >= command.max_y:
                directions.remove("down")
            if "up" in directions and coord.y <= command.min_y:
                directions.remove("up")

        if len(directions) == 0:
            # If no movement is permitted.
            self.finish_command(command)
        else:
            random_direction = random.choice(directions)

            if random_direction == "up":
                self.command_go_up(command, gt, pop=pop)
            elif random_direction == "down":
                self.command_go_down(command, gt, pop=pop)
            elif random_direction == "left":
                self.command_go_left(command, gt, pop=pop)
            if random_direction == "right":
                self.command_go_right(command, gt, pop=pop)

    def command_go_custom(self, command, gt):  # noqa
        """
        Executes and consumes a go_custom command. Causes the character to move a certain amount of pixels in both the
        x and y directions. Used for gridless movement.
        :param ControlCommand command: The command being executed.
        :param float gt: The current game time in seconds
        """
        move_by_x = command.move_by_x
        move_by_y = command.move_by_y
        if move_by_x != 0:
            move_x_to_y = float(move_by_y) / move_by_x
        else:
            move_x_to_y = 0.0

        # Variables that only have to be calculated once
        base_x_start = self.base_x_start
        base_x_end = self.base_x_end
        base_y_start = self.base_y_start
        base_y_end = self.base_y_end
        movement_speed = self.movement_speed

        # Coordinates at which object crosses a grid line.
        cross_coordinates = []

        if move_by_x > 0:
            # Right side of the base crosses grid lines first.
            start_x = self.parent.pixel_to_coord(base_x_end, is_x=True)
            end_x = self.parent.pixel_to_coord(base_x_end + move_by_x, is_x=True)

            previous_coord = Coord(base_x_start, base_y_start)
            base_width = self.base_width
            for x_coord in range(start_x, end_x):
                # crossing at x border x_coord x_coord + 1
                cross_x = ((x_coord + 1) * self.parent.tile_size.x) - base_width
                cross_y = previous_coord.y + floor((cross_x - previous_coord.x) * move_x_to_y)
                cross_coord = Coord(cross_x, cross_y)
                previous_coord = cross_coord
                cross_coordinates.append(cross_coord)
        elif move_by_x < 0:
            # Left side of the base crosses grid lines first.
            start_x = self.parent.pixel_to_coord(base_x_start, is_x=True)
            end_x = self.parent.pixel_to_coord(base_x_start + move_by_x, is_x=True)

            previous_coord = Coord(base_x_start, base_y_start)
            for x_coord in range(start_x, end_x, -1):
                # crossing at x border x_coord x_coord - 1
                cross_x = x_coord * self.parent.tile_size.x
                cross_y = previous_coord.y + floor((cross_x - previous_coord.x) * move_x_to_y)
                cross_coord = Coord(cross_x, cross_y)
                previous_coord = cross_coord
                cross_coordinates.append(cross_coord)

        if move_by_y > 0:
            # Bottom side of the base crossed grid lines first.
            start_y = self.parent.pixel_to_coord(base_y_end, is_x=False)
            end_y = self.parent.pixel_to_coord(base_y_end + move_by_y, is_x=False)

            previous_coord = Coord(base_x_start, base_y_start)
            base_height = self.base_height
            for y_coord in range(start_y, end_y):
                # crossing at y border y_coord y_coord - 1
                cross_y = ((y_coord + 1) * self.parent.tile_size.y) - base_height
                cross_x = previous_coord.x + floor((cross_y - previous_coord.y) / move_x_to_y)
                cross_coord = Coord(cross_x, cross_y)
                previous_coord = cross_coord
                if cross_coord not in cross_coordinates:
                    cross_coordinates.append(cross_coord)
        elif move_by_y < 0:
            # Top size of the base crosses grid lines first.
            start_y = self.parent.pixel_to_coord(base_y_start, is_x=False)
            end_y = self.parent.pixel_to_coord(base_y_start + move_by_y, is_x=False)

            previous_coord = Coord(base_x_start, base_y_start)
            for y_coord in range(start_y, end_y, -1):
                # crossing at y border y_coord y_coord + 1
                cross_y = (y_coord * self.parent.tile_size.y)
                cross_x = previous_coord.x + floor((cross_y - previous_coord.y) / move_x_to_y)
                cross_coord = Coord(cross_x, cross_y)
                previous_coord = cross_coord
                if cross_coord not in cross_coordinates:
                    cross_coordinates.append(cross_coord)

        # Sort crossing coordinates by distance
        if move_by_x > 0:
            cross_coordinates = sorted(cross_coordinates, key=lambda z: z[0])
        elif move_by_x < 0:
            cross_coordinates = sorted(cross_coordinates, key=lambda z: z[0], reverse=True)
        elif move_by_y > 0:
            cross_coordinates = sorted(cross_coordinates, key=lambda z: z[1])
        elif move_by_y < 0:
            cross_coordinates = sorted(cross_coordinates, key=lambda z: z[1], reverse=True)

        # Adds final, non-grid crossing, end coordinate
        final_coordinate = Coord(base_x_start + move_by_x, base_y_start + move_by_y)
        if final_coordinate not in cross_coordinates:
            cross_coordinates.append(final_coordinate)

        previous_coord = Coord(base_x_start, base_y_start)
        command_components = []
        for coordinate in cross_coordinates:
            comp_move_by_x = coordinate.x - previous_coord.x
            comp_move_by_y = coordinate.y - previous_coord.y
            if comp_move_by_x == 0 and comp_move_by_y == 0:
                continue

            # Seconds to cross a pixel horizontally
            horizontal_speed = movement_speed / self.parent.tile_size.x
            # Seconds to cross a pixel vertically
            vertical_speed = movement_speed / self.parent.tile_size.y

            horizontal_time = horizontal_speed * comp_move_by_x
            vertical_time = vertical_speed * comp_move_by_y

            # Seconds necessary for the movement
            diagonal_time = sqrt((horizontal_time * horizontal_time) + (vertical_time * vertical_time))

            command_component = ControlCommand(
                "custom_component", move_by_x=comp_move_by_x, move_by_y=comp_move_by_y,
                pop_invalid_move=command.pop_invalid_move, animate_invalid_move=command.animate_invalid_move,
                never_repeat=True, movement_time=diagonal_time)
            command_components.append(command_component)
            previous_coord = coordinate

        # Removes this command
        self.finish_command(command)

        # Adds component commands.
        for x in range(len(command_components)):
            self.control_stack.insert(x, command_components[x])

    def command_custom_component(self, command, gt):
        """
        Executes and consumes a custom_component command. Custom movements (non-grid movements) are split into these,
        with each custom component consisting of at most a single grid coordinate change.

        :param ControlCommand command: The command being executed.
        :param float gt: The current game time in seconds
        """
        # sets orientation
        self._current_command = command
        move_by_x = command.move_by_x
        move_by_y = command.move_by_y
        if abs(move_by_x) > abs(move_by_y):
            if move_by_x > 0:
                self._orientation = "right"
            else:
                self._orientation = "left"
        else:
            if move_by_y > 0:
                self._orientation = "down"
            elif move_by_y < 0:
                # This is elif rather than else to prevent turning if both move_by_x and move_by_y end up being 0 for
                # some reason.
                self._orientation = "up"

        # Check if permitted
        target_x = self.x + move_by_x
        target_y = self.y + move_by_y
        permitted_move = True
        if not (
                self.can_always_move or
                self.parent.base_grid.is_move_permitted(
                    self.base_id, target_x, target_y, ignore_elements=command.ignore_elements)):
            permitted_move = False

        # get movement_speed
        if command.movement_time is not None:
            movement_time = command.movement_time
        else:
            movement_time = self.movement_speed

        # Sets movement parameters
        if permitted_move:
            self.parent.base_grid.move_element(self.base_id, target_x, target_y)
            self._command_gt_start = gt
            self._command_gt_end = gt + movement_time
            self._command_x_start, self._command_y_start = self.x, self.y
            self._command_x_end = target_x
            self._command_y_end = target_y
            self._play_movement_sound(can_move=True)

            self._set_animation(self.move_animation)
            self.finish_command(command)
        else:
            self._play_movement_sound(can_move=False)
            self._command_gt_start = gt
            self._command_gt_end = gt + self.movement_speed
            if command.animate_invalid_move:
                self._set_animation(self.move_animation)
            else:
                self._set_animation(self.stand_animation)
            if command.pop_invalid_move:
                self.finish_command(command)

    def command_go_to_custom(self, command, gt):  # noqa
        """
        Executes and consumes a go_custom command. Causes the character to move the top-left coordinate of their
        base to a given pixel.
        :param ControlCommand command: The command being executed.
        :param float gt: The current game time in seconds
        """
        target = command.target
        move_by_x = target[0] - self.base_x_start
        move_by_y = target[1] - self.base_y_end

        go_to_command = ControlCommand(
            "go_custom", move_by_x=move_by_x, move_by_y=move_by_y,
            pop_invalid_move=command.pop_invalid_move, animate_invalid_move=command.animate_invalid_move,
            never_repeat=True)
        self.finish_command(command)
        self.control_stack.insert(0, go_to_command)

    def command_play_animation(self, command, gt):
        """
        Executes and consumes a 'play_animation' command, which causes a single animation sequence for the current
        sprite collection to play in full. The next command isn't executed until the animation is finished playing.

        :param ControlCommand command: The command being executed.
        :param float gt: The current game time in seconds
        """
        self._current_command = command

        if command.animation_speed is not None:
            self._set_animation(command.animation_name, speed=command.animation_speed)
        else:
            self._set_animation(command.animation_name)

        animation_duration = (
                (len(self.sprite_collection.current_animation.images) * self.sprite_collection.current_speed) - 0.05
        )
        # The 0.05 is for situations wherein multiple animations/animation changes are placed after each other,
        # preventing the tiny frame of stand/move animation that would otherwise occur between these.

        self._command_gt_start = gt
        self._command_gt_end = gt + animation_duration

        self.finish_command(command)

    def command_change_stand_animation(self, command, gt):
        """
        Executes and consumes a 'change_stand_animation' command, which changes the stand animation for this object.

        :param ControlCommand command: The command being executed.
        :param float gt: The current game time in seconds
        """
        self._current_command = command

        currently_standing = False
        if self.current_animation_name == self.stand_animation:
            currently_standing = True

        self.stand_animation = command.animation_name

        if currently_standing:
            self._set_animation(self.stand_animation)

        self._command_gt_start = gt
        self._command_gt_end = gt

        self.finish_command(command)

    def command_change_move_animation(self, command, gt):
        """
        Executes and consumes a 'change_move_animation' command, which changes the move animation for this object.

        :param ControlCommand command: The command being executed.
        :param float gt: The current game time in seconds
        """
        self._current_command = command

        currently_moving = False
        if self.current_animation_name == self.move_animation:
            currently_moving = True
        self.move_animation = command.animation_name
        if currently_moving:
            self._set_animation(self.move_animation)

        if self is self.parent.player_object:
            for follower in renpy.store.pink_otm_followers:
                if follower.current_animation_name == follower.move_animation:
                    currently_moving = True
                follower.move_animation = command.animation_name
                if currently_moving:
                    follower._set_animation(follower.move_animation)   # noqa

        self._command_gt_start = gt
        self._command_gt_end = gt

        self.finish_command(command)

    def command_special_move(self, command, gt):
        """
        Executes and consumes a 'special_move' command, used to have special movement on special blocks. Special moves
        ignore conventional movement rules, and can have any x or y.

        :param ControlCommand command: The command being executed.
        :param float gt: The current game time in seconds
        """
        self._current_command = command

        if command.movement_time is not None:
            movement_time = command.movement_time
        else:
            movement_time = self.movement_speed

        self._command_gt_start = gt
        self._command_gt_end = gt + movement_time
        self._command_x_start, self._command_y_start = self.x, self.y

        renpy.store.pink_sound_manager.play_sound(
            sound_file=command.path,
            emitter=self,
            pan=command.pan_sound,
            scale=command.scale_sound,
            max_volume_distance=command.max_volume_distance,
            min_volume_distance=command.min_volume_distance,
            min_volume=command.min_volume,
            max_volume=command.max_volume,
            max_pan_distance=command.max_pan_distance,
            no_pan_distance=command.no_pan_distance,
            max_pan=command.max_pan,
            mixer=command.mixer)

        if command.orientation:
            self._orientation = command.orientation

        target_x = self.x + command.move_by_x
        target_y = self.y + command.move_by_y

        self.prev_coord = self.central_coord
        self.parent.base_grid.move_element(self.base_id, target_x, target_y)
        self._set_animation(self.move_animation)
        self._command_x_end = target_x
        self._command_y_end = target_y
        self._command_arc_height = command.arc_height

        self.finish_command(command)

    @property
    def height(self):
        """
        :return: This object's image height in pixel
        :rtype: int
        """
        return self.sprite_collection.height

    @property
    def width(self):
        """
        :return: This object's image width in pixel
        :rtype: int
        """
        return self.sprite_collection.width

    @property
    def base_offset_x_start(self):
        """
        :return: The x offset of the start of the object's base (where the object begins for mapping and event
        purposes in relation to where the image of the object begins)
        :rtype: int
        """
        if "base_offset_x_start" in self.sprite_collection.current_animation.properties:
            return floor(self.sprite_collection.current_animation.properties["base_offset_x_start"] * self.xzoom)
        else:
            return 0

    @property
    def base_offset_x_end(self):
        """
        :return: The x offset of the end of the object's base (where the object ends for mapping and event
        purposes in relation to where the image of the object begins)
        :rtype: int
        """
        if "base_offset_x_end" in self.sprite_collection.current_animation.properties:
            return floor(self.sprite_collection.current_animation.properties["base_offset_x_end"] * self.xzoom)
        else:
            return self.sprite_collection.current_animation.image_width

    @property
    def base_offset_y_start(self):
        """
        :return: The y offset of the start of the object's base (where the object begins for mapping and event
        purposes in relation to where the image of the object begins)
        :rtype: int
        """
        if "base_offset_y_start" in self.sprite_collection.current_animation.properties:
            return floor(self.sprite_collection.current_animation.properties["base_offset_y_start"] * self.yzoom)
        else:
            return 0

    @property
    def base_offset_y_end(self):
        """
        :return: The y offset of the end of the object's base (where the object ends for mapping and event
        purposes in relation to where the image of the object begins)
        :rtype: int
        """
        if "base_offset_y_end" in self.sprite_collection.current_animation.properties:
            return floor(self.sprite_collection.current_animation.properties["base_offset_y_end"] * self.yzoom)
        else:
            return self.sprite_collection.current_animation.image_height

    @property
    def move_from(self):
        """
        :return: The movement allowed from a square occupied by this object.
        :rtype: str|None
        """
        if self.hidden:
            return "1111"
        elif "move_from" in self.properties:
            return self.properties["move_from"]
        elif "move_from" in self.sprite_collection.current_animation.properties:
            return self.sprite_collection.current_animation.properties["move_from"]
        else:
            return None

    @property
    def move_to(self):
        """
        :return: The movement allowed to a square occupied by this object.
        :rtype: str|None
        """
        if self.hidden:
            return "1111"
        elif "move_to" in self.properties:
            return self.properties["move_to"]
        elif "move_to" in self.sprite_collection.current_animation.properties:
            return self.sprite_collection.current_animation.properties["move_to"]
        else:
            return None

    @property
    def forbid_autocenter(self):
        """
        :return: Whether autocenter settings should be overwritten for this sprite collection.
        :rtype: bool
        """
        if 'forbid_autocenter' in self.properties:
            return self.properties['forbid_autocenter']
        else:
            return False


OrthogonalTiledMapGameObjectSpriteCollection.movement_commands = OrthogonalTiledMapGameObjectMobile.movement_commands.copy()  # noqa
OrthogonalTiledMapGameObjectSpriteCollection.movement_commands.update({
    "delay": OrthogonalTiledMapGameObjectSpriteCollection.command_delay,
    "go_to": OrthogonalTiledMapGameObjectSpriteCollection.command_go_to,
    "go_to_smart": OrthogonalTiledMapGameObjectSpriteCollection.command_go_to_smart,
    "go_left": OrthogonalTiledMapGameObjectSpriteCollection.command_go_left,
    "go_right": OrthogonalTiledMapGameObjectSpriteCollection.command_go_right,
    "go_up": OrthogonalTiledMapGameObjectSpriteCollection.command_go_up,
    "go_down": OrthogonalTiledMapGameObjectSpriteCollection.command_go_down,
    "go_random": OrthogonalTiledMapGameObjectSpriteCollection.command_go_random,
    "go_custom": OrthogonalTiledMapGameObjectSpriteCollection.command_go_custom,
    "custom_component": OrthogonalTiledMapGameObjectSpriteCollection.command_custom_component,
    "go_to_custom": OrthogonalTiledMapGameObjectSpriteCollection.command_go_to_custom,
    "turn_left": OrthogonalTiledMapGameObjectSpriteCollection.command_turn_left,
    "turn_right": OrthogonalTiledMapGameObjectSpriteCollection.command_turn_right,
    "turn_up": OrthogonalTiledMapGameObjectSpriteCollection.command_turn_up,
    "turn_down": OrthogonalTiledMapGameObjectSpriteCollection.command_turn_down,
    "turn_clockwise": OrthogonalTiledMapGameObjectSpriteCollection.command_turn_clockwise,
    "turn_counter_clockwise": OrthogonalTiledMapGameObjectSpriteCollection.command_turn_counter_clockwise,
    "turn_random": OrthogonalTiledMapGameObjectSpriteCollection.command_turn_random,
    "turn_to": OrthogonalTiledMapGameObjectSpriteCollection.command_turn_to,
    "play_animation": OrthogonalTiledMapGameObjectSpriteCollection.command_play_animation,
    "change_stand_animation": OrthogonalTiledMapGameObjectSpriteCollection.command_change_stand_animation,
    "change_move_animation": OrthogonalTiledMapGameObjectSpriteCollection.command_change_move_animation,
    "special_move": OrthogonalTiledMapGameObjectSpriteCollection.command_special_move
})


class OrthogonalTiledMapTiledBasesEntry(object):
    def __init__(self, parent_map, element_id, x, y, layer, game_object):
        """
        A single object's base.
        :param OrthogonalTiledMap parent_map: The game map this base is a part of.
        :param int element_id: The element id of this base. Should be the same as the displayable id for the object
        this is the base of, if this base is linked to an object. If not, this id should be negative.
        :param int x: Distance in pixels between this base's object's left side and the left border of the map.
        :param int y: Distance in pixels between this base's object's top side and the top border of the map.
        :param TiledMapGameLayer layer: The later this object is placed on
        :param OrthogonalTiledMapGameObjectBase game_object: The game object this is the base of
        """
        self.parent = parent_map
        self.game_object = game_object
        self.element_id = element_id

        self.base_x_start = x + game_object.base_offset_x_start
        self.base_y_start = y + game_object.base_offset_y_start + game_object.arc_y_offset
        self.base_x_end = x + game_object.base_offset_x_end
        self.base_y_end = y + game_object.base_offset_y_end + game_object.arc_y_offset

        self.base_priority = (LAYER_PRIORITY[layer.layer_type], layer.z_order, self.element_id)

    def recalculate_base(self, new_x, new_y):
        """
        Recalculates this base for a new x and y
        :param int new_x: The new distance in pixels between this base's object's left side and the left border of the
        map.
        :param int new_y: The new distance in pixels between this base's object's top side and the top border of the
        map.
        """
        self.base_x_start = new_x + self.game_object.base_offset_x_start
        self.base_y_start = new_y + self.game_object.base_offset_y_start + self.game_object.arc_y_offset
        self.base_x_end = new_x + self.game_object.base_offset_x_end
        self.base_y_end = new_y + self.game_object.base_offset_y_end + self.game_object.arc_y_offset

    def get_base_columns(self):
        """
        :return: The range of indexes of columns this base intersects.
        :rtype: range
        """
        start_x_coord = floor(self.base_x_start / self.parent.tile_size.x)  # BASE NO WORK FOR TILE.
        end_x_coord = floor((self.base_x_end - 1) / self.parent.tile_size.x)  # BASE NO WORK FOR TILE.
        return range(start_x_coord, end_x_coord + 1)  # BASE NO WORK FOR TILE.

    def get_base_rows(self):
        """
        :return: The range of indexes of rows this base intersects.
        :rtype: range
        """
        start_y_coord = floor(self.base_y_start / self.parent.tile_size.y)
        end_y_coord = floor((self.base_y_end - 1) / self.parent.tile_size.y)
        return range(start_y_coord, end_y_coord + 1)

    @property
    def central_coord(self):
        """
        :return: The coordinate covered by the center of this object's base.
        :rtype: Coord
        """
        x_coord = floor(((self.base_x_start + self.base_x_end - 1) / 2) / self.parent.tile_size.x)
        y_coord = floor(((self.base_y_start + self.base_y_end - 1) / 2) / self.parent.tile_size.y)

        return Coord(x_coord, y_coord)

    @property
    def upper_left_coord(self):
        """
        :return: The map coordinate at which the upper left corner of this base resides.
        :rtype: Coord
        """
        x_coord = floor(self.base_x_start / self.parent.tile_size.x)
        y_coord = floor(self.base_y_start / self.parent.tile_size.y)

        return Coord(x_coord, y_coord)

    @property
    def upper_coord(self):
        """
        :return: The map coordinate at which the exact middle of the upper end of this base resides.
        :rtype: Coord
        """
        x_coord = floor(((self.base_x_start + self.base_x_end - 1) / 2) / self.parent.tile_size.x)
        y_coord = floor(self.base_y_start / self.parent.tile_size.y)

        return Coord(x_coord, y_coord)

    @property
    def upper_right_coord(self):
        """
        :return: The map coordinate at which the upper right corner of this base resides.
        :rtype: Coord
        """
        x_coord = floor((self.base_x_end - 1) / self.parent.tile_size.x)
        y_coord = floor(self.base_y_start / self.parent.tile_size.y)

        return Coord(x_coord, y_coord)

    @property
    def right_coord(self):
        """
        :return: The map coordinate at which the exact middle of the right end of this base resides.
        :rtype: Coord
        """
        x_coord = floor((self.base_x_end - 1) / self.parent.tile_size.x)
        y_coord = floor(((self.base_y_start + self.base_y_end - 1) / 2) / self.parent.tile_size.y)

        return Coord(x_coord, y_coord)

    @property
    def lower_right_coord(self):
        """
        :return: The map coordinate at which the lower right corner of this base resides.
        :rtype: Coord
        """
        x_coord = floor((self.base_x_end - 1) / self.parent.tile_size.x)
        y_coord = floor((self.base_y_end - 1) / self.parent.tile_size.y)

        return Coord(x_coord, y_coord)

    @property
    def lower_coord(self):
        """
        :return: The map coordinate at which the exact middle of the bottom end of this base resides.
        :rtype: Coord
        """
        x_coord = floor(((self.base_x_start + self.base_x_end - 1) / 2) / self.parent.tile_size.x)
        y_coord = floor((self.base_y_end - 1) / self.parent.tile_size.y)

        return Coord(x_coord, y_coord)

    @property
    def lower_left_coord(self):
        """
        :return: The map coordinate at which the lower left corner of this base resides.
        :rtype: Coord
        """
        x_coord = floor(self.base_x_start / self.parent.tile_size.x)
        y_coord = floor((self.base_y_end - 1) / self.parent.tile_size.y)

        return Coord(x_coord, y_coord)

    @property
    def left_coord(self):
        """
        :return: The map coordinate at which the exact middle of the left end of this base resides.
        :rtype: Coord
        """
        x_coord = floor(self.base_x_start / self.parent.tile_size.x)
        y_coord = floor(((self.base_y_start + self.base_y_end - 1) / 2) / self.parent.tile_size.y)

        return Coord(x_coord, y_coord)

    @property
    def start_x_coord(self):
        """
        :return: The first X coordinate covered by this base
        :rtype: int
        """
        return floor(self.base_x_start / self.parent.tile_size.x)

    @property
    def end_x_coord(self):
        """
        :return: The last X coordinate covered by this base
        :rtype: int
        """
        return floor((self.base_x_end - 1) / self.parent.tile_size.x)

    @property
    def start_y_coord(self):
        """
        :return: The first Y coordinate covered by this base
        :rtype: int
        """
        return floor(self.base_y_start / self.parent.tile_size.y)

    @property
    def end_y_coord(self):
        """
        :return: The last Y coordinate covered by this base
        :rtype: int
        """
        return floor((self.base_y_end - 1) / self.parent.tile_size.y)

    @property
    def coords(self):
        """
        :return: The list of coordinates covered by this object's base.
        :rtype: list
        """
        coords = []
        for x in range(self.start_x_coord, self.end_x_coord + 1):
            for y in range(self.start_y_coord, self.end_y_coord + 1):
                coords.append(Coord(x, y))

        return coords


class OrthogonalTiledMapTiledBases(object):
    def __init__(self, game_object, x_dim, y_dim):
        """
        The structured collection of bases for an orthogonal tiled map
        :param OrthogonalTiledMap game_object: The game map this is the base collection of.
        :param int x_dim: The width in pixels of the map.
        :param int y_dim: The height in pixels of the map.
        """
        self.game_object = game_object

        # Creates a grid for all objects, to more efficiently check for objects that might be in your way.
        self.base_grid = []
        self.base_grid_x_size = x_dim
        self.base_grid_y_size = y_dim
        for x in range(self.base_grid_x_size):
            self.base_grid.append([])
            for y in range(self.base_grid_y_size):
                self.base_grid[x].append({})

        # Index of all bases
        self._next_id = -1  # type: int
        self.map_elements = {}

    def get_next_id(self):
        """
        :return: The next ID that should be given to a tile.
        :rtype: int
        """
        next_id = self._next_id
        self._next_id -= 1
        return next_id

    def add_element(self, x, y, layer, game_object):
        """
        Adds the base for the given game_object to this collection.
        :param int x: Distance in pixels between the object's left side and the left border of the map.
        :param int y: Distance in pixels between the object's top side and the top border of the map.
        :param TiledMapGameLayer layer: The layer the object is placed on
        :param OrthogonalTiledMapGameTile|OrthogonalTiledMapGameObject game_object:
        """
        element_id = self.get_next_id()
        if game_object.single_display:
            game_object.base_id = element_id

        new_element = OrthogonalTiledMapTiledBasesEntry(self.game_object, element_id, x, y, layer, game_object)
        self.map_elements[element_id] = new_element

        self.add_to_grid(new_element)

    def remove_element(self, element_id):
        """
        Removes the element with the given id.
        :param int element_id: The given id
        """
        element = self.map_elements.get(element_id)

        self.remove_from_grid(element)

        if element.game_object.single_display:
            element.game_object.base_id = None

    def add_to_grid(self, element):
        """
        Adds the given base to this collection
        :param OrthogonalBaseEntry element: The given base
        """
        for column in element.get_base_columns():
            for row in element.get_base_rows():
                if 0 <= row < self.base_grid_y_size and 0 <= column < self.base_grid_x_size:
                    self.base_grid[column][row][element.base_priority] = element

    def remove_from_grid(self, element):
        """
        Removes the given base from this collection
        :param OrthogonalBaseEntry element: the given base
        """
        for column in element.get_base_columns():
            for row in element.get_base_rows():
                if 0 <= row < self.base_grid_y_size and 0 <= column < self.base_grid_x_size:
                    self.base_grid[column][row].pop(element.base_priority)

    def move_element(self, element_id, new_x, new_y):
        """
        Moves the element with the given id to the given x and y
        :param int element_id: the given element id
        :param int new_x: the given x
        :param int new_y: the given y
        """
        element = self.map_elements[element_id]
        self.remove_from_grid(element)
        element.recalculate_base(new_x, new_y)
        self.add_to_grid(element)

    def get_top_base_with_property(
            self, base_property, x_coord, y_coord, ignore_elements=None, default_value=None,
            additional_requirements=None
    ):
        """
        For the given property name, retrieves the value of the highest base where the value is set, and which
        intersects with the given coordinate.
        :param str base_property: The given property name
        :param int x_coord: The given x coordinate
        :param int y_coord: The given y coordinate
        :param list ignore_elements: Ignore these elements in the retrieval process (used to prevent objects
        from preventing their own movement and such)
        :param list additional_requirements:
        :param default_value: The value that should be returned if no object whose base intersects with the given
        coordinates has the given property set.
        """
        try:
            objects_at_coord = self.base_grid[x_coord][y_coord].copy()
        except IndexError:
            return default_value, None

        # Removes ignored element
        if ignore_elements is not None:
            for ignore_element in ignore_elements:
                ignore_base_priority = ignore_element.base_priority
                if ignore_base_priority in objects_at_coord:
                    objects_at_coord.pop(ignore_base_priority)

        # Gets property
        matching_property = None
        corresponding_object = None
        for base_object_priority in sorted(objects_at_coord.keys(), reverse=True):
            base_object = objects_at_coord[base_object_priority]
            if additional_requirements is not None:
                additional_requirements_met = True

                for additional_requirement in additional_requirements:
                    if not getattr(base_object.game_object, additional_requirement):
                        additional_requirements_met = False
                        break

                if not additional_requirements_met:
                    break

            base_object_property = getattr(base_object.game_object, base_property)
            if base_object_property is not None:
                corresponding_object = base_object.game_object
                matching_property = base_object_property
                break

        # If no rules are found:
        if matching_property is None:
            matching_property = default_value

        return matching_property, corresponding_object

    def get_activation_event(self, x_coord, y_coord, ignore_element=None):
        """
        Retrieves the name of the event to activate upon interaction with the given coordinate.
        :param int x_coord: The x of the given coordinate
        :param int y_coord: The y of the given coordinate
        :param ignore_element: Which element to ignore while figuring out the activation event.
        :rtype: str|None
        """
        return self.get_top_base_with_property(
            'event_on_activate', x_coord, y_coord, ignore_elements=[ignore_element],
            additional_requirements=['event_conditional_met'])

    def get_touch_event(self, x_coord, y_coord, ignore_element=None):
        """
        Retrieves the name of the event to activate upon touching the given coordinate.
        :param int x_coord: The x of the given coordinate
        :param int y_coord: The y of the given coordinate
        :param ignore_element: Which element to ignore while figuring out the touch event.
        :rtype: str|None
        """
        return self.get_top_base_with_property(
            'event_on_touch', x_coord, y_coord, ignore_elements=[ignore_element],
            additional_requirements=['event_conditional_met'])

    def get_activation_code(self, x_coord, y_coord, ignore_element=None):
        """
        Retrieves the code to run upon interaction with the given coordinate.
        :param int x_coord: The x of the given coordinate
        :param int y_coord: The y of the given coordinate
        :param ignore_element: Which element to ignore while retrieving the code
        :rtype: str|None
        """
        return self.get_top_base_with_property(
            'code_on_activate', x_coord, y_coord, ignore_elements=[ignore_element],
            additional_requirements=['code_conditional_met'])

    def get_touch_code(self, x_coord, y_coord, ignore_element=None):
        """
        Retrieves the code to run upon touching the given coordinate.
        :param int x_coord: The x of the given coordinate
        :param int y_coord: The y of the given coordinate
        :param ignore_element: Which element to ignore while retrieving the code
        :rtype: str|None
        """
        return self.get_top_base_with_property(
            'code_on_touch', x_coord, y_coord, ignore_elements=[ignore_element],
            additional_requirements=['code_conditional_met'])

    def get_override_go_right(self, x_coord, y_coord):
        """
        Retrieves the movement override code for going right on the given coordinate.
        :param int x_coord: the x of the given coordinate.
        :param int y_coord: the y of the given coordinate.
        :rtype: str|None
        """
        return self.get_top_base_with_property('override_go_right', x_coord, y_coord)[0]

    def get_override_go_left(self, x_coord, y_coord):
        """
        Retrieves the movement override code for going left on the given coordinate.
        :param int x_coord: the x of the given coordinate.
        :param int y_coord: the y of the given coordinate.
        :rtype: str|None
        """
        return self.get_top_base_with_property('override_go_left', x_coord, y_coord)[0]

    def get_override_go_up(self, x_coord, y_coord):
        """
        Retrieves the movement override code for going up on the given coordinate.
        :param int x_coord: the x of the given coordinate.
        :param int y_coord: the y of the given coordinate.
        :rtype: str|None
        """
        return self.get_top_base_with_property('override_go_up', x_coord, y_coord)[0]

    def get_override_go_down(self, x_coord, y_coord):
        """
        Retrieves the movement override code for going down on the given coordinate.
        :param int x_coord: the x of the given coordinate.
        :param int y_coord: the y of the given coordinate.
        :rtype: str|None
        """
        return self.get_top_base_with_property('override_go_down', x_coord, y_coord)[0]

    def get_override_go_direction(self, x_coord, y_coord, direction):
        """
        Retrieves the movement override code for going down on the given coordinate for the given direction
        :param int x_coord: the x of the given coordinate.
        :param int y_coord: the y of the given coordinate.
        :param str direction: the direction to check
        :rtype: str|None
        """
        return self.get_top_base_with_property(f'override_go_{direction}', x_coord, y_coord)[0]

    def get_override_condition_direction(self, x_coord, y_coord, direction):
        """
        Retrieves the condition for overriding going right on the given coordinate for the given direction
        :param int x_coord: the x of the given coordinate.
        :param int y_coord: the y of the given coordinate.
        :param str direction: the direction to check
        :rtype: str|None
        """
        return self.get_top_base_with_property(f'override_go_{direction}_condition', x_coord, y_coord)[0]

    def get_override_smart_coords(self, x_coord, y_coord, direction) -> List[Coord]:
        """
        Retrieves the coordinate that the overriding move will result in. Used for calculating routes for smart
        movement.
        """
        offsets = self.get_top_base_with_property(f'override_go_{direction}_coord_offsets', x_coord, y_coord)[0]

        if offsets is None:
            base_coord = Coord(x_coord, y_coord)
            return [getattr(base_coord, direction)]
        else:
            return [Coord(x_coord + offset[0], y_coord + offset[1]) for offset in offsets]

    def get_override_smart_g_increment(self, x_coord, y_coord, direction):
        """
        Retrieves the amount of moves that the overriding move should be considered to take for the purposes of smart
        movement.
        :rtype: float
        """
        g_inc = self.get_top_base_with_property(f'override_go_{direction}_g_inc', x_coord, y_coord)[0]
        if g_inc is None:
            return 1.0
        else:
            return g_inc

    def get_override_go_right_condition(self, x_coord, y_coord):
        """
        Retrieves the condition for overriding going right on the given coordinate.
        :param int x_coord: the x of the given coordinate.
        :param int y_coord: the y of the given coordinate.
        :rtype: str|None
        """
        return self.get_top_base_with_property('override_go_right_condition', x_coord, y_coord)[0]

    def get_override_go_left_condition(self, x_coord, y_coord):
        """
        Retrieves the condition for overriding going left on the given coordinate.
        :param int x_coord: the x of the given coordinate.
        :param int y_coord: the y of the given coordinate.
        :rtype: str|None
        """
        return self.get_top_base_with_property('override_go_left_condition', x_coord, y_coord)[0]

    def get_override_go_up_condition(self, x_coord, y_coord):
        """
        Retrieves the condition for overriding going upwards on the given coordinate.
        :param int x_coord: the x of the given coordinate.
        :param int y_coord: the y of the given coordinate.
        :rtype: str|None
        """
        return self.get_top_base_with_property('override_go_up_condition', x_coord, y_coord)[0]

    def get_override_go_down_condition(self, x_coord, y_coord):
        """
        Retrieves the condition for overriding going down on the given coordinate.
        :param int x_coord: the x of the given coordinate.
        :param int y_coord: the y of the given coordinate.
        :rtype: str|None
        """
        return self.get_top_base_with_property('override_go_down_condition', x_coord, y_coord)[0]

    def get_override_go_direction_condition(self, x_coord, y_coord, direction):
        """
        Retrieves the movement override code for going down on the given coordinate for the given direction
        :param int x_coord: the x of the given coordinate.
        :param int y_coord: the y of the given coordinate.
        :param str direction: the direction to check
        :rtype: str|None
        """
        return self.get_top_base_with_property(f'override_go_{direction}_condition', x_coord, y_coord)[0]

    def get_move_to(self, x_coord, y_coord):
        """
        Retrieves the movement rules for entering the given coordinate.
        :param int x_coord: the x of the given coordinate.
        :param int y_coord: the y of the given coordinate.
        :rtype: str|None
        """
        return self.get_top_base_with_property('move_to', x_coord, y_coord)[0]

    def get_sound_tag(self, x_coord, y_coord):
        """
        Retrieves the sound tag for the given coordinate.
        :param int x_coord: the x of the given coordinate.
        :param int y_coord: the y of the given coordinate.
        :rtype: str|None
        """
        return self.get_top_base_with_property('sound_tag', x_coord, y_coord)[0]

    def base_to_coords(self, base_x_start, base_x_end, base_y_start, base_y_end):
        """
        :param int base_x_start: The distance in pixels between the left side of the base and the left border of the
        map.
        :param int base_x_end: The distance in pixels between the right side of the base and the left border of the
        map.
        :param int base_y_start: The distance in pixels between the top side of the base and the upper border of the
        map.
        :param int base_y_end: The distance in pixels between the bottom side of the base and the upper border of the
        map.
        :return: The list of coordinates that a base with the given start and end pixels would occupy.
        :rtype: list
        """
        start_x_coord = floor(base_x_start / self.game_object.tile_size.x)
        end_x_coord = floor((base_x_end - 1) / self.game_object.tile_size.x)
        start_y_coord = floor(base_y_start / self.game_object.tile_size.y)
        end_y_coord = floor((base_y_end - 1) / self.game_object.tile_size.y)

        coords = []
        for x in range(start_x_coord, end_x_coord + 1):
            for y in range(start_y_coord, end_y_coord + 1):
                coords.append(Coord(x, y))

        return coords

    def _check_movement_straight(self, old_coords, new_coords, ignore_elements, relevant_from_side, relevant_to_side):
        """
        :param list old_coords: list of old coordinate tuples
        :param list new_coords: list of new coordinate tuples
        :param list ignore_elements: list of objects to ignore (used to make objects not stand in the way of their
        own movement, or be able to move onto the player's square)
        :param int relevant_from_side: The index of the movement rule to look at for the movement from the
         old tile. (0 is top, 1 is right, 2 is bottom, 3 is left)
        :param int relevant_to_side: The index of the movement rule to look at for the movement to the
         new tile. (0 is top, 1 is right, 2 is bottom, 3 is left)
        :return: Whether or not straight movement between the given set of old coordinates and the given set of new
        coordinates would be allowed.
        :rtype: bool
        """
        for x, y in old_coords:
            from_rules, rules_object = self.get_top_base_with_property(
                'move_from', x, y, ignore_elements=ignore_elements, default_value='1111')
            if from_rules[relevant_from_side] == "0":
                return False
        for x, y in new_coords:
            to_rules, rules_object = self.get_top_base_with_property(
                'move_to', x, y, ignore_elements=ignore_elements, default_value='0000')
            if to_rules[relevant_to_side] == "0":
                return False
        return True

    def _check_movement_diagonal(self, old_coords, new_coords, ignore_elements, relevant_from_sides, relevant_to_sides):
        """
        :param list old_coords: list of old coordinate tuples
        :param list new_coords: list of new coordinate tuples
        :param list ignore_elements: list of objects to ignore (used to make objects not stand in the way of their
        own movement, or be able to move onto the player's square)
        :param list relevant_from_sides: The indices of the movement rule to look at for the movement from the
         old tile. (0 is top, 1 is right, 2 is bottom, 3 is left)
        :param list relevant_to_sides: The indices of the movement rule to look at for the movement to the
         new tile. (0 is top, 1 is right, 2 is bottom, 3 is left)
        :return: Whether or not diagonal movement between the given set of old coordinates and the given set of new
        coordinates would be allowed.
        :rtype: bool
        """
        for x, y in old_coords:
            from_rules, rules_object = self.get_top_base_with_property(
                'move_from', x, y, ignore_elements=ignore_elements, default_value='1111')
            for relevant_from_side in relevant_from_sides:
                if from_rules[relevant_from_side] == "0":
                    return False
        for x, y in new_coords:
            to_rules, rules_object = self.get_top_base_with_property(
                'move_to', x, y, ignore_elements=ignore_elements, default_value='0000')
            for relevant_to_side in relevant_to_sides:
                if to_rules[relevant_to_side] == "0":
                    return False
        return True

    def is_move_in_direction_permitted(self, element_id, old_coord, direction, ignore_elements=None):
        """
        Retrieves whether a movement from the given coordinate in the given direction is permitted for the object
        with the given element id.
        :param int element_id: The element id of the object for which to assess whether movement is permitted.
        :param Coord old_coord: The coordinate from which the moving is done.
        :param str direction: The direction in which the moving is done.
        :param list|None ignore_elements: The list of objects to ignore during the assessment of movement rules.
        :rtype: bool
        """
        ignore_map_elements = [self.map_elements[element_id]]
        if ignore_elements is not None:
            for ignore_id in ignore_elements:
                ignore_id = 'renpy.store.' + ignore_id
                ignore_object = eval(ignore_id)
                try:
                    ignore_map_elements.append(self.map_elements[ignore_object.base_id])
                except (KeyError, AttributeError):
                    continue

        if direction == "right":
            new_coord = Coord(old_coord.x + 1, old_coord.y)
            return self._check_movement_straight(
                [old_coord], [new_coord], ignore_elements=ignore_map_elements, relevant_from_side=1, relevant_to_side=3)
        elif direction == "left":
            new_coord = Coord(old_coord.x - 1, old_coord.y)
            return self._check_movement_straight(
                [old_coord], [new_coord], ignore_elements=ignore_map_elements, relevant_from_side=3, relevant_to_side=1)
        elif direction == "up":
            new_coord = Coord(old_coord.x, old_coord.y - 1)
            return self._check_movement_straight(
                [old_coord], [new_coord], ignore_elements=ignore_map_elements, relevant_from_side=0, relevant_to_side=2)
        elif direction == "down":
            new_coord = Coord(old_coord.x, old_coord.y + 1)
            return self._check_movement_straight(
                [old_coord], [new_coord], ignore_elements=ignore_map_elements, relevant_from_side=2, relevant_to_side=0)

    def is_move_permitted(self, element_id, new_x, new_y, ignore_elements=None):
        """
        :param int element_id: The id of the object for which to check.
        :param int new_x: the given new x
        :param int new_y: the given new y
        :param list ignore_elements: List of elements to ignore.
        :return: whether or not the base with the given ID is allowed to move to the given x and y.
        :rtype: bool
        """
        element = self.map_elements[element_id]

        ignore_map_elements = [element]
        if ignore_elements is not None:
            for ignore_id in ignore_elements:
                ignore_id = 'renpy.store.' + ignore_id
                ignore_object = eval(ignore_id)
                try:
                    ignore_map_elements.append(self.map_elements[ignore_object.base_id])
                except (KeyError, AttributeError):
                    continue

        x_diff = new_x - element.game_object.x
        y_diff = new_y - element.game_object.y
        old_coords = element.coords
        new_coords = self.base_to_coords(
            element.base_x_start + x_diff, element.base_x_end + x_diff, element.base_y_start + y_diff,
            element.base_y_end + y_diff)

        # Moving outside the map is always illegal
        for new_x, new_y in new_coords:
            if new_x < 0 or new_x > self.game_object.grid_size.x - 1:
                return False
            if new_y < 0 or new_y > self.game_object.grid_size.y - 1:
                return False

        x_coord_diff = new_coords[0].x - old_coords[0].x
        y_coord_diff = new_coords[0].y - old_coords[0].y

        # moving within your current coordinate is always permitted
        if x_coord_diff == 0 and y_coord_diff == 0:
            return True

        # Checking movement for coordinates
        if x_coord_diff > 0 and y_coord_diff == 0:  # right
            return self._check_movement_straight(
                old_coords, new_coords, ignore_elements=ignore_map_elements, relevant_from_side=1, relevant_to_side=3)
        elif x_coord_diff < 0 and y_coord_diff == 0:  # left
            return self._check_movement_straight(
                old_coords, new_coords, ignore_elements=ignore_map_elements, relevant_from_side=3, relevant_to_side=1)
        elif x_coord_diff == 0 and y_coord_diff < 0:  # up
            return self._check_movement_straight(
                old_coords, new_coords, ignore_elements=ignore_map_elements, relevant_from_side=0, relevant_to_side=2)
        elif x_coord_diff == 0 and y_coord_diff > 0:  # down
            return self._check_movement_straight(
                old_coords, new_coords, ignore_elements=ignore_map_elements, relevant_from_side=2, relevant_to_side=0)
        elif x_coord_diff > 0 and y_coord_diff > 0:  # right-down
            return self._check_movement_diagonal(
                old_coords, new_coords, ignore_elements=ignore_map_elements, relevant_from_sides=[1, 2],
                relevant_to_sides=[3, 0])
        elif x_coord_diff > 0 and y_coord_diff < 0:  # noqa  # right-up
            return self._check_movement_diagonal(
                old_coords, new_coords, ignore_elements=ignore_map_elements, relevant_from_sides=[1, 0],
                relevant_to_sides=[3, 2])
        elif x_coord_diff < 0 and y_coord_diff > 0:  # noqa  # left-down
            return self._check_movement_diagonal(
                old_coords, new_coords, ignore_elements=ignore_map_elements, relevant_from_sides=[3, 2],
                relevant_to_sides=[1, 0])
        elif x_coord_diff < 0 and y_coord_diff < 0:  # noqa  # left-up
            return self._check_movement_diagonal(
                old_coords, new_coords, ignore_elements=ignore_map_elements, relevant_from_sides=[3, 0],
                relevant_to_sides=[1, 2])

        return False


class OrthogonalTiledCamera(TiledMapCamera):
    def __init__(self, game_map):
        """
        This class serves as the in-game camera for the Pink Engine maps, with the x and y being used as the
        viewport adjustment variables in Pink Engine map screens.
        :param OrthogonalTiledMap game_map: The game map this is the camera of
        """
        TiledMapCamera.__init__(self, game_map)

        self.viewport_x_offset = renpy.store.pink_otm_default_viewport_x_offset
        self.viewport_y_offset = renpy.store.pink_otm_default_viewport_y_offset
        self.viewport_width = renpy.store.pink_otm_default_viewport_width
        self.viewport_height = renpy.store.pink_otm_default_viewport_height

        self.camera_target = None
        self.xzoom = renpy.store.pink_otm_camera_current_xzoom
        self.yzoom = renpy.store.pink_otm_camera_current_yzoom

    def set_default_zoom(self, zoom):
        """
        Sets this camera's x and y zoom to the given value
        :param float zoom: the given zoom value
        """
        self.set_default_x_zoom(zoom)
        self.set_default_y_zoom(zoom)

    def set_default_x_zoom(self, xzoom):
        # TODO something
        self.set_x_zoom(xzoom)

    def set_default_y_zoom(self, yzoom):
        # TODO something
        self.set_y_zoom(yzoom)

    def set_zoom(self, zoom):
        """
        Sets this camera's x and y zoom to the given value
        :param float zoom: the given zoom value
        """
        self.set_x_zoom(zoom)
        self.set_y_zoom(zoom)

    def set_x_zoom(self, xzoom):
        """
        Sets this camera's x zoom to the given value
        :param float xzoom: the given zoom value
        """
        self.xzoom = xzoom
        self.x.range = renpy.store.pink_otm_current_map.image_size.x * self.xzoom
        renpy.store.pink_otm_zoom_controller.original_xzoom = xzoom
        renpy.store.pink_otm_zoom_controller.target_xzoom = xzoom
        renpy.store.pink_otm_camera_current_xzoom = xzoom
        self.center_on_target()

    def set_y_zoom(self, yzoom):
        """
        Sets this camera's y zoom to the given value
        :param float yzoom: the given zoom value
        """
        self.yzoom = yzoom
        self.y.range = renpy.store.pink_otm_current_map.image_size.y * self.yzoom
        renpy.store.pink_otm_zoom_controller.original_yzoom = yzoom
        renpy.store.pink_otm_zoom_controller.target_yzoom = yzoom
        renpy.store.pink_otm_camera_current_yzoom = yzoom
        self.center_on_target()

    def camera_map_refresh(self):
        """
        Called by the pink_otm_call_map label, refreshing the camera for the new map.
        """
        self.x.range = renpy.store.pink_otm_current_map.image_size.x * self.xzoom - self.viewport_width
        self.y.range = renpy.store.pink_otm_current_map.image_size.y * self.yzoom - self.viewport_height

        self.center_on_target()

    @staticmethod
    def camera_target_for_object(target_object):
        """
        Which particular to pixel to center for a camera aimed at the given object.
        :param OrthogonalTiledMapGameObjectMobile target_object: the given target
        """
        centered_x = (
                target_object.x + target_object.camera_offset_x + floor(target_object.width / 2))
        centered_y = (
                target_object.y + target_object.camera_offset_y + target_object.arc_y_offset +
                floor(target_object.height / 2))

        return centered_x, centered_y

    def center_on_target(self):
        """
        Makes the camera center on its current target.
        """
        if self.camera_target is None:
            return

        centered_x, centered_y = self.camera_target_for_object(self.camera_target)
        self.center_on_location(centered_x, centered_y)

    def center_on_location(self, target_x, target_y):
        """
        Used the center the camera on a specific location.
        :param int target_x: x (in pixels) of the target location
        :param int target_y: y (in pixels) of the target location
        :return:
        """
        pink_otm_current_map = renpy.store.pink_otm_current_map  # type: OrthogonalTiledMap

        target_x *= self.xzoom
        target_y *= self.yzoom

        if (pink_otm_current_map.image_size.x * self.xzoom) >= self.viewport_width:
            max_x = self.x.range
            centered_x = target_x - (self.viewport_width / 2)
            final_x = max(min(max_x, centered_x), 0)
        else:
            final_x = 0

        if (pink_otm_current_map.image_size.y * self.yzoom) >= self.viewport_height:
            max_y = self.y.range
            centered_y = target_y - (self.viewport_height / 2)
            final_y = max(min(max_y, centered_y), 0)
        else:
            final_y = 0

        self.x.change(final_x)
        self.y.change(final_y)

    def smooth_zoom(self, target_zoom, zoom_speed):
        """
        Smoothly zooms out to the given value in the given number of seconds.
        :param float target_zoom: Which zoom level you want to zoom to (in ratio of the default)
        :param float zoom_speed: Amount of time to spend zooming (in seconds)
        """
        zoom_controller = renpy.store.pink_otm_zoom_controller  # Py 2
        if (
                zoom_controller.target_xzoom != target_zoom or
                zoom_controller.target_yzoom != target_zoom or
                zoom_controller.zoom_speed != zoom_speed):
            zoom_controller.start_zoom_gt = zoom_controller.last_gt
            zoom_controller.original_xzoom = self.xzoom
            zoom_controller.original_yzoom = self.yzoom
            zoom_controller.target_xzoom = target_zoom
            zoom_controller.target_yzoom = target_zoom
            zoom_controller.zoom_speed = zoom_speed

    def set_target(self, target):
        """
        Makes this object follow the given target, without immediately centering.
        :param OrthogonalTiledMapGameObjectMobile target: the given target
        """
        self.camera_target = target

    def switch_target(self, new_target):  # TODO make it also accept a ref_name
        """
        Makes this object follow the given target, with immediate centering.
        :param OrthogonalTiledMapGameObject new_target: The given target.
        """
        self.camera_target = new_target
        self.center_on_target()

    def recenter_on_player(self):
        """
        Recenters the camera on the pc.
        """
        self.switch_target(renpy.store.pink_otm_current_pc)

    def spawn_camera_drone(self):
        """
        Spawns a camera drone and switches the camera to it. The camera drone is a pink collection object, which can
        then be given any kind of movement command.
        """
        drone_coord = self.camera_target.central_coord
        current_center_x, current_center_y = self.camera_target_for_object(self.camera_target)

        pink_otm_current_map = renpy.store.pink_otm_current_map  # type: OrthogonalTiledMap
        pink_otm_current_map.add_object_at_coord(
            renpy.store.pink_otm_camera_drone_init_dict, x_coord=drone_coord.x, y_coord=drone_coord.y)

        camera_drone = renpy.store.pink_otm_camera_drone
        drone_center_x, drone_center_y = self.camera_target_for_object(camera_drone)
        camera_drone.camera_offset_x = current_center_x - drone_center_x + camera_drone.camera_offset_x
        camera_drone.camera_offset_y = current_center_y - drone_center_y + camera_drone.camera_offset_y
        self.switch_target(renpy.store.pink_otm_camera_drone)


class DirectionCache(object):
    def __init__(self):
        self.direction_list = []

    def start_movement(self, direction):
        """
        Adds the given direction to the cache.
        :param str direction: the given direction
        """
        if direction not in self.direction_list:
            self.direction_list.append(direction)

    def set_movement(self, direction):
        """
        Makes the cache consist solely of a single move in the given direction.
        :param str direction: the given direction
        """
        self.direction_list = [direction]

    def stop_movement(self, direction):
        """
        Removes the given direction to the cache
        :param str direction: the given direction
        """
        if direction in self.direction_list:
            self.direction_list.remove(direction)

    def stop_movement_all(self):
        """
        Stops all movement
        """
        self.direction_list = []

    def current_movement_direction(self):
        """
        :return: The current movement direction
        :rtype: str
        """
        if len(self.direction_list) == 0:
            return None
        else:
            return self.direction_list[-1]


class OrthogonalTiledMap(TiledMapGame):
    npc_layer_dict = {
        "draworder": "topdown", "id": 999999999999, "name": "player_layer",
        "objects": [],
        "opacity": 1,
        "properties": [
            {"name": "layer_type", "type": "string", "value": "dynamic"},
            {"name": "z_order", "type": "int", "value": 100}],
        "type": "objectgroup", "visible": True, "x": 0, "y": 0}
    default_camera_variable = "pink_otm_current_camera"

    object_sprite_collection_class = OrthogonalTiledMapGameObjectSpriteCollection
    object_class = OrthogonalTiledMapGameObject
    tile_class = OrthogonalTiledMapGameTile
    tile_animated_class = OrthogonalTiledMapGameTileAnimated

    camera_class = OrthogonalTiledCamera

    def __init__(self, map_dict, path, **kwargs):
        """
        A single Orthogonal Tiled Map
        :param dict map_dict: The initialization dictionary for this map
        :param str path: The path at which this map can be found.
        """
        # Ren'py variable that can be used to reference loading maps before they are assigned to the current map
        #  variable.
        renpy.store.pink_otm_loading_map = self

        self.mobile_objects = []
        self.base_grid = OrthogonalTiledMapTiledBases(self, map_dict.get('width'), map_dict.get('height'))

        # new parallel process system, requires dict setup before object initialization
        self.parallel_processes = {}

        # Used to initialize events at the start of the map, must be setup before object initialization, so objects
        # can add events.
        self.start_map_events = StartMapEvents()

        TiledMapGame.__init__(self, map_dict, path, **kwargs)

        # noinspection PyTypeChecker
        self.player_object = None  # type: OrthogonalTiledMapGameObjectSpriteCollection
        self.npc_layer = self.add_layer(self.npc_layer_dict)

        # Dictionaries for matching various types of input to functions.
        self.event_type_functions = renpy.store.pink_otm_event_type_functions  # type: dict
        self.key_down_functions = renpy.store.pink_otm_key_down_functions  # type: dict
        self.key_up_functions = renpy.store.pink_otm_key_up_functions  # type: dict
        self.key_held_functions = renpy.store.pink_otm_key_held_functions  # type: dict
        self.movement_keys = renpy.store.pink_otm_movement_keys  # type: dict
        self.gamepad_movement_axis = renpy.store.pink_otm_gamepad_movement_axis  # type: dict
        self.gamepad_turning_axis = renpy.store.pink_otm_gamepad_turning_axis  # type: dict
        self.gamepad_held_functions = renpy.store.pink_otm_gamepad_held_keys  # type: dict
        self.gamepad_functions = renpy.store.pink_otm_gamepad_functions  # type: dict
        self.mouse_button_down_functions = renpy.store.pink_otm_mouse_button_down_functions  # type: dict
        self.mouse_button_up_functions = renpy.store.pink_otm_mouse_button_up_functions  # type: dict

        # Variables related to player movement
        self._direction_cache = DirectionCache()
        self._pc_is_running = False
        self._pc_walk_animation = renpy.store.pink_otm_default_walk_animation_name  # type: str
        self._pc_run_animation = renpy.store.pink_otm_default_run_animation_name  # type: str
        self._pc_walk_speed = renpy.store.pink_otm_current_walk_speed  # type: float
        self._pc_run_speed = renpy.store.pink_otm_current_run_speed  # type: float

        # Variables related specifically to mouse functionality
        self._mouse_state = None  # None if unpressed, click if briefly pressed, hold if pressed for longer.
        self._mouse_click_start = None  # None if unpressed, st of first mou
        self._mouse_move_target_pixel = None  # none if unpressed, pixel that's currently hovered over if pressed
        self._mouse_move_target = None  # none if unpressed, set to currently targeted coord if key is pressed.

        # Variables related to freezing the screen when the menu is open
        self._screen_freeze = False
        self._screen_freeze_gt = 0.0
        self._screen_freeze_parallel_processes = set()

        # Force check touch on go_to_map
        self.force_check_touch = False

        # Check for start map events
        self.checked_start_map_event = False

        # Start default parallel processes
        for parallel_process_class in renpy.store.pink_otm_standard_parallel_processes:
            parallel_process_class.ensure_existence(self)

        # Inherit consistent overlays
        if renpy.store.pink_otm_current_map is not None:
            consistent_overlays = renpy.store.pink_otm_current_map.get_consistent_overlays()
            self._overlay_manager.add_consistent_overlays(consistent_overlays)

        # Used to ensure the player can't save during cutscene movement waits (which causes a loading issue due to
        #  ren'py)
        self.current_event_wait: Optional[EventWait] = None

        renpy.store.pink_otm_loading_map = None

    def get_consistent_overlays(self) -> List[Overlay]:
        return self._overlay_manager.get_consistent_overlays()

    def reload_keys(self):
        """
        Reloads the input keys this map responds to, processing any changes.
        """
        self.event_type_functions = renpy.store.pink_otm_event_type_functions  # type: dict
        self.key_down_functions = renpy.store.pink_otm_key_down_functions  # type: dict
        self.key_up_functions = renpy.store.pink_otm_key_up_functions  # type: dict
        self.key_held_functions = renpy.store.pink_otm_key_held_functions  # type: dict
        self.movement_keys = renpy.store.pink_otm_movement_keys  # type: dict
        self.gamepad_movement_axis = renpy.store.pink_otm_gamepad_movement_axis  # type: dict
        self.gamepad_turning_axis = renpy.store.pink_otm_gamepad_turning_axis  # type: dict
        self.gamepad_held_functions = renpy.store.pink_otm_gamepad_held_keys  # type: dict
        self.gamepad_functions = renpy.store.pink_otm_gamepad_functions  # type: dict
        self.mouse_button_down_functions = renpy.store.pink_otm_mouse_button_down_functions  # type: dict
        self.mouse_button_up_functions = renpy.store.pink_otm_mouse_button_up_functions  # type: dict

    def check_existence(self):
        """
        :return: True if a OTM map currently exists.
        :rtype: bool
        """
        return renpy.store.pink_otm_current_map is not None

    def game_tick(self, gt):
        """
        Core gameplay loop, advancing the game by a single tick per run.
        :param float gt: The current game time in seconds
        """
        # Checks for a player touch event immediately on map start.
        if (
                self.force_check_touch and
                self.player_object is not None and
                renpy.store.pink_otm_current_event_name is None):
            self.force_check_touch = False
            self.check_touch(self.player_object)

        # Checks for a start map event on map start.
        if not self.checked_start_map_event:
            self.checked_start_map_event = True
            self.check_start_map_event()

        # If the gt has been reset for whatever reason, this updates the animation frame times for all animated tiles
        # to correspond to the reset st.
        if gt < self.last_gt:
            for animated_tile in self.animated_tiles:
                animated_tile.st_reset_frames(gt)

            if self.current_event_wait is not None:
                self.current_event_wait.st_reset(self.last_gt, gt)
            gt_diff = self.last_gt + gt
        else:
            gt_diff = gt - self.last_gt

        # Checks whether a menu screen is open
        self.check_freeze_screen(gt)

        # Checks whether current mid-event wait is over
        if self.current_event_wait is not None:
            self.current_event_wait.check_wait(gt)

        # Updates scaled and panned sound channels
        renpy.store.pink_sound_manager.per_frame(gt)

        if not self._screen_freeze:
            # Updates timer, checks for timed code
            renpy.store.otm_timer.per_tick(gt_diff)

            # Checks for timed event
            if renpy.store.pink_otm_current_event_name is None:
                event_data = renpy.store.otm_timer.check_timed_event()

                if event_data is not None:
                    event, event_args, event_kwargs = event_data
                    self.trigger_event(event, "timer", *event_args, **event_kwargs)

        # Moves mobile objects
        self.check_player_movement()
        for mobile_object in self.mobile_objects:
            mobile_object.per_tick(gt)

        # Advances animations and checks conditional objects
        TiledMapGame.game_tick(self, gt)

        # Runs every parallel process once.
        if self is renpy.store.pink_otm_current_map:
            # Only checks for local parallel processes when not fading between maps.
            for parallel_process in self.parallel_processes.values():
                parallel_process.per_tick(gt)

        renpy.exports.retain_after_load()

    def pause_parallel_processes(self, *processes):
        """
        Pauses all parallel processes with the given IDs until the current event ends. No action is taken if a
        parallel process with a given ID is not initiated.
        :param str processes: The IDs for the processes to pause.
        """
        for parallel_process in processes:   # type: ParallelProcess
            if parallel_process in self.parallel_processes:
                self.parallel_processes[parallel_process].pause()

    def unpause_parallel_processes(self, *processes):
        """
        Unpauses all parallel processes with the given IDs. No action is taken if a  parallel process with a given ID
        is not initiated.
        :param str processes: The IDs for the processes to unpause.
        """
        for parallel_process in processes:
            if parallel_process in self.parallel_processes:
                this_parallel_process = self.parallel_processes[parallel_process]  # type: ParallelProcess
                this_parallel_process.unpause()

    def pause_all_parallel_processes(self):
        """
        Pauses all parallel processes
        """
        for parallel_process in self.parallel_processes.values():  # type: ParallelProcess
            parallel_process.pause()

    def unpause_all_parallel_processes(self):
        """
        Unpauses all parallel processes
        """
        for parallel_process in self.parallel_processes.values():  # type: ParallelProcess
            if parallel_process.paused:
                parallel_process.unpause()

    def is_tile_impassible(self, x_coord: int, y_coord: int) -> bool:
        return self.base_grid.get_top_base_with_property(
                'move_to', x_coord, y_coord, ignore_elements=[renpy.store.pink_otm_current_pc], default_value='0000'
        ) == "0000"

    def check_freeze_screen(self, gt):
        """
        Freezes and unfreezes the game depending on whether or not there are any menu screens open and whether the
        game is currently frozen because of that.
        :param float gt: The current game time in seconds
        """
        # Freezes the game when a menu screen is up.
        freeze_screen_open = self.freeze_screen_open()
        if not self._screen_freeze:
            # The game is currently not frozen.
            if freeze_screen_open:
                # A menu screen is open, so the screen should be frozen
                self._screen_freeze = True
                self._screen_freeze_gt = gt
                renpy.store.pink_sound_manager.pause_all_sounds()

                self.disable_controls()
                self.stop_running()
                self.freeze_map()
                self._overlay_manager.pause()
                for process_id, parallel_process in self.parallel_processes.items():
                    if not parallel_process.paused:
                        parallel_process.pause()
                        self._screen_freeze_parallel_processes.add(process_id)

        else:
            # The game is currently frozen because of a menu screen
            if freeze_screen_open:
                # A menu screen is still open, so the game should remain frozen.
                return

            self._screen_freeze = False

            if gt == 0.0:
                # The game was just loaded from a save file.
                self.recheck_variable_sprite_collections()
                self._overlay_manager.increment_all_gt(self._overlay_manager.last_st - self._screen_freeze_gt)
                self._overlay_manager.unpause()
                if renpy.store.pink_otm_current_event_type == 'static':
                    # However, the game should remain frozen because there is a static event going on. The movement GT
                    # should increment with self.last_gt so that the unfreezing process at the end
                    # of the event has the correct game time.
                    self._increment_all_gt(self.last_gt, include_paused_processes=True)
                else:
                    # No static event is going on, so controls are enabled, and the map is unfrozen.
                    # GT increment is based off the object's last gt prior to being saved.
                    renpy.store.pink_sound_manager.unpause_all_sounds()
                    self.unfreeze_map(increment_gt=False)
                    for parallel_process_id in self._screen_freeze_parallel_processes:
                        self.parallel_processes[parallel_process_id].paused = False

                    for parallel_process in self.parallel_processes.values():
                        parallel_process.increment_gt(parallel_process.last_gt - self._screen_freeze_gt)

                    self._screen_freeze_parallel_processes = set()
                    if renpy.store.pink_otm_current_event_type is None:
                        self.stop_running()
                        self.enable_controls()
                        self.check_held_keys()
            else:
                # A menu screen was just closed.
                gt_diff = gt - self._screen_freeze_gt

                self._overlay_manager.increment_all_gt(gt_diff)
                self._overlay_manager.unpause()

                if renpy.store.pink_otm_current_event_type == 'static':
                    # However, the game should remain frozen because there is a static event going on. Because a
                    # static event ends in a GT reset, no movement/animation GT increment is required.
                    pass
                else:
                    # No static event is going on, so controls are enabled. The movement GT, animation GT and parallel
                    # process GT should increment by the amount of time the menu was open.
                    renpy.store.pink_sound_manager.unpause_all_sounds()
                    for parallel_process_id in self._screen_freeze_parallel_processes:
                        self.parallel_processes[parallel_process_id].paused = False
                    self._screen_freeze_parallel_processes = set()
                    self._increment_all_gt(gt_diff)
                    self.unfreeze_map(increment_gt=False)
                    if renpy.store.pink_otm_current_event_type is None:
                        self.stop_running()
                        self.enable_controls()
                        self.check_held_keys()

    def _increment_all_gt(self, gt_diff, include_paused_processes=False):
        """
        Increments all animation and movement gts by the given amount, used if the game skips over a period of game time
        :param float gt_diff: The amount by which to increment gt.
        :param bool include_paused_processes: Includes paused processes
        """
        self._increment_all_animation_gt(gt_diff)
        self._increment_all_movement_gt(gt_diff)
        self._increment_all_parallel_process_gt(gt_diff, include_paused_processes=include_paused_processes)

    def _increment_all_animation_gt(self, gt_diff):
        """
        Increments all animation gts by the given amount, used if the game skips over a period of game time
        :param float gt_diff: The amount by which to increment gt.
        """
        for animated_tile in self.animated_tiles:  # type: OrthogonalTiledMapGameTileAnimated
            animated_tile.increment_gt(gt_diff)

    def _increment_all_movement_gt(self, gt_diff):
        """
        Increments all movement gts by the given amount, used if the game skips over a period of game time
        :param float gt_diff: The amount by which to increment gt.
        """
        for mobile_object in self.mobile_objects:  # type: OrthogonalTiledMapGameObjectMobile
            mobile_object.increment_gt(gt_diff)

    def _increment_all_parallel_process_gt(self, gt_diff, include_paused_processes=False):
        """
        Increments all parallel process gts by the given amount, used if the gave skips over a period of game time.
        :param float gt_diff: The amount by which to increment gt.
        """
        for parallel_process in self.parallel_processes.values():  # type: ParallelProcess
            if include_paused_processes or not parallel_process.paused:
                parallel_process.increment_gt(gt_diff)

    @staticmethod
    def freeze_screen_open():
        """
        Determines whether or not a screen that the OTM should freeze on is currently open. The list of screen
        tag/layer combinations is contained in the pink_freeze_game_screens renpy variable, which is set in the pink
        config
        """
        pink_freeze_game_screens = renpy.store.pink_freeze_game_screens  # Py2
        for tag, layer in pink_freeze_game_screens:
            if renpy.exports.get_screen(tag, layer=layer):
                return True
        return False

    def change_walk_speed(self, new_speed):
        """
        Changes the player walking speed to the given value.
        :param float new_speed: The player's new walking speed.
        """
        renpy.store.pink_otm_current_walk_speed = new_speed
        self._pc_walk_speed = new_speed

    def change_run_speed(self, new_speed):
        """
        Changes the player running speed to the given value.
        :param float new_speed: The player's new running speed.
        """
        renpy.store.pink_otm_current_run_speed = new_speed
        self._pc_run_speed = new_speed

    def check_run(self):
        # Movement animation and speed  # TODO not efficient?
        if self._pc_is_running:
            if self.player_object.move_animation != self._pc_run_animation:
                self.player_object.control_stack.append(
                    ControlCommand('change_move_animation', animation_name=self._pc_run_animation,
                                   never_repeat=True))
            if self.player_object.movement_speed != self._pc_run_speed:
                self.player_object.control_stack.append(
                    ControlCommand('change_movement_speed', quantity=self._pc_run_speed, never_repeat=True))
        else:
            if self.player_object.move_animation != self._pc_walk_animation:
                self.player_object.control_stack.append(
                    ControlCommand('change_move_animation', animation_name=self._pc_walk_animation,
                                   never_repeat=True))
            if self.player_object.movement_speed != self._pc_walk_speed:
                self.player_object.control_stack.append(
                    ControlCommand('change_movement_speed', quantity=self._pc_walk_speed, never_repeat=True))

    def check_player_movement(self):
        """
        The player's per-tick movement calculation
        """
        current_movement_direction = self._direction_cache.current_movement_direction()

        # Checks if next movement does not match current direction, pops it if so.
        if (
                self.controls_enabled and
                current_movement_direction is not None and
                len(self.player_object.control_stack) == 1
        ):
            if self.player_object.control_stack[0].type not in ("special_move", "go_to_smart") and (
                (current_movement_direction == "right" and self.player_object.control_stack[0].type != "go_right") or
                (current_movement_direction == "left" and self.player_object.control_stack[0].type != "go_left") or
                (current_movement_direction == "up" and self.player_object.control_stack[0].type != "go_up") or
                (current_movement_direction == "down" and self.player_object.control_stack[0].type != "go_down")
            ):
                self.player_object.control_stack.pop(0)

        if (
                self.controls_enabled and
                current_movement_direction is not None and
                len(self.player_object.control_stack) == 0
        ):
            self.check_run()
            # Actual movement
            self.player_object.control_stack.append(
                ControlCommand(
                    "go_" + current_movement_direction,
                    turn_and_move=renpy.store.pink_otm_turn_and_move,
                    animate_invalid_move=renpy.store.pink_otm_animate_invalid_move,
                    pop_invalid_move=True, never_repeat=True))

    def add_element(self, x, y, layer, game_object, already_in_conditional=False):
        """
        Adds a new element to the game map, and returns its displayable id. Checks for conditionality first.
        :param int x: Distance in pixels between the object's left side and the left border of the map.
        :param int y: Distance in pixels between the object's top side and the top border of the map.
        :param TiledMapGameLayer layer: The layer the object is a part of.
        :param OrthogonalTiledMapGameTile|OrthogonalTiledMapGameTileAnimated|OrthogonalTiledMapGameObject game_object:
        The object to add
        :param bool already_in_conditional: Set to True when adding an object that is already present in the
        conditional list, so that it does not get re-added.
        :rtype: int
        """
        TiledMapGame.add_element(self, x, y, layer, game_object, already_in_conditional=already_in_conditional)
        if game_object.is_conditional:
            if game_object.condition_met():
                self._add_element(x, y, layer, game_object)
        else:
            self._add_element(x, y, layer, game_object)

    def _add_element(self, x, y, layer, game_object):
        """
        Subfunction of add_element
        :param int x: Distance in pixels between the object's left side and the left border of the map.
        :param int y: Distance in pixels between the object's top side and the top border of the map.
        :param TiledMapGameLayer layer: The layer the object is a part of.
        :param OrthogonalTiledMapGameTile|OrthogonalTiledMapGameTileAnimated|OrthogonalTiledMapGameObject game_object:
        The object to add
        :rtype: int
        """
        if isinstance(game_object, OrthogonalTiledMapGameObjectMobile):
            self.mobile_objects.append(game_object)

        # Override coords if the object has its own. This accommodates consistent objects.
        if hasattr(game_object, 'x'):
            x = game_object.x
        if hasattr(game_object, 'y'):
            y = game_object.y
        self.base_grid.add_element(x, y, layer, game_object)

        if isinstance(game_object, OrthogonalTiledMapGameObjectSpriteCollection):
            # If adding post-initiation, rebases frames
            if self.last_gt != 0.0:
                game_object.st_reset_frames(self.last_gt)

            # Auto-centers
            if game_object.should_be_auto_centered():
                central_coord = game_object.central_coord
                game_object.set_to_coords(central_coord.x, central_coord.y, orientation=game_object.start_orientation)

            if renpy.store.pink_otm_current_event_type == 'static':
                game_object.freeze()
            elif renpy.store.pink_otm_current_event_type == "dynamic":
                game_object.save_and_halt()
        game_object.run_code_on_add()
        if hasattr(game_object, 'emits_sound') and getattr(game_object, 'emits_sound') is not None:
            game_object.sound_channel = renpy.store.pink_sound_manager.play_sound(
                sound_file=game_object.emits_sound,
                emitter=game_object,
                pan=game_object.emits_sound_pan,
                scale=game_object.emits_sound_scale,
                max_volume_distance=game_object.emits_sound_max_volume_distance,
                min_volume_distance=game_object.emits_sound_min_volume_distance,
                min_volume=game_object.emits_sound_min_volume,
                max_volume=game_object.emits_sound_max_volume,
                max_pan_distance=game_object.emits_sound_max_pan_distance,
                no_pan_distance=game_object.emits_sound_no_pan_distance,
                max_pan=game_object.emits_sound_max_pan,
                loop=True,
                mixer=game_object.emits_sound_mixer)

    def remove_element(self, element):
        """
        Removes the given element from the map
        :param OrthogonalTiledMapGameTile|OrthogonalTiledMapGameTileAnimated|OrthogonalTiledMapGameObject element:
        The element to remove
        """
        element.run_code_on_remove()
        if hasattr(element, 'emits_sound') and getattr(element, 'emits_sound') is not None:
            element.sound_channel = renpy.store.pink_sound_manager.stop_sound(element.sound_channel)

        if isinstance(element, OrthogonalTiledMapGameObjectMobile):
            self.mobile_objects.remove(element)

        base_id = element.base_id
        self.base_grid.remove_element(base_id)
        TiledMapGame.remove_element(self, element)

    def add_object_at_coord(
            self, object_dict, x_coord=0, y_coord=0, is_player=False, orientation=None
    ):
        """
        Adds a new element to the game map at the given coordinates.
        :param dict object_dict: The initialization dictionary for the object
        :param int x_coord: The x coordinate which to center the object on
        :param int y_coord: The y coordinate which to center the object on
        :param bool is_player: Whether this object is the player character
        :param str orientation: The orientation to which to set the new object.
        """
        new_object = self.add_object(object_dict=object_dict, x=0, y=0, layer=self.npc_layer)
        new_object.set_to_coords(x_coord, y_coord, orientation=orientation)

        if is_player:
            self.camera.set_target(new_object)
            self.player_object = new_object

        return new_object

    def pixel_to_coord(self, pixel_loc, is_x=True):
        """
        Returns the coordinates of the given pixel on the current map.
        :param int pixel_loc: The given pixel location.
        :param bool is_x: Whether the given pixel location is an x (if True), or a y (if False)
        :return: The coordinates of the given pixel on the current map.
        :rtype: int
        """
        if is_x:
            return floor(pixel_loc / self.tile_size.x)
        else:
            return floor(pixel_loc / self.tile_size.y)

    def check_conditional_object(self, conditional_object):
        """
        Checks the given object's conditionality, adding and removing it according to whether or not their condition is
        currently met.
        :param OrthogonalTiledMapGameObject conditional_object: The object to check the conditionality of
        """
        if not conditional_object.is_on_map() and conditional_object.condition_met():
            self.add_element(
                conditional_object.x, conditional_object.y, conditional_object.layer, conditional_object,
                already_in_conditional=True)

            if isinstance(conditional_object, OrthogonalTiledMapGameObjectSpriteCollection):
                # Variable sprite collection
                if conditional_object.sprite_collection_path.startswith('renpy.store'):
                    conditional_object.switch_sprite_collection(conditional_object.sprite_collection_path)

        elif conditional_object.is_on_map() and not conditional_object.condition_met():
            self.remove_element(conditional_object)

    def check_activation_code(self):
        """
        Called by the interaction key, this checks whether there is code to be interacted with in the current
        location. If so, this function also executes that code
        """
        if self.player_object is None:
            return

        player_base = self.base_grid.map_elements[self.player_object.base_id]

        for x, y in player_base.coords:
            if self.player_object.orientation == "up":
                code, code_cause = self.base_grid.get_activation_code(x, y - 1, ignore_element=player_base)
            elif self.player_object.orientation == "right":
                code, code_cause = self.base_grid.get_activation_code(x + 1, y, ignore_element=player_base)
            elif self.player_object.orientation == "down":
                code, code_cause = self.base_grid.get_activation_code(x, y + 1, ignore_element=player_base)
            elif self.player_object.orientation == "left":
                code, code_cause = self.base_grid.get_activation_code(x - 1, y, ignore_element=player_base)
            else:
                break

            """Executes code"""
            if code:
                code_cause.run_code_on_activate()

    def check_activation_event(self, event_button):
        """
        Called by the interaction key, this checks whether there is an event to be interacted with in the current
        location. If so, this function also calls that event.
        :param tuple event_button: A tuple representing the button that was pressed to trigger the event. First
        value in the tuple is a string representing the device on which the button was pressed ('keyboard', 'mouse',
        'controller'), second part is an identifying int or string for the button.
        """
        if self.player_object is None:
            return

        player_base = self.base_grid.map_elements[self.player_object.base_id]

        for x, y in player_base.coords:
            if self.player_object.orientation == "up":
                event, event_cause = self.base_grid.get_activation_event(x, y - 1, ignore_element=player_base)
            elif self.player_object.orientation == "right":
                event, event_cause = self.base_grid.get_activation_event(x + 1, y, ignore_element=player_base)
            elif self.player_object.orientation == "down":
                event, event_cause = self.base_grid.get_activation_event(x, y + 1, ignore_element=player_base)
            elif self.player_object.orientation == "left":
                event, event_cause = self.base_grid.get_activation_event(x - 1, y, ignore_element=player_base)
            else:
                break

            """Jumps to event in question"""
            if event:
                event_args, event_kwargs = event_cause.event_on_activate_args, event_cause.event_on_activate_kwargs
                renpy.store.pink_otm_event_button = event_button
                return self.trigger_event(event, event_cause, *event_args, **event_kwargs)

    def check_touch(self, triggering_object):
        """
        Checks whether the given object should trigger any touch code or events. If so, this function also executes that
        code and/or calls that event.
        :param OrthogonalTiledMapGameObjectBase triggering_object: The given object
        """
        code, code_cause, event, event_cause = None, None, None, None
        if renpy.store.pink_otm_current_event_type is None:
            if triggering_object is self.player_object:
                player_base = self.base_grid.map_elements[self.player_object.base_id]
                for x, y in player_base.coords:
                    code, code_cause = self.base_grid.get_touch_code(
                        x, y, ignore_element=player_base)
                    event, event_cause = self.base_grid.get_touch_event(
                        x, y, ignore_element=player_base)
            else:
                if triggering_object.code_conditional_met:
                    code, code_cause = triggering_object.code_on_touch, triggering_object
                if triggering_object.event_conditional_met:
                    event, event_cause = triggering_object.event_on_touch, triggering_object

        if code:
            code_cause.run_code_on_touch()

        """Jumps to event in question"""
        if event:
            event_args, event_kwargs = event_cause.event_on_touch_args, event_cause.event_on_touch_kwargs
            return self.trigger_event(event, event_cause, *event_args, **event_kwargs)

    def check_start_map_event(self):
        start_map_event = self.start_map_events.get_start_map_event()
        if start_map_event:
            self.trigger_event(
                start_map_event.event, start_map_event.object, *start_map_event.args, **start_map_event.kwargs)

    @staticmethod
    def trigger_event(event_label, event_cause, *args, **kwargs):
        """
        Triggers the event with the given label
        :param str event_label: The given event label
        :param OrthogonalTiledMapGameObjectBase|str event_cause: The object causing the event to be triggered
        """
        renpy.store.pink_otm_current_event_name = event_label
        renpy.store.pink_otm_event_trigger = event_cause
        renpy.exports.call(event_label, *args, **kwargs)

    def event_key_down(self, ev, x, y, st):  # noqa
        """
        Checks whether this should execute any functions on a given key_down event, and executes them if so.
        :param ev: The event
        :param x: event x
        :param y: event y
        :param st: event st
        """
        if not self.controls_enabled:
            return
        if ev.key in self.movement_keys:
            self._movement_key_down(ev, x, y, st)
        elif ev.key in self.key_down_functions:
            self.key_down_functions[ev.key](self, ev, x, y, st)  # noqa

    def event_key_up(self, ev, x, y, st):  # noqa
        """
        Checks whether this should execute any functions on a given key_up event, and executes them if so.
        :param ev: The event
        :param x: event x
        :param y: event y
        :param st: event st
        """
        if not self.controls_enabled:
            return
        if ev.key in self.movement_keys:
            self._movement_key_up(ev, x, y, st)
        if ev.key in self.key_up_functions:
            self.key_up_functions[ev.key](self, ev, x, y, st)  # noqa

    def event_gamepad(self, ev, x, y, st):
        """
        Checks whether this should execute any functions on a given EVENTNAME event (EVENTNAME is the event name for
        gamepad events), and executes them if so.
        :param ev: The event
        :param x: event x
        :param y: event y
        :param st: event st
        """
        if not self.controls_enabled:
            raise renpy.exports.IgnoreEvent()
        if hasattr(ev, 'controller') and ev.controller in self.gamepad_functions:
            self.gamepad_functions[ev.controller](self, ev, x, y, st)

    def event_mouse_move(self, ev, x, y, st):  # noqa
        if not self.controls_enabled:
            return
        if self._mouse_state is not None:
            if (
                    self._mouse_state == 'click' and
                    self._mouse_click_start + renpy.store.pink_otm_hold_delay < self.last_gt
            ):
                self._mouse_state = 'hold'

            self._mouse_move_target_pixel = (x, y)
            if self._mouse_state == 'hold' and renpy.store.pink_otm_mouse_held_move:
                self.process_mouse_hold_move(x, y)

    def event_mouse_button_down(self, ev, x, y, st):
        """
        Checks whether this should execute any functions on a given mouse_button_down event, and executes them if so.
        :param ev: The event
        :param x: event x
        :param y: event y
        :param st: event st
        """
        if not self.controls_enabled:
            return
        if ev.button in self.mouse_button_down_functions:
            self.mouse_button_down_functions[ev.button](self, ev, x, y, st)  # noqa

    def event_mouse_button_up(self, ev, x, y, st):
        """
        Checks whether this should execute any functions on a given mouse_button_up event, and executes them if so.
        :param ev: The event
        :param x: event x
        :param y: event y
        :param st: event st
        """
        if not self.controls_enabled:
            return
        if ev.button in self.mouse_button_up_functions:
            self.mouse_button_up_functions[ev.button](self, ev, x, y, st)  # noqa

    def event_joy_axis_motion(self, ev, x, y, st):  # noqa
        """
        Checks whether this should execute any functions on a given joy_axis_motion event, and executes them if so.
        :param ev: The event
        :param x: event x
        :param y: event y
        :param st: event st
        """
        if not self.controls_enabled:
            return
        axis = ev.axis
        value = ev.value

        # Is this a movement on an x axis or a y axis?
        if axis % 2 == 0:
            x_axis = True
        else:
            x_axis = False

        # If movement is set to 0, stops movement
        if value == 0:
            self.stop_movement_all()

        # Otherwise, moves in the right direction
        elif x_axis:
            if value < 0:
                self.start_movement("left")
            else:
                self.start_movement("right")
        else:
            if value < 0:
                self.start_movement("down")
            else:
                self.start_movement("up")
        raise renpy.exports.IgnoreEvent()

    def event_joy_ball_motion(self, ev, x, y, st):  # noqa
        """
        Checks whether this should execute any functions on a given joy_ball_motion event, and executes them if so.
        :param ev: The event
        :param x: event x
        :param y: event y
        :param st: event st
        """
        if not self.controls_enabled:
            return
        # This function is left as an exercise to the reader.
        pass

    def event_joy_hat_motion(self, ev, x, y, st):  # noqa
        """
        Checks whether this should execute any functions on a given joy_hat_motion event, and executes them if so.
        :param ev: The event
        :param x: event x
        :param y: event y
        :param st: event st
        """
        if not self.controls_enabled:
            return
        hat_x, hat_y = ev.value
        if hat_x == hat_y == 0:
            return
        if abs(hat_x) > abs(hat_y):
            if hat_x < 0:
                self.turn_player("left")
            else:
                self.turn_player("right")
        else:
            if hat_y < 0:
                self.turn_player("down")
            else:
                self.turn_player("up")
        raise renpy.exports.IgnoreEvent()

    def _movement_key_down(self, ev, x, y, st):  # noqa
        """
        Checks whether this should execute any functions on a given key_down event if said key is registered as
        a movement key, and executes them if so.
        :param ev: The event
        :param x: event x
        :param y: event y
        :param st: event st
        """
        self.interrupt_mouse_click_move()
        direction = self.movement_keys[ev.key]
        if ev.mod & pygame.KMOD_ALT and renpy.store.pink_otm_alt_turning_enabled:
            self.turn_player(direction)
        else:
            self.start_movement(direction)
        raise renpy.exports.IgnoreEvent()

    def _left_movement_key_down_gamepad(self, ev, x, y, st):  # noqa
        self.set_movement("left")
        raise renpy.exports.IgnoreEvent()

    def _right_movement_key_down_gamepad(self, ev, x, y, st):  # noqa
        self.set_movement("right")
        raise renpy.exports.IgnoreEvent()

    def _up_movement_key_down_gamepad(self, ev, x, y, st):  # noqa
        self.set_movement("up")
        raise renpy.exports.IgnoreEvent()

    def _down_movement_key_down_gamepad(self, ev, x, y, st):  # noqa
        self.set_movement("down")
        raise renpy.exports.IgnoreEvent()

    def _movement_key_up(self, ev, x, y, st):  # noqa
        """
        Checks whether this should execute any functions on a given key_up event if said key is registered as
        a movement key, and executes them if so.
        :param ev: The event
        :param x: event x
        :param y: event y
        :param st: event st
        """
        direction = self.movement_keys[ev.key]
        self.stop_movement(direction)
        raise renpy.exports.IgnoreEvent()

    def _left_right_movement_key_up_gamepad(self, ev, x, y, st):  # noqa
        self.stop_movement("left")
        self.stop_movement("right")
        raise renpy.exports.IgnoreEvent()

    def _up_down_movement_key_up_gamepad(self, ev, x, y, st):  # noqa
        self.stop_movement("up")
        self.stop_movement("down")
        raise renpy.exports.IgnoreEvent()

    def _left_turn_gamepad(self, ev, x, y, st):  # noqa
        self.turn_player("left")
        raise renpy.exports.IgnoreEvent()

    def _right_turn_gamepad(self, ev, x, y, st):  # noqa
        self.turn_player("right")
        raise renpy.exports.IgnoreEvent()

    def _up_turn_gamepad(self, ev, x, y, st):  # noqa
        self.turn_player("up")
        raise renpy.exports.IgnoreEvent()

    def _down_turn_gamepad(self, ev, x, y, st):  # noqa
        self.turn_player("down")
        raise renpy.exports.IgnoreEvent()

    def check_held_keys(self):
        """
        Checks the currently held keys, and whether any functions should be executed depending on those keys. Used
        to start movement immediately on entering a new map or ending an event.
        """
        if not self.controls_enabled:
            return
        self.check_held_direction()
        self.stop_running()

        # Keyboard
        keys = pygame.key.get_pressed()
        for held_key in self.key_held_functions:
            if keys[held_key]:
                self.key_held_functions[held_key](self)  # noqa

        holding_movement_key = False
        for movement_key in self.movement_keys:
            if keys[movement_key]:
                holding_movement_key = True
                break

        # Controllers
        controllers = _get_controllers()
        for controller in controllers:
            if not controller.get_init():
                controller.init()

        for controller in controllers:
            for held_key in self.gamepad_held_functions:
                if controller.get_button(pygame.controller.get_button_from_string(held_key.encode('utf-8'))) == 1:
                    self.gamepad_held_functions[held_key](self)
            for movement_axis in self.gamepad_movement_axis:
                if abs(controller.get_axis(
                        pygame.controller.get_axis_from_string(movement_axis.encode('utf-8')))) > 10000:
                    holding_movement_key = True
                    break
            for turning_axis in self.gamepad_turning_axis:
                if abs(controller.get_axis(
                        pygame.controller.get_axis_from_string(turning_axis.encode('utf-8')))) > 10000:
                    holding_movement_key = True
                    break

        # Mouse
        if self._mouse_state is None and pygame.mouse.get_pressed()[0] == 1:
            self._mouse_state = 'click'
            if self._mouse_click_start is None:
                self._mouse_click_start = self.last_gt
                self._mouse_move_target_pixel = pygame.mouse.get_pos()

        if self._mouse_state is not None and self._mouse_move_target_pixel is not None:
            # Second clause in if statement necessary for preventing error on game quit.
            # Updates mouse movement target as map shifts while player moves.
            if (
                    self._mouse_state == 'click' and
                    self._mouse_click_start + renpy.store.pink_otm_hold_delay < self.last_gt
            ):
                self._mouse_state = 'hold'

            x, y = self._mouse_move_target_pixel
            if self._mouse_state == 'hold' and renpy.store.pink_otm_mouse_held_move:
                self.process_mouse_hold_move(x, y)
            elif renpy.store.pink_otm_mouse_click_move:
                self.process_mouse_click_move(x, y)

        if not holding_movement_key and self._mouse_state is None:
            self.stop_movement_all()

    @staticmethod
    def allowed_to_run():
        """
        :return: Whether the player is currently allowed to run
        :rtype: bool
        """
        return not (renpy.store.pink_otm_current_map.forbid_run or renpy.store.pink_otm_forbid_run)

    def forced_to_run(self):
        """
        :return: Whether the player is currently forced to run
        :rtype: bool
        """
        return self.allowed_to_run() and (renpy.store.pink_otm_current_map.force_run or renpy.store.pink_otm_force_run)

    def console_key_down(self, ev, x, y, st):  # noqa
        """
        Executes an event where the current console key is pressed. Checks whether the player is allowed to
        access the console, and whether the shift key is held before jumping to console label.
        """
        if (renpy.store.config.console or renpy.store.config.developer) and (ev.mod & pygame.KMOD_SHIFT):
            # This is a call rather than a jump, as the label makes use of leave_otm, which pops the
            # latest item off the call stack.
            renpy.exports.call("pink_otm_developer_start")
            raise renpy.exports.IgnoreEvent()

    def run_key_down(self, ev, x, y, st):  # noqa
        """
        Executes an event where the run key is pressed down. Checks whether the player is allowed to start running,
        and makes the player start running if so.
        """
        self.start_running()
        raise renpy.exports.IgnoreEvent()

    def run_key_up(self, ev, x, y, st):  # noqa
        """
        Executes an event where the run key is released. Checks whether the player is allowed to stop running,
        and makes the player stop running if so.
        """
        self.stop_running()
        raise renpy.exports.IgnoreEvent()

    def start_running(self):
        """
        Makes the player start running if allowed.
        """
        if self.allowed_to_run():
            self._pc_is_running = True

    def stop_running(self):
        """
        Makes the player stop running if allowed.
        """
        if not self.forced_to_run():
            self._pc_is_running = False

    def turn_player(self, direction):
        """
        Adds a turn command in the given direction to the player's control stack
        :param str direction: the given direction
        """
        self.player_object.control_stack = []
        self.player_object.control_stack.append(ControlCommand(command_type='turn_' + direction))

    def start_movement(self, direction):
        """
        Makes the player start movement in the given direction. Start movement is meant for the keyboard, and keeps
        track of all held keys. If you release the currently held key but are still holding another, start movement
        will switch to the still held key.
        :param str direction: the given direction
        """
        self._direction_cache.start_movement(direction)

    def set_movement(self, direction):
        """
        Makes the player start movement in the given direction. Set movement is meant for the gamepad, and does not
        keep track of held keys (since a stick can't hold more than one direction at once).
        :param str direction: the given direction
        """
        self._direction_cache.set_movement(direction)

    def stop_movement(self, direction):
        """
        Makes the player stop movement in the given direction
        :param str direction: the given direction
        """
        if self._direction_cache.current_movement_direction() == direction:
            if (
                    len(self.player_object.control_stack) > 0 and
                    self.player_object.control_stack[0].type == "go_" + direction
            ):
                self.player_object.control_stack.pop(0)
            self.check_held_direction()
        self._direction_cache.stop_movement(direction)

    def check_held_direction(self):
        """
        Checks whether any movement keys are currently pressed, and starts movement keys in that direction if so.
        """
        keys = pygame.key.get_pressed()

        for movement_key, direction in self.movement_keys.items():
            if (
                    (keys[pygame.K_RALT] or keys[pygame.K_LALT]) and
                    keys[movement_key] and renpy.store.pink_otm_alt_turning_enabled
            ):
                self.turn_player(direction)
            elif keys[movement_key]:
                self.start_movement(direction)

        controllers = _get_controllers()
        for controller in controllers:
            if not controller.get_init():
                controller.init()

        for controller in controllers:
            # Turning
            direction_dict = {}
            for movement_key, orientation in self.gamepad_turning_axis.items():
                axis_value = controller.get_axis(pygame.controller.get_axis_from_string(movement_key.encode('utf-8')))
                if axis_value > 10000 and orientation == "horizontal":
                    direction_dict[axis_value] = "right"
                elif axis_value > 10000 and orientation == "vertical":
                    direction_dict[axis_value] = "down"
                elif axis_value < -10000 and orientation == "horizontal":
                    direction_dict[abs(axis_value)] = "left"
                elif axis_value < -10000 and orientation == "vertical":
                    direction_dict[abs(axis_value)] = "up"
            if len(direction_dict) > 0:
                self.turn_player(direction_dict[max(direction_dict)])

            # Moving
            direction_dict = {}
            for movement_key, orientation in self.gamepad_movement_axis.items():
                axis_value = controller.get_axis(pygame.controller.get_axis_from_string(movement_key.encode('utf-8')))
                if axis_value > 10000 and orientation == "horizontal":
                    direction_dict[axis_value] = "right"
                elif axis_value > 10000 and orientation == "vertical":
                    direction_dict[axis_value] = "down"
                elif axis_value < -10000 and orientation == "horizontal":
                    direction_dict[abs(axis_value)] = "left"
                elif axis_value < -10000 and orientation == "vertical":
                    direction_dict[abs(axis_value)] = "up"
            if len(direction_dict) > 0:
                self.set_movement(direction_dict[max(direction_dict)])

    def stop_movement_all(self):
        """
        Stops the player's movement entirely.
        """
        new_control_stack = []
        for control in self.player_object.control_stack:
            if control.type in ("special_move", "go_to_smart", "execute_code"):
                # TODO starting to get many exceptions, maybe not great?
                new_control_stack.append(control)
        self.player_object.control_stack = new_control_stack
        self._direction_cache.stop_movement_all()

    def purge_non_special_move(self):
        """
        Removes all control commands that aren't special moves from the control stack.
        """
        new_control_stack = []
        for control in self.player_object.control_stack:
            if control.type == "special_move":
                new_control_stack.append(control)
        self.player_object.control_stack = new_control_stack

    def screen_pixels_to_map_pixels(self, x: int, y: int) -> Coord:
        # Calculates the offsets as created by the pink_otm_size_offset
        width: int = renpy.store.config.screen_width
        height: int = renpy.store.config.screen_height
        offset_x = max(
            int((width - (self.image_size.x * self.camera.xzoom)) / 2),
            self.camera.viewport_x_offset
        ) + self._overlay_manager.shake_x
        offset_y = max(
            int((height - (self.image_size.y * self.camera.yzoom)) / 2),
            self.camera.viewport_y_offset
        ) + self._overlay_manager.shake_y
        x_pixel = (self.camera.x.value + x - offset_x) / self.camera.xzoom
        y_pixel = (self.camera.y.value + y - offset_y) / self.camera.yzoom
        return Coord(x_pixel, y_pixel)

    def screen_pixels_to_map_coords(self, x: int, y: int) -> Coord:
        map_pixel = self.screen_pixels_to_map_pixels(x, y)

        x_coord = self.pixel_to_coord(map_pixel.x, is_x=True)
        y_coord = self.pixel_to_coord(map_pixel.y, is_x=False)
        return Coord(x_coord, y_coord)

    def process_mouse_turn_move(self, pc_coord: Coord, x: int, y: int):
        map_pixel = self.screen_pixels_to_map_pixels(x, y)
        x_in_coord = map_pixel.x - (self.tile_size.x * pc_coord.x)
        y_in_coord = map_pixel.y - (self.tile_size.y * pc_coord.y)

        self.purge_non_special_move()
        if x_in_coord < self.tile_size.x * 0.33:
            self.player_object.control_stack.append(ControlCommand("turn_left", never_repeat=True))
        elif x_in_coord > self.tile_size.x * 0.66:
            self.player_object.control_stack.append(ControlCommand("turn_right", never_repeat=True))

        elif y_in_coord < self.tile_size.y * 0.33:
            self.player_object.control_stack.append(ControlCommand("turn_up", never_repeat=True))
        elif y_in_coord > self.tile_size.y * 0.66:
            self.player_object.control_stack.append(ControlCommand("turn_down", never_repeat=True))

        self.player_object.control_stack.append(ControlCommand(
            "execute_code",
            code="renpy.store.pink_otm_current_map.player_interaction()", never_repeat=True))

    def process_mouse_hold_move(self, x, y):
        if pygame.mouse.get_pressed()[0] == 0 and self._mouse_state is not None:
            # Confirm that mouse is actually held.
            self.purge_non_special_move()
            self._mouse_state = None
            self._mouse_move_target_pixel = None
            self._mouse_move_target = None
            return
        # TODO compare pixels rather than coordinates?
        ms_coord = self.screen_pixels_to_map_coords(x, y)
        pc_coord = self.player_object.central_coord

        x_diff = abs(pc_coord.x - ms_coord.x)
        y_diff = abs(pc_coord.y - ms_coord.y)

        renpy.store.ms_coord = ms_coord
        renpy.store.pc_coord = pc_coord
        renpy.store.x_diff = x_diff
        renpy.store.y_diff = y_diff

        if x_diff == 0 and y_diff == 0:
            self.stop_movement_all()
            self.process_mouse_turn_move(pc_coord, x, y)
        else:
            self.purge_non_special_move()  # Reset control stack without interrupting special moves
            self.check_run()
            if x_diff >= y_diff:
                if pc_coord.x > ms_coord.x:
                    self.player_object.control_stack.append(ControlCommand("go_left", interact_on_fail=True))
                else:
                    self.player_object.control_stack.append(ControlCommand("go_right", interact_on_fail=True))
            else:
                if pc_coord.y > ms_coord.y:
                    self.player_object.control_stack.append(ControlCommand("go_up", interact_on_fail=True))
                else:
                    self.player_object.control_stack.append(ControlCommand("go_down", interact_on_fail=True))

    def interrupt_mouse_click_move(self):
        self.purge_non_special_move()
        self._mouse_state = None
        self._mouse_move_target_pixel = None
        self._mouse_move_target = None

    def process_mouse_click_move(self, x: int, y: int):
        if pygame.mouse.get_pressed()[0] == 0 and self._mouse_state is not None:
            # Confirm that mouse is actually held.
            self.interrupt_mouse_click_move()
            return
        coord = self.screen_pixels_to_map_coords(x, y)
        pc_coord = self.player_object.central_coord
        self._direction_cache.stop_movement_all()
        mouse_move_target = (coord.x, coord.y)
        if pc_coord == mouse_move_target:
            self.stop_movement_all()
            self.process_mouse_turn_move(coord, x, y)
        elif self._mouse_move_target != mouse_move_target:
            self.purge_non_special_move()  # Reset control stack without interrupting special moves
            self.check_run()
            self.player_object.control_stack.append(
                ControlCommand(
                    "go_to_smart",
                    target=(coord.x, coord.y), pop_invalid_move=True, never_repeat=True, max_path_length=30))
            self.player_object.control_stack.append(
                ControlCommand(
                    "execute_code", code="renpy.store.pink_otm_current_map.player_interaction()", never_repeat=True))
            self._mouse_move_target = mouse_move_target

    def click_on_map(self, ev, x, y, st):  # noqa
        self._mouse_state = 'click'  # TODO ENUM
        self._mouse_click_start = st
        self._mouse_move_target_pixel = (x, y)
        if renpy.store.pink_otm_mouse_click_move:
            self.process_mouse_click_move(x, y)
        elif renpy.store.pink_otm_mouse_held_move:
            self.process_mouse_hold_move(x, y)

    def unclick_on_map(self, ev, x, y, st):  # noqa
        self._mouse_state = None
        self._mouse_move_target_pixel = None
        self._mouse_move_target = None

    def player_interaction(self, ev=None, x=0, y=0, st=0.0):  # noqa
        """
        Executes an event where the interaction key is released. Checks whether there is any code or event to
        execute in the given location, and executes that code and/or event.
        """
        if hasattr(ev, "key"):
            event_button = 'keyboard', ev.key
        elif hasattr(ev, "button"):
            event_button = 'mouse', ev.button
        elif hasattr(ev, "controller"):
            event_button = 'controller', ev.controller
        else:
            event_button = 'unknown', None

        if renpy.store.pink_otm_current_event_type is None:
            self.check_activation_code()
            self.check_activation_event(event_button)
            if ev is not None:
                raise renpy.exports.IgnoreEvent()

    def disable_controls(self):
        """
        Stops all movement and disables controls
        """
        self.stop_movement_all()
        self.controls_enabled = False

    def enable_controls(self):
        """
        Enables controls
        """
        self.controls_enabled = True

    def end_all_interactions(self):
        """
        Ends the interactions on all Mobile Objects on this map.
        """
        for mobile_object in self.mobile_objects:
            if mobile_object.currently_interacting:
                mobile_object.end_interaction()

    def freeze_map(self):
        """
        Freezes the map, making all objects stop dead in their tracks and all animations halt.
        """
        for mobile_object in self.mobile_objects:
            mobile_object.freeze()
        for animated_tile in self.animated_tiles:
            animated_tile.pause_animation()

    def unfreeze_map(self, increment_gt=True):
        """
        Unfreezes the map, making all objects continue where they stopped, and restarts animations
        :param bool increment_gt: If True, increments the gt of all mobile and animated objects, as well as parallel
        processes, to account for the amount of time they were frozen.
        """
        for mobile_object in self.mobile_objects:
            mobile_object.unfreeze(increment_gt=increment_gt)
        for animated_tile in self.animated_tiles:
            animated_tile.unpause_animation()

    def halt_map(self):
        """
        Saves the position of all objects on the map, and halts them, as well as blocking player controls. Intended
        to be used for labels with movements (such as cutscenes).
        """
        for mobile_object in self.mobile_objects:
            if mobile_object is not self.player_object:
                mobile_object.save_and_halt()

    def unhalt_map(self):
        """
        Restores all sprites to the location they were saved from.
        """
        for mobile_object in self.mobile_objects:
            if mobile_object is not self.player_object and mobile_object not in renpy.store.pink_otm_followers:
                mobile_object.load_and_continue()

    def halt_player(self):
        self.player_object.force_stand()
        self.stop_running()
        self.player_object.movement_speed = self._pc_walk_speed

        for follower in renpy.store.pink_otm_followers:
            follower.movement_speed = self._pc_walk_speed

    def is_coord_impassible(self, x_coord, y_coord):
        """
        :return: True if the given coordinate is impassible (movement to rules equal to 0000)
        :param int x_coord: The x of the given coord
        :param int y_coord: The y of the given coord
        """
        return self.base_grid.get_move_to(x_coord=x_coord, y_coord=y_coord) == "0000"

    @staticmethod
    def get_follower(image_path: str) -> Optional[OrthogonalTiledMapGameObjectSpriteCollection]:
        """Left for compatibility purposes"""
        return get_follower(image_path)

    @property
    def background_music(self):
        """
        :return: The background music track to play for this map, or whether to 'continue' the background music of the
        previous map or whether to 'stop' the currently playing background music.
        :rtype: str
        """
        if 'background_music' in self.properties:
            return self.properties['background_music']
        else:
            return "continue"

    @property
    def background_ambience(self):
        """
        :return: The background ambience track to play for this map, or whether to 'continue' the background ambience
        of the previous map or whether to 'stop' the currently playing background ambience.
        :rtype: str
        """
        if 'background_ambience' in self.properties:
            return self.properties['background_ambience']
        else:
            return "stop"

    @property
    def forbid_run(self):
        """
        :return: Whether running is forbidden on this map
        :rtype: bool
        """
        if 'forbid_run' in self.properties:
            return self.properties['forbid_run']
        else:
            return False

    @property
    def force_run(self):
        """
        :return: Whether running is forced on this map
        :rtype: bool
        """
        if 'force_run' in self.properties:
            return self.properties['force_run']
        else:
            return False

    @property
    def code_on_enter(self):
        """
        :return: The code (in string form) that should run on entering this map.
        :rtype: str|None
        """
        if 'code_on_enter' in self.properties:
            return self.properties['code_on_enter']
        else:
            return None

    def run_code_on_enter(self):
        """
        Runs the code_on_enter on this map
        """
        if self.code_on_enter is not None:
            exec(self.code_on_enter)

    @property
    def code_on_leave(self):
        """
        :return: The code (in string form) that should run on leaving this map.
        :rtype: str|None
        """
        if 'code_on_leave' in self.properties:
            return self.properties['code_on_leave']
        else:
            return None

    def run_code_on_leave(self):
        """
        Runs the code_on_leave on this map
        """
        if self.code_on_leave is not None:
            exec(self.code_on_leave)

    def add_overlay_image(
            self,
            image_name: str,
            fade_time: float = 0.0,
            alpha: float = 1.0,
            x: int = 0,
            y: int = 0,
            width: int = renpy.store.config.screen_width,
            height: int = renpy.store.config.screen_height,
            target_x: Optional[int] = None,
            target_y: Optional[int] = None,
            target_width: Optional[int] = None,
            target_height: Optional[int] = None,
            move_time: float = 0.0,
            consistent: bool = False,
            x_arc: int = 0,
            y_arc: int = 0
    ) -> OverlayImage:
        """
        Adds and returns an overlay that shows an image
        :param image_name: the filepath for the image to be shown.
        :param fade_time: The amount of time in seconds the overlay takes to fade to its target alpha. If 0.0, no
        fade takes place, but the overlay instantly transitions.
        :param alpha: The alpha value the overlay should have at the end of its fade. 0.0 for completely transparent,
        1.0 for 100% visible.
        :param consistent: Whether or not the overlay lasts between maps.
        :param x: Starting x in pixels
        :param y: Starting y in pixels
        :param width: Starting width in pixels
        :param height: Starting height in pixels
        :param target_x: If set, makes it so the overlay starts out as moving, transitioning from the starting x to
        the target x
        :param target_y: If set, makes it so the overlay starts out as moving, transitioning from the starting y to
        the target y
        :param target_width: If set, makes it so the overlay starts out as moving, transitioning from the starting width
        to the target width
        :param target_height: If set, makes it so the overlay starts out as moving, transitioning from the starting
        height to the target height
        :param move_time: The amount of time in seconds it should take to transition between the start_dimensions and
        target_dimensions.
        :param x_arc: If set to a value other than 0, adds horizontal arcing to the movement from start_dimensions to
        target_dimensions. The arcing is parabolic, with the greatest extent being the value of x_arc.
        :param y_arc: If set to a value other than 0, adds vertical arcing to the movement from start_dimensions to
        target_dimensions. The arcing is parabolic, with the greatest extent being the value of y_arc.
        """
        return self._overlay_manager.add_overlay_image(
            image_name=image_name, fade_time=fade_time, alpha=alpha, x=x, y=y, width=width, height=height,
            target_x=target_x, target_y=target_y, target_width=target_width, target_height=target_height,
            move_time=move_time, consistent=consistent, x_arc=x_arc, y_arc=y_arc)

    def add_overlay_text(
            self,
            text: str,
            fade_time: float = 0.0,
            alpha: float = 1.0,
            x: int = 0,
            y: int = 0,
            width: int = renpy.store.config.screen_width,
            height: int = renpy.store.config.screen_height,
            target_x: Optional[int] = None,
            target_y: Optional[int] = None,
            target_width: Optional[int] = None,
            target_height: Optional[int] = None,
            move_time: float = 0.0,
            consistent: bool = False,
            autosize: bool = True,
            x_arc: int = 0,
            y_arc: int = 0
    ) -> OverlayText:
        """
        Adds and returns an overlay that shows text
        :param text: The text to show in this overlay. Can include ren'py formatting.
        :param fade_time: The amount of time in seconds the overlay takes to fade to its target alpha. If 0.0, no
        fade takes place, but the overlay instantly transitions.
        :param alpha: The alpha value the overlay should have at the end of its fade. 0.0 for completely transparent,
        1.0 for 100% visible.
        :param consistent: Whether or not the overlay lasts between maps.
        :param x: Starting x in pixels
        :param y: Starting y in pixels
        :param width: Starting width in pixels
        :param height: Starting height in pixels
        :param target_x: If set, makes it so the overlay starts out as moving, transitioning from the starting x to
        the target x
        :param target_y: If set, makes it so the overlay starts out as moving, transitioning from the starting y to
        the target y
        :param target_width: If set, makes it so the overlay starts out as moving, transitioning from the starting width
        to the target width
        :param target_height: If set, makes it so the overlay starts out as moving, transitioning from the starting
        height to the target height
        :param move_time: The amount of time in seconds it should take to transition between the start_dimensions and
        target_dimensions.
        :param autosize: Whether to autosize this overlay. If True, automatically sets the width and height of this
        overlay to be that of the underlying text at 1.0 zoom, preventing any stretching.
        :param x_arc: If set to a value other than 0, adds horizontal arcing to the movement from start_dimensions to
        target_dimensions. The arcing is parabolic, with the greatest extent being the value of x_arc.
        :param y_arc: If set to a value other than 0, adds vertical arcing to the movement from start_dimensions to
        target_dimensions. The arcing is parabolic, with the greatest extent being the value of y_arc.
        """
        return self._overlay_manager.add_overlay_text(
            text=text, fade_time=fade_time, alpha=alpha, x=x, y=y, width=width, height=height, target_x=target_x,
            target_y=target_y, target_width=target_width, target_height=target_height, move_time=move_time,
            consistent=consistent, autosize=autosize, x_arc=x_arc, y_arc=y_arc)

    def add_overlay_solid(
            self,
            color: str,
            fade_time: float = 0.0,
            alpha: float = 1.0,
            x: int = 0,
            y: int = 0,
            width: int = renpy.store.config.screen_width,
            height: int = renpy.store.config.screen_height,
            target_x: Optional[int] = None,
            target_y: Optional[int] = None,
            target_width: Optional[int] = None,
            target_height: Optional[int] = None,
            move_time: float = 0.0,
            consistent: bool = False,
            x_arc: int = 0,
            y_arc: int = 0
    ) -> OverlaySolid:
        """
        Adds and returns an overlay that shows a solid color
        :param color: the color (has the format '#rrggbb').
        :param fade_time: The amount of time in seconds the overlay takes to fade to its target alpha and color. If 0.0,
        no fade takes place, but the overlay instantly transitions.
        :param alpha: The alpha value the overlay should have at the end of its fade. 0.0 for completely transparent,
        1.0 for 100% visible.
        :param consistent: Whether or not the overlay lasts between maps.
        :param x: Starting x in pixels
        :param y: Starting y in pixels
        :param width: Starting width in pixels
        :param height: Starting height in pixels
        :param target_x: If set, makes it so the overlay starts out as moving, transitioning from the starting x to
        the target x
        :param target_y: If set, makes it so the overlay starts out as moving, transitioning from the starting y to
        the target y
        :param target_width: If set, makes it so the overlay starts out as moving, transitioning from the starting width
        to the target width
        :param target_height: If set, makes it so the overlay starts out as moving, transitioning from the starting
        height to the target height
        :param move_time: The amount of time in seconds it should take to transition between the start_dimensions and
        target_dimensions.
        :param x_arc: If set to a value other than 0, adds horizontal arcing to the movement from start_dimensions to
        target_dimensions. The arcing is parabolic, with the greatest extent being the value of x_arc.
        :param y_arc: If set to a value other than 0, adds vertical arcing to the movement from start_dimensions to
        target_dimensions. The arcing is parabolic, with the greatest extent being the value of y_arc.
        """
        return self._overlay_manager.add_overlay_solid(
            color=color, fade_time=fade_time, alpha=alpha, x=x, y=y, width=width, height=height, target_x=target_x,
            target_y=target_y, target_width=target_width, target_height=target_height, move_time=move_time,
            consistent=consistent, x_arc=x_arc, y_arc=y_arc)

    def add_screen_shaker(
            self,
            duration: float,
            frequency: float,
            x_amp: int = 0,
            y_amp: int = 0,
            phase: float = 0.0
    ) -> None:
        """
        Adds a screen shaking effect
        :param duration: How long the shake should last, in seconds.
        :param frequency: The frequency in shakes per seconds
        :param x_amp: The amplitude of the x axis in pixels.
        :param y_amp: The amplitude of the y axis in pixels.
        :param phase: The starting phase of the shake, in radians.
        """
        return self._overlay_manager.add_screen_shaker(
            duration=duration, frequency=frequency, x_amp=x_amp, y_amp=y_amp, phase=phase)

    @staticmethod
    def remove_overlay(overlay: Overlay, fade_time: float = 0.0) -> None:
        """
        Removes the target overlay. Note that it technically doesn't remove, it just makes invisible.
        :param overlay: the overlay to make invisible.
        :param fade_time: The amount of time the removal should take, with the overlay fading away. If 0.0 (the
        default), no fade takes place, and the overlay is removed instantly.
        """
        OverlayManager.remove_overlay(overlay=overlay, fade_time=fade_time)

    def remove_all_overlays(self, fade_time: float = 0.0) -> None:
        """
        Removes all overlays. Note that it technically doesn't remove, it just makes invisible.
        :param fade_time: The amount of time the removal should take, with the overlays fading away. If 0.0 (the
        default), no fade takes place, and the overlays are removed instantly.
        """
        self._overlay_manager.remove_all_overlays(fade_time=fade_time)

    def stop_shaking(self) -> None:
        """
        Instantly stops and deletes all ScreenShakers.
        """
        self._overlay_manager.stop_shaking()

    @property
    def is_shaking(self) -> bool:
        """
        Returns True if there are any Screen Shakers still in existence.
        """
        return self._overlay_manager.is_shaking

    @property
    def zoom(self):
        return self.properties.get('zoom', None)

    @property
    def x_zoom(self):
        return self.properties.get('x_zoom', self.zoom)

    @property
    def y_zoom(self):
        return self.properties.get('y_zoom', self.zoom)


class StartMapEvent(object):
    def __init__(self, condition, event, priority, triggering_object, event_args, event_kwargs):
        self.condition = condition
        self.event = event
        self.priority = priority
        self.object = triggering_object
        self.args = event_args
        self.kwargs = event_kwargs

    @property
    def condition_met(self):
        return eval(self.condition)


class StartMapEvents(object):
    def __init__(self):
        self.data: Dict[str, StartMapEvent] = {}

        # The ID to use in the next auto-generated condition_id.
        self._next_id_nr = 0

    @classmethod
    def get_current_instance(cls, game_map=None):
        """
        Retrieves the current instance of the class on the given map. If None, will use the map currently being loaded
        if such a map exists, otherwise will target the current map.
        :param OrthogonalTiledMap game_map: the given game map
        """
        if game_map is None:
            if renpy.store.pink_otm_loading_map is not None:
                game_map = renpy.store.pink_otm_loading_map   # type: OrthogonalTiledMap
            else:
                game_map = renpy.store.pink_otm_current_map
        return game_map.start_map_events

    @classmethod
    def add_event(
            cls, event, triggering_object=None, condition=None, priority=0, condition_id=None, game_map=None,
            event_args=None, event_kwargs=None
    ):
        current_instance = cls.get_current_instance(game_map)  # type: StartMapEvents

        if condition_id is None:
            condition_id = cls.get_next_auto_id(game_map=game_map)

        if condition is None:
            condition = 'True'
        if triggering_object is None:
            triggering_object = ""
        if event_args is None:
            event_args = []
        if event_kwargs is None:
            event_kwargs = {}

        current_instance.data[condition_id] = StartMapEvent(
            condition=condition,
            event=event,
            priority=priority,
            triggering_object=triggering_object,
            event_args=event_args,
            event_kwargs=event_kwargs)

    @classmethod
    def get_start_map_event(cls, game_map=None):
        current_instance = cls.get_current_instance(game_map)  # type: StartMapEvents

        for start_map_event in sorted(current_instance.data.values(), key=cls.get_priority):  # py2
            if start_map_event.condition_met:
                return start_map_event

    @staticmethod
    def get_priority(start_map_event):  # necessary for sorting, remove on python version update
        return start_map_event.priority

    @classmethod
    def get_next_auto_id(cls, game_map=None):
        """
        Generates the next auto-generated condition ID.
        :param OrthogonalTiledMap game_map: The map for which to perform this operation. Defaults to the map being
        loaded, or the map that is on screen if no map is being loaded. Will almost never have to be specified.
        """
        current_instance = cls.get_current_instance(game_map)  # type: StartMapEvents
        next_auto_id = "auto_id_" + str(current_instance._next_id_nr)
        current_instance._next_id_nr += 1
        return next_auto_id


class ParallelProcess(object):
    process_id = ""

    def __init__(self):
        """
        This class represents a Parallel Process, a process which runs in parallel to the current pink engine map.
        Each parallel process has a 'per_tick' process, which is called before the rendering of each frame of the
        pink engine map.
        """
        self.paused = False
        self.last_gt = 0.0

    def pause(self):
        """
        Pauses this parallel process.
        """
        self.paused = True

    def unpause(self):
        """
        Unpauses this parallel process.
        """
        self.paused = False

    def increment_gt(self, gt_diff):
        """
        Increments the GT for timing-sensitive parallel processes
        :param float gt_diff: the quantity of time by which to increment the gt
        """
        pass  # implemented in sub-classes

    @classmethod
    def exists(cls, game_map):
        """
        Returns True if a parallel process with this id already exists for the given map
        :param OrthogonalTiledMap game_map: The given map
        :rtype: bool
        """
        if (
                cls.process_id in game_map.parallel_processes):
            return True
        else:
            return False

    @classmethod
    def ensure_existence(cls, game_map):
        """
        Ensures an instance of the class exists on the given map.
        :param OrthogonalTiledMap game_map: the given game map
        """
        if not cls.exists(game_map):
            game_map.parallel_processes[cls.process_id] = cls()

    @classmethod
    def get_current_instance(cls, game_map=None):
        """
        Retrieves the current instance of the class on the given map. If None, will use the map currently being loaded
        if such a map exists, otherwise will target the current map.
        :param OrthogonalTiledMap game_map: the given game map
        """
        if game_map is None:
            if renpy.store.pink_otm_loading_map is not None:   # type: OrthogonalTiledMap
                game_map = renpy.store.pink_otm_loading_map
            else:
                game_map = renpy.store.pink_otm_current_map
        cls.ensure_existence(game_map)
        return game_map.parallel_processes[cls.process_id]

    @staticmethod
    def _get_areas(
            start_x, end_x, start_y, end_y,
            trans_start_x=None, trans_end_x=None, trans_start_y=None, trans_end_y=None,
            trans_radius=None
    ):
        """
        Retrieves the area and transition area that define an area for the purpose of a parallel process. If no
        transition-related variables are given, the transition area and main area will be the same.
        :param int start_x: Starting x coord of the area.
        :param int end_x: final x coord of the area
        :param int start_y: starting y coord of the area
        :param int end_y: final y coord of the area
        :param int trans_start_x: Starting x coord of the transition area. Overrides trans_radius if given.
        :param int trans_end_x: final x coord of the transition area. Overrides trans_radius if given.
        :param int trans_start_y: starting y coord of the transition area. Overrides trans_radius if given.
        :param int trans_end_y: final y coord of the transition area. Overrides trans_radius if given.
        :param int trans_radius: Places the transition area around the main area with the given extra radius. Using
        any of the other transition-related variables will override the radius for that side only.
        :rtype: tuple
        """
        if trans_start_x is None:
            if trans_radius is not None:
                trans_start_x = start_x - trans_radius
            else:
                trans_start_x = start_x
        if trans_end_x is None:
            if trans_radius is not None:
                trans_end_x = end_x + trans_radius
            else:
                trans_end_x = end_x
        if trans_start_y is None:
            if trans_radius is not None:
                trans_start_y = start_y - trans_radius
            else:
                trans_start_y = start_y
        if trans_end_y is None:
            if trans_radius is not None:
                trans_end_y = end_y + trans_radius
            else:
                trans_end_y = end_y
        return Area(start_x, end_x, start_y, end_y), Area(trans_start_x, trans_end_x, trans_start_y, trans_end_y)

    def per_tick(self, gt):
        """
        Runs this parallel process for a single frame. Implemented in sub-classes.
        :param float gt: the frame's game time in seconds.
        """
        self.last_gt = gt

    def on_init(self):
        """
        Runs any code that needs to run after finishing the initialization of the map. Implemented in sub-classes.
        """
        pass


class SmoothZoomController(ParallelProcess):
    process_id = "smooth_zoom_controller"

    def __init__(self):
        """
        This class represents the parallel process that allows for smooth camera zooms.
        """
        ParallelProcess.__init__(self)

        # Smooth zoom-related variables
        self.original_xzoom = renpy.store.pink_otm_camera_current_xzoom  # type: float
        self.target_xzoom = renpy.store.pink_otm_camera_current_xzoom  # type: float
        self.original_yzoom = renpy.store.pink_otm_camera_current_yzoom  # type: float
        self.target_yzoom = renpy.store.pink_otm_camera_current_yzoom  # type: float
        self.start_zoom_gt = 0.0
        self.zoom_speed = 1.0  # Time in seconds to complete the zoom

    def on_init(self):
        renpy.store.pink_otm_zoom_controller = self

    def per_tick(self, gt):
        if not self.paused:
            pink_otm_current_camera = renpy.store.pink_otm_current_camera

            if pink_otm_current_camera.xzoom != self.target_xzoom:
                if self.start_zoom_gt > gt:
                    self.start_zoom_gt = 0.00001
                gt_diff = gt - self.start_zoom_gt
                gt_fraction = min(1.0, gt_diff / self.zoom_speed)
                new_xzoom = self.original_xzoom - (self.original_xzoom - self.target_xzoom) * gt_fraction
                pink_otm_current_camera.xzoom = new_xzoom
                pink_otm_current_camera.x.range = \
                    renpy.store.pink_otm_current_map.image_size.x * new_xzoom - pink_otm_current_camera.viewport_width
                renpy.store.pink_otm_camera_current_xzoom = new_xzoom

            if pink_otm_current_camera.yzoom != self.target_yzoom:
                if self.start_zoom_gt > gt:
                    self.start_zoom_gt = 0.00001
                gt_diff = gt - self.start_zoom_gt
                gt_fraction = min(1.0, gt_diff / self.zoom_speed)
                new_yzoom = self.original_yzoom - (self.original_yzoom - self.target_yzoom) * gt_fraction
                pink_otm_current_camera.yzoom = new_yzoom
                pink_otm_current_camera.y.range = \
                    renpy.store.pink_otm_current_map.image_size.y * new_yzoom - pink_otm_current_camera.viewport_height
                renpy.store.pink_otm_camera_current_yzoom = new_yzoom

        ParallelProcess.per_tick(self, gt)


class ConditionalEventTriggers(ParallelProcess):
    process_id = "conditional_event_triggers"

    def __init__(self):
        """
        This class represents the parallel process that triggers events when specified conditions are met.
        """
        ParallelProcess.__init__(self)

        # Indexed elements that can be removed
        self.id_data = {}

        # Non-indexed elements that cannot be removed.
        self.other_data = []

    @classmethod
    def add_condition(cls, condition, event_name, game_map=None, event_args=None, event_kwargs=None, condition_id=None):
        """
        Adds the given condition for triggering the given event to the given map. Only one event can be triggered
        for any condition, and adding a new event with identical conditions will override the previous event for
        that condition.
        :param OrthogonalTiledMap game_map: The given map
        :param str condition: The given conditions.
        :param str event_name: The name of the event to call when conditions are met.
        :param list event_args: A list of additional arguments to pass when calling the event
        :param dict event_kwargs: A dict of additional arguments to pass when calling the event.
        :param str condition_id: the ID to use for the condition, to target it for removal. If no id is given, the
        condition cannot be removed.
        """
        if event_args is None:
            event_args = []
        if event_kwargs is None:
            event_kwargs = {}
        event_tuple = (condition, event_name, event_args, event_kwargs)

        if condition_id is not None:
            cls.get_current_instance(game_map).id_data[condition_id] = event_tuple
        else:
            cls.get_current_instance(game_map).other_data.append(event_tuple)

    @classmethod
    def drop_condition(cls, condition_id, game_map=None):
        """
        Drops the arbitrary event trigger with the given condition id from the given map.
        :param OrthogonalTiledMap game_map: The given map
        :param str condition_id: The given condition ID.
        """
        cls.get_current_instance(game_map).data.pop(condition_id)

    @staticmethod
    def _evaluate_condition(condition, event_name, event_args, event_kwargs):
        """
        Calls the event with the given name, with the given args and kwargs, if the condition is met.
        :param str condition: The given condition.
        :param str event_name: The given event name.
        :param list event_args: The given list of arguments to pass to the event.
        :param dict event_kwargs: The given list of keyword arguments to pass to the event.
        """
        if eval(condition):
            renpy.store.pink_otm_current_map.trigger_event(
                event_name, "", *event_args, **event_kwargs)

    def per_tick(self, gt):
        """
        Runs this parallel process for a single frame
        :param float gt: the frame's game time in seconds.
        """
        if not self.paused and renpy.store.pink_otm_current_event_name is None:
            for condition, event_name, event_args, event_kwargs in self.id_data.values():
                self._evaluate_condition(condition, event_name, event_args, event_kwargs)
            for condition, event_name, event_args, event_kwargs in self.other_data:
                self._evaluate_condition(condition, event_name, event_args, event_kwargs)
        ParallelProcess.per_tick(self, gt)


class ConditionalCodeTriggers(ParallelProcess):
    process_id = "conditional_code_triggers"

    def __init__(self):
        """
        This class represents the parallel process that runs code when specified conditions are met.
        """
        ParallelProcess.__init__(self)

        # Indexed elements that can be removed
        self.id_data = {}

        # Non-indexed elements that cannot be removed.
        self.other_data = []

    @classmethod
    def add_condition(cls, condition, event_code, game_map=None, condition_id=None):
        """
        Adds a trigger for running a given bit of code once a given condition is met on a given map.
        :param OrthogonalTiledMap game_map: The given map.
        :param str condition: The condition under which the code executes.
        :param str event_code: The code to execute once conditions are met.
        :param str condition_id: The ID to use for the condition, allowing the condition to be removed by other
        scripts.
        """
        condition_tuple = (condition, event_code)
        if condition_id is not None:
            cls.get_current_instance(game_map).id_data[condition_id] = condition_tuple
        else:
            cls.get_current_instance(game_map).other_data.append(condition_tuple)

    @classmethod
    def drop_condition(cls, condition_id, game_map=None):
        """
        Removes the condition with the given ID from the given map.
        :param OrthogonalTiledMap game_map: The given map
        :param str condition_id: the given map.
        """
        cls.get_current_instance(game_map).id_data.pop(condition_id)

    @staticmethod
    def _evaluate_condition(condition, code):
        """
        Evaluates the given condition and executes the given code if it is met.
        :param str condition: The given condition.
        :param str code: The given code.
        """
        if eval(condition):
            exec(code)

    def per_tick(self, gt):
        """
        Runs this parallel process for a single frame
        :param float gt: the frame's game time in seconds.
        """
        if not self.paused:
            for condition, event_code in self.id_data.values():
                self._evaluate_condition(condition, event_code)
            for condition, event_code in self.other_data:
                self._evaluate_condition(condition, event_code)
        ParallelProcess.per_tick(self, gt)


class SoundPlayAreas(ParallelProcess):
    process_id = "sound_play_areas"

    def __init__(self):
        """
        This class represents the parallel process that changes the background music when areas are entered.
        """
        ParallelProcess.__init__(self)

        # Indexed elements that can be removed
        self.id_data = {}

        # Non-indexed elements that cannot be removed.
        self.other_data = []

        # Background music defaults to map background music, default channel defaults to 'music'
        self.channel_defaults = {}

    @classmethod
    def add_area(cls, sound_path, start_x, end_x, start_y, end_y, channel="music", game_map=None, area_id=None):
        """
        Adds a new area to this parallel process.
        :param str sound_path: The path to the track to play on the given channel when this area is entered. In
        addition to paths, this also recognizes the 'stop' and 'continue' commands. 'stop' will make the music stop,
        'continue' will make the music from the previous area continue playing.
        :param int start_x: The starting X coord of this area.
        :param int end_x: The final X coord of this area.
        :param int start_y: The starting Y coord of this area.
        :param int end_y: The final Y coord of this area.
        :param str channel: The channel on which to play the given music.
        :param OrthogonalTiledMap game_map: The map for which to perform this operation. Defaults to the map being
        loaded, or the map that is on screen if no map is being loaded. Will almost never have to be specified.
        :param str area_id: the id under which to index the area, by which it can be targeted for removal. If no
        area_id is given, this area cannot be removed by later code.
        """
        area_tuple = (Area(start_x, end_x, start_y, end_y), sound_path, channel)

        if area_id is not None:
            cls.get_current_instance(game_map).id_data[area_id] = area_tuple
        else:
            cls.get_current_instance(game_map).other_data.append(area_tuple)

    @classmethod
    def drop_area(cls, area_id, game_map=None):
        """
        Drops the area with the given ID from this parallel process.
        :param str area_id: the given ID.
        :param OrthogonalTiledMap game_map: The map for which to perform this operation. Defaults to the map being
        loaded, or the map that is on screen if no map is being loaded. Will almost never have to be specified.
        """
        cls.get_current_instance(game_map).id_data.pop(area_id)

    @classmethod
    def set_default(cls, sound_path, channel="music", game_map=None):
        """
        Sets the default sound track for the given channel.
        :param str sound_path: The path to the track to play on the given channel by default In
        addition to paths, this also recognizes the 'stop' and 'continue' commands. 'stop' will make the music stop,
        'continue' will make the music from the previous area continue playing.
        :param str channel: The given channel.
        :param OrthogonalTiledMap game_map: The map for which to perform this operation. Defaults to the map being
        loaded, or the map that is on screen if no map is being loaded. Will almost never have to be specified.
        """
        cls.get_current_instance(game_map).channel_defaults[channel] = sound_path

    @classmethod
    def drop_default(cls, channel, game_map=None):
        """
        Drops the default sound track for the given channel.
        :param str channel: The given channel.
        :param OrthogonalTiledMap game_map: The map for which to perform this operation. Defaults to the map being
        loaded, or the map that is on screen if no map is being loaded. Will almost never have to be specified.
        """
        cls.get_current_instance(game_map).channel_defaults.pop(channel)

    @staticmethod
    def _handle_area(pc_coords, area, sound_path, channel):
        """
        Handles the per-tick operations for a single area.
        :param Coord pc_coords: The current central coord of the player character.
        :param Area area: the area to handle per call.
        :param str sound_path: The sound_path for this area.
        :param str channel: The channel to which this area applies.
        """
        if in_area(pc_coords, area):
            if sound_path == "stop":
                renpy.exports.music.stop(channel=channel)
                return channel
            elif sound_path == "continue":
                return channel
            else:
                renpy.exports.music.play(sound_path, loop=True, if_changed=True, channel=channel)
                return channel

    def per_tick(self, gt):
        """
        Per-tick operations for this parallel process. Will check every area to see whether the player is currently
        inside them, playing the music if so. Then, if the player is not inside any areas for a channel that has a
        default set, this function will execute that default.
        :param float gt: the game time in seconds.
        """
        if not self.paused:
            pink_otm_current_pc = renpy.store.pink_otm_current_pc  # type: OrthogonalTiledMapGameObjectSpriteCollection
            pc_coords = pink_otm_current_pc.central_coord

            # Channels that the player is in zones for during this tick.
            tick_channels = set()

            for area, sound_path, channel in self.id_data.values():
                channel = self._handle_area(pc_coords, area, sound_path, channel)
                if channel:
                    tick_channels.add(channel)
            for area, sound_path, channel in self.other_data:
                channel = self._handle_area(pc_coords, area, sound_path, channel)
                if channel:
                    tick_channels.add(channel)

            # Only reaches this bit if current player area corresponds to no set area.
            for channel, sound_path in self.channel_defaults.items():
                if channel not in tick_channels:
                    # Channel does not have a zone this tick, resorting to default behavior.
                    if sound_path == "continue":
                        continue
                    elif sound_path == "stop":
                        renpy.exports.music.stop(channel=channel)
                    else:
                        renpy.exports.music.play(sound_path, loop=True, if_changed=True, channel=channel)

        ParallelProcess.per_tick(self, gt)


class SoundPanAreas(ParallelProcess):
    process_id = "sound_pan_areas"

    def __init__(self):
        """
        This class represents the parallel process that changes the panning on specified channels when areas are
        entered.
        """
        ParallelProcess.__init__(self)

        # Indexed elements that can be removed
        self.id_data = {}

        # Non-indexed elements that cannot be removed.
        self.other_data = []

        # Background music defaults to map background music, default channel defaults to 'music'
        self.channel_defaults = {}

    @classmethod
    def add_area(
            cls, pan_level, start_x, end_x, start_y, end_y,
            trans_start_x=None, trans_end_x=None, trans_start_y=None, trans_end_y=None,
            trans_radius=None,
            channel="music", game_map=None, area_id=None
    ):
        """
        Adds a new area to this Parallel process.
        :param float pan_level: The pan level to maintain in this area. A pan of 1.0 is all the way to the right, a
        pan of -1.0 is all the way to the left.
        :param int start_x: Starting x coord of the area.
        :param int end_x: final x coord of the area
        :param int start_y: starting y coord of the area
        :param int end_y: final y coord of the area
        :param int trans_start_x: Starting x coord of the transition area. Overrides trans_radius if given.
        :param int trans_end_x: final x coord of the transition area. Overrides trans_radius if given.
        :param int trans_start_y: starting y coord of the transition area. Overrides trans_radius if given.
        :param int trans_end_y: final y coord of the transition area. Overrides trans_radius if given.
        :param int trans_radius: Places the transition area around the main area with the given extra radius. Using
        any of the other transition-related variables will override the radius for that side only.
        :param str channel: The sound channel which this area affects.
        :param OrthogonalTiledMap game_map: The map for which to perform this operation. Defaults to the map being
        loaded, or the map that is on screen if no map is being loaded. Will almost never have to be specified.
        :param str area_id: the id under which to index the area, by which it can be targeted for removal. If no
        area_id is given, this area cannot be removed by later code.
        """
        full_area, trans_area = cls._get_areas(
            start_x, end_x, start_y, end_y, trans_start_x, trans_end_x, trans_start_y, trans_end_y, trans_radius)
        area_tuple = (pan_level, full_area, trans_area, channel)

        if area_id is not None:
            cls.get_current_instance(game_map).id_data[area_id] = area_tuple
        else:
            cls.get_current_instance(game_map).other_data.append(area_tuple)

    @classmethod
    def drop_area(cls, area_id, game_map=None):
        """
        Drops the area with the given ID from this parallel process.
        :param str area_id: the given ID.
        :param OrthogonalTiledMap game_map: The map for which to perform this operation. Defaults to the map being
        loaded, or the map that is on screen if no map is being loaded. Will almost never have to be specified.
        """
        cls.get_current_instance(game_map).id_data.pop(area_id)

    @classmethod
    def set_default(cls, pan_level, channel="music", game_map=None):
        """
        Sets the default pan for the given channel.
        :param float pan_level: The pan level to maintain by default.
        :param str channel: The given channel.
        :param OrthogonalTiledMap game_map: The map for which to perform this operation. Defaults to the map being
        loaded, or the map that is on screen if no map is being loaded. Will almost never have to be specified.
        """
        cls.get_current_instance(game_map).channel_defaults[channel] = pan_level

    @classmethod
    def drop_default(cls, channel, game_map=None):
        """
        Drops the default sound pan for the given channel.
        :param str channel: The given channel.
        :param OrthogonalTiledMap game_map: The map for which to perform this operation. Defaults to the map being
        loaded, or the map that is on screen if no map is being loaded. Will almost never have to be specified.
        """
        cls.get_current_instance(game_map).channel_defaults.pop(channel)

    def _handle_area(self, pc_coords, full_area, trans_area, pan_level, channel):
        """
        Handles the per-tick operations for a single area.
        :param Coord pc_coords: The current central coord of the player character.
        :param Area full_area: the full area for this pan level.
        :param Area trans_area: the transition area for this pan level.
        :param float pan_level: The pan level for this area.
        :param str channel: The channel to which this area applies.
        """
        if in_area(pc_coords, full_area):
            # In full area, meaning full pan setting is in effect
            renpy.exports.music.set_pan(pan_level, delay=0.1, channel=channel)
            return channel
        elif in_area(pc_coords, trans_area):
            # In transition area, meaning total panning depends on relative position
            trans_ratio = get_trans_ratio(pc_coords, full_area, trans_area)
            channel_default = 0.5 if channel not in self.channel_defaults else self.channel_defaults[channel]

            final_pan = channel_default + (pan_level - channel_default) * trans_ratio
            renpy.exports.music.set_pan(final_pan, delay=0.1, channel=channel)
            return channel

    def per_tick(self, gt):
        """
        Per-tick operations for this parallel process. Will check every area to see whether the player is currently
        inside them or their transition areas, setting the pan appropriately if so. Then, if the player is not inside
        any areas for a channel that has a default set, this function will execute that default.
        :param float gt: the game time in seconds.
        """
        if not self.paused:
            pink_otm_current_pc = renpy.store.pink_otm_current_pc  # type: OrthogonalTiledMapGameObjectSpriteCollection
            pc_coords = pink_otm_current_pc.central_coord

            # Channels that the player is in zones for during this tick.
            tick_channels = set()

            for pan_level, full_area, trans_area, channel in self.id_data.values():
                channel = self._handle_area(pc_coords, full_area, trans_area, pan_level, channel)
                if channel:
                    tick_channels.add(channel)
            for pan_level, full_area, trans_area, channel in self.other_data:
                channel = self._handle_area(pc_coords, full_area, trans_area, pan_level, channel)
                if channel:
                    tick_channels.add(channel)

            # Only reaches this bit if current player area corresponds to no set area.
            for channel, pan_level in self.channel_defaults.items():
                if channel not in tick_channels:
                    # Channel does not have a zone this tick, resorting to default behavior.
                    renpy.exports.music.set_pan(pan_level, delay=0.1, channel=channel)
        ParallelProcess.per_tick(self, gt)


class SoundVolumeAreas(ParallelProcess):
    process_id = "sound_volume_areas"

    def __init__(self):
        """
        This class represents the parallel process that changes the volume for specified channels when areas are
        entered.
        """
        ParallelProcess.__init__(self)

        # Indexed elements that can be removed
        self.id_data = {}

        # Non-indexed elements that cannot be removed.
        self.other_data = []

        # Background music defaults to map background music, default channel defaults to 'music'
        self.channel_defaults = {}

    @classmethod
    def add_area(
            cls, volume_level, start_x, end_x, start_y, end_y,
            trans_start_x=None, trans_end_x=None, trans_start_y=None, trans_end_y=None,
            trans_radius=None,
            channel="music", game_map=None, area_id=None
    ):
        """
        Adds a new area to this Parallel process.
        :param float volume_level: The volume level to maintain in this area.
        :param int start_x: Starting x coord of the area.
        :param int end_x: final x coord of the area
        :param int start_y: starting y coord of the area
        :param int end_y: final y coord of the area
        :param int trans_start_x: Starting x coord of the transition area. Overrides trans_radius if given.
        :param int trans_end_x: final x coord of the transition area. Overrides trans_radius if given.
        :param int trans_start_y: starting y coord of the transition area. Overrides trans_radius if given.
        :param int trans_end_y: final y coord of the transition area. Overrides trans_radius if given.
        :param int trans_radius: Places the transition area around the main area with the given extra radius. Using
        any of the other transition-related variables will override the radius for that side only.
        :param str channel: The sound channel which this area affects.
        :param OrthogonalTiledMap game_map: The map for which to perform this operation. Defaults to the map being
        loaded, or the map that is on screen if no map is being loaded. Will almost never have to be specified.
        :param str area_id: the id under which to index the area, by which it can be targeted for removal. If no
        area_id is given, this area cannot be removed by later code.
        """
        full_area, trans_area = cls._get_areas(
            start_x, end_x, start_y, end_y, trans_start_x, trans_end_x, trans_start_y, trans_end_y, trans_radius)
        area_tuple = (volume_level, full_area, trans_area, channel)

        if area_id is not None:
            cls.get_current_instance(game_map).id_data[area_id] = area_tuple
        else:
            cls.get_current_instance(game_map).other_data.append(area_tuple)

    @classmethod
    def drop_area(cls, area_id, game_map=None):
        """
        Drops the area with the given ID from this parallel process.
        :param str area_id: the given ID.
        :param OrthogonalTiledMap game_map: The map for which to perform this operation. Defaults to the map being
        loaded, or the map that is on screen if no map is being loaded. Will almost never have to be specified.
        """
        cls.get_current_instance(game_map).id_data.pop(area_id)

    @classmethod
    def set_default(cls, volume_level, channel="music", game_map=None):
        """
        Sets the default volume for the given channel.
        :param float volume_level: The volume level to maintain by default.
        :param str channel: The given channel.
        :param OrthogonalTiledMap game_map: The map for which to perform this operation. Defaults to the map being
        loaded, or the map that is on screen if no map is being loaded. Will almost never have to be specified.
        """
        cls.get_current_instance(game_map).channel_defaults[channel] = volume_level

    @classmethod
    def drop_default(cls, channel="music", game_map=None):
        """
        Drops the default sound volume for the given channel.
        :param str channel: The given channel.
        :param OrthogonalTiledMap game_map: The map for which to perform this operation. Defaults to the map being
        loaded, or the map that is on screen if no map is being loaded. Will almost never have to be specified.
        """
        cls.get_current_instance(game_map).channel_defaults.pop(channel)

    def _handle_area(self, pc_coords, full_area, trans_area, volume_level, channel):
        """
        Handles the per-tick operations for a single area.
        :param Coord pc_coords: The current central coord of the player character.
        :param Area full_area: the full area for this pan level.
        :param Area trans_area: the transition area for this pan level.
        :param float volume_level: The volume level for this area.
        :param str channel: The channel to which this area applies.
        """
        if in_area(pc_coords, full_area):
            # In full area, meaning full pan setting is in effect
            renpy.exports.music.set_volume(volume_level, delay=0.1, channel=channel)
            return channel
        elif in_area(pc_coords, trans_area):
            # In transition area, meaning total panning depends on relative position
            trans_ratio = get_trans_ratio(pc_coords, full_area, trans_area)
            channel_default = 0.5 if channel not in self.channel_defaults else self.channel_defaults[channel]

            final_volume = channel_default + (volume_level - channel_default) * trans_ratio
            renpy.exports.music.set_volume(final_volume, delay=0.1, channel=channel)
            return channel

    def per_tick(self, gt):
        """
        Per-tick operations for this parallel process. Will check every area to see whether the player is currently
        inside them or their transition areas, setting the volume appropriately if so. Then, if the player is not inside
        any areas for a channel that has a default set, this function will execute that default.
        :param float gt: the game time in seconds.
        """
        if not self.paused:
            pink_otm_current_pc = renpy.store.pink_otm_current_pc  # type: OrthogonalTiledMapGameObjectSpriteCollection
            pc_coords = pink_otm_current_pc.central_coord

            # Channels that the player is in zones for during this tick.
            tick_channels = set()

            for volume_level, full_area, trans_area, channel in self.id_data.values():
                channel = self._handle_area(pc_coords, full_area, trans_area, volume_level, channel)
                if channel:
                    tick_channels.add(channel)
            for volume_level, full_area, trans_area, channel in self.other_data:
                channel = self._handle_area(pc_coords, full_area, trans_area, volume_level, channel)
                if channel:
                    tick_channels.add(channel)

            # Only reaches this bit if current player area corresponds to no set area.
            for channel, volume_level in self.channel_defaults.items():
                if channel not in tick_channels:
                    # Channel does not have a zone this tick, resorting to default behavior.
                    renpy.exports.music.set_volume(volume_level, delay=0.0, channel=channel)
        ParallelProcess.per_tick(self, gt)

    def on_init(self):
        for channel, volume_level in self.channel_defaults.items():
            renpy.exports.music.set_volume(volume_level, delay=0.0, channel=channel)


class ZoomAreas(ParallelProcess):
    process_id = "zoom_areas"

    def __init__(self):
        """
        This class represents the parallel process that makes the camera zoom when specified areas are entered.
        """
        ParallelProcess.__init__(self)

        # Indexed elements that can be removed
        self.id_data = {}

        # Non-indexed elements that cannot be removed.
        self.other_data = []

        # Background music defaults to map background music, default channel defaults to 'music'
        self.default_zoom = None
        self.default_zoom_time = None

    @classmethod
    def add_area(
            cls, zoom_level, zoom_time, start_x, end_x, start_y, end_y,
            trans_start_x=None, trans_end_x=None, trans_start_y=None, trans_end_y=None,
            trans_radius=None,
            game_map=None, area_id=None
    ):
        """
        Adds a new area to this Parallel process.
        :param float zoom_level: The zoom level to maintain in this area. 1.0 is the default level, with higher values
        being closer zooms, and lower values more distant zooms.
        :param float zoom_time: How long it should take to reach the zoom level, in seconds.
        :param int start_x: Starting x coord of the area.
        :param int end_x: final x coord of the area
        :param int start_y: starting y coord of the area
        :param int end_y: final y coord of the area
        :param int trans_start_x: Starting x coord of the transition area. Overrides trans_radius if given.
        :param int trans_end_x: final x coord of the transition area. Overrides trans_radius if given.
        :param int trans_start_y: starting y coord of the transition area. Overrides trans_radius if given.
        :param int trans_end_y: final y coord of the transition area. Overrides trans_radius if given.
        :param int trans_radius: Places the transition area around the main area with the given extra radius. Using
        any of the other transition-related variables will override the radius for that side only.
        :param OrthogonalTiledMap game_map: The map for which to perform this operation. Defaults to the map being
        loaded, or the map that is on screen if no map is being loaded. Will almost never have to be specified.
        :param str area_id: the id under which to index the area, by which it can be targeted for removal. If no
        area_id is given, this area cannot be removed by later code.
        """
        full_area, trans_area = cls._get_areas(
            start_x, end_x, start_y, end_y, trans_start_x, trans_end_x, trans_start_y, trans_end_y, trans_radius)
        area_tuple = (zoom_level, zoom_time, full_area, trans_area)

        if area_id is not None:
            cls.get_current_instance(game_map).id_data[area_id] = area_tuple
        else:
            cls.get_current_instance(game_map).other_data.append(area_tuple)

    @classmethod
    def drop_area(cls, area_id, game_map=None):
        """
        Drops the area with the given ID from this parallel process.
        :param str area_id: the given ID.
        :param OrthogonalTiledMap game_map: The map for which to perform this operation. Defaults to the map being
        loaded, or the map that is on screen if no map is being loaded. Will almost never have to be specified.
        """
        cls.get_current_instance(game_map).id_data.pop(area_id)

    @classmethod
    def set_default(cls, zoom_level, zoom_time, game_map=None):
        """
        Sets the default zoom level
        :param float zoom_level: The zoom level to maintain by default. 1.0 is the default level, with higher values
        being closer zooms, and lower values more distant zooms.
        :param float zoom_time: How long it should take to reach the zoom level, in seconds.
        :param OrthogonalTiledMap game_map: The map for which to perform this operation. Defaults to the map being
        loaded, or the map that is on screen if no map is being loaded. Will almost never have to be specified.
        """
        current_instance = cls.get_current_instance(game_map)
        current_instance.default_zoom = zoom_level
        current_instance.default_zoom_time = zoom_time

    def _handle_area(self, pc_coords, full_area, trans_area, zoom_level, zoom_time):
        """
        Handles the per-tick operations for a single area.
        :param Coord pc_coords: The current central coord of the player character.
        :param Area full_area: the full area for this pan level.
        :param Area trans_area: the transition area for this pan level.
        :param float zoom_level: The zoom level for this area.
        :param float zoom_time: The zoom time for this area.
        """
        if in_area(pc_coords, full_area):
            # In full area, meaning full pan setting is in effect
            renpy.store.pink_otm_current_camera.smooth_zoom(zoom_level, zoom_time)
            return True
        elif in_area(pc_coords, trans_area):
            # In transition area, meaning total panning depends on relative position
            trans_ratio = get_trans_ratio(pc_coords, full_area, trans_area)

            final_zoom = self.default_zoom + (zoom_level - self.default_zoom) * trans_ratio
            renpy.store.pink_otm_current_camera.smooth_zoom(final_zoom, zoom_time)
            return True
        return False

    def per_tick(self, gt):
        """
        Per-tick operations for this parallel process. Will check every area to see whether the player is currently
        inside them or their transition areas, starting the zoom process appropriately if so. If the player is not
        inside any areas, will start the zoom process for the default zoom.
        :param float gt: the game time in seconds.
        """
        if not self.paused:
            pink_otm_current_pc = renpy.store.pink_otm_current_pc  # type: OrthogonalTiledMapGameObjectSpriteCollection
            pc_coords = pink_otm_current_pc.central_coord

            for zoom_level, zoom_time, full_area, trans_area in self.id_data.values():
                if self._handle_area(pc_coords, full_area, trans_area, zoom_level, zoom_time):
                    return
            for zoom_level, zoom_time, full_area, trans_area in self.other_data:
                if self._handle_area(pc_coords, full_area, trans_area, zoom_level, zoom_time):
                    return
            if self.default_zoom is not None and self.default_zoom_time is not None:
                renpy.store.pink_otm_current_camera.smooth_zoom(self.default_zoom, self.default_zoom_time)
        ParallelProcess.per_tick(self, gt)


class VarAreas(ParallelProcess):
    process_id = "var_areas"

    def __init__(self):
        """
        This class represents the parallel process that changes variables when areas are entered.
        """
        ParallelProcess.__init__(self)

        # Indexed elements that can be removed
        self.id_data = {}

        # Non-indexed elements that cannot be removed.
        self.other_data = []

    @classmethod
    def add_area(cls, var_name, var_value, start_x, end_x, start_y, end_y, game_map=None, area_id=None):
        """
        Adds a new area to this parallel process.
        :param str var_name: The name of the variable to alter.
        :param var_value: The value to which to set the variable.
        :param int start_x: The starting X coord of this area.
        :param int end_x: The final X coord of this area.
        :param int start_y: The starting Y coord of this area.
        :param int end_y: The final Y coord of this area.
        :param OrthogonalTiledMap game_map: The map for which to perform this operation. Defaults to the map being
        loaded, or the map that is on screen if no map is being loaded. Will almost never have to be specified.
        :param str area_id: the id under which to index the area, by which it can be targeted for removal. If no
        area_id is given, this area cannot be removed by later code.
        """
        area_tuple = (Area(start_x, end_x, start_y, end_y), var_name, var_value)

        if area_id is not None:
            cls.get_current_instance(game_map).id_data[area_id] = area_tuple
        else:
            cls.get_current_instance(game_map).other_data.append(area_tuple)

    @classmethod
    def drop_area(cls, area_id, game_map=None):
        """
        Drops the area with the given ID from this parallel process.
        :param str area_id: the given ID.
        :param OrthogonalTiledMap game_map: The map for which to perform this operation. Defaults to the map being
        loaded, or the map that is on screen if no map is being loaded. Will almost never have to be specified.
        """
        cls.get_current_instance(game_map).id_data.pop(area_id)

    @staticmethod
    def _handle_area(pc_coords, area, var_name, var_value):
        """
        Handles the per-tick operations for a single area.
        :param Coord pc_coords: The current central coord of the player character.
        :param Area area: the area for this variable setter.
        :param str var_name: The name of the variable to alter.
        :param var_value: The value to which to set the variable.
        """
        if in_area(pc_coords, area):
            setattr(renpy.store, var_name, var_value)

    def per_tick(self, gt):
        """
        Per-tick operations for this parallel process. Will check every area to see whether the player is currently
        inside them, updating variables appropriately if so.
        :param float gt: the game time in seconds.
        """

        if not self.paused:
            pink_otm_current_pc = renpy.store.pink_otm_current_pc  # type: OrthogonalTiledMapGameObjectSpriteCollection
            pc_coords = pink_otm_current_pc.central_coord

            for area, var_name, var_value in self.id_data.values():
                self._handle_area(pc_coords, area, var_name, var_value)
            for area, var_name, var_value in self.other_data:
                self._handle_area(pc_coords, area, var_name, var_value)
        ParallelProcess.per_tick(self, gt)


class CameraSwitchAreas(ParallelProcess):
    process_id = "camera_switch_areas"

    def __init__(self):
        """
        This class represents the parallel process that changes the camera focus when areas are entered.
        """
        ParallelProcess.__init__(self)

        # Indexed elements that can be removed
        self.id_data = {}

        # Non-indexed elements that cannot be removed.
        self.other_data = []

        # defaults
        self.default_camera_target = None
        self.default_zoom_level = None

    @classmethod
    def add_area(cls, camera_target, start_x, end_x, start_y, end_y, zoom_level=1.0, game_map=None, area_id=None):
        """
        Adds a new area to this parallel process.
        :param str camera_target: The refname of the camera's target
        :param int start_x: The starting X coord of this area.
        :param int end_x: The final X coord of this area.
        :param int start_y: The starting Y coord of this area.
        :param int end_y: The final Y coord of this area.
        :param float zoom_level: The zoom level to maintain for this camera by default. Transition times are
         near-instantaneous and cannot be customized.
        :param OrthogonalTiledMap game_map: The map for which to perform this operation. Defaults to the map being
        loaded, or the map that is on screen if no map is being loaded. Will almost never have to be specified.
        :param str area_id: the id under which to index the area, by which it can be targeted for removal. If no
        area_id is given, this area cannot be removed by later code.
        """
        area_tuple = (Area(start_x, end_x, start_y, end_y), camera_target, zoom_level)

        if area_id is not None:
            cls.get_current_instance(game_map).id_data[area_id] = area_tuple
        else:
            cls.get_current_instance(game_map).other_data.append(area_tuple)

    @classmethod
    def drop_area(cls, area_id, game_map=None):
        """
        Drops the area with the given ID from this parallel process.
        :param str area_id: the given ID.
        :param OrthogonalTiledMap game_map: The map for which to perform this operation. Defaults to the map being
        loaded, or the map that is on screen if no map is being loaded. Will almost never have to be specified.
        """
        cls.get_current_instance(game_map).id_data.pop(area_id)

    @classmethod
    def set_default(cls, camera_target, zoom_level=1.0, game_map=None):
        """
        Sets the default camera_target and zoom level
        :param str camera_target: The refname of the camera's target
        :param float zoom_level: The zoom level to maintain for this camera by default.
        :param OrthogonalTiledMap game_map: The map for which to perform this operation. Defaults to the map being
        loaded, or the map that is on screen if no map is being loaded. Will almost never have to be specified.
        """
        current_instance = cls.get_current_instance(game_map)
        current_instance.default_camera_target = camera_target
        current_instance.default_zoom_level = zoom_level

    @staticmethod
    def _handle_area(pc_coords, area, camera, camera_target, zoom_level, zoom_time):
        """
        Handles the per-tick operations for a single area.
        :param Coord pc_coords: The current central coord of the player character.
        :param Area area: the area for this variable setter.
        :param OrthogonalTiledCamera camera: the current camera object
        :param str camera_target: The refname of the camera's target for this area.
        :param float zoom_level: The zoom level to maintain for the area.
        :param float zoom_time: The time in seconds to transition to the zoom level.
        """
        if in_area(pc_coords, area):
            camera.switch_target(getattr(renpy.store, camera_target))
            camera.smooth_zoom(zoom_level, zoom_time)
            return True

    def per_tick(self, gt):
        """
        Per-tick operations for this parallel process. Will check every area to see whether the player is currently
        inside them, setting the camera and zoom level to the first listed area the player is inside. If the player is
        not inside any areas, will set the camera to the default if one is set, and to the player if not.
        :param float gt: the game time in seconds.
        """
        if not self.paused:
            pink_otm_current_pc = renpy.store.pink_otm_current_pc  # type: OrthogonalTiledMapGameObjectSpriteCollection
            pc_coords = pink_otm_current_pc.central_coord
            zoom_time = pink_otm_current_pc.movement_speed - 0.04
            camera = renpy.store.pink_otm_current_camera  # type: OrthogonalTiledCamera

            for area, camera_target, zoom_level in self.id_data.values():
                if self._handle_area(pc_coords, area, camera, camera_target, zoom_level, zoom_time):
                    return
            for area, camera_target, zoom_level in self.other_data:
                if self._handle_area(pc_coords, area, camera, camera_target, zoom_level, zoom_time):
                    return

            if self.default_camera_target is not None:
                camera.switch_target(getattr(renpy.store, self.default_camera_target))
                camera.smooth_zoom(self.default_zoom_level, zoom_time)
            else:
                # if no default is set, recenters on player
                camera.recenter_on_player()
        ParallelProcess.per_tick(self, gt)


class ControlAreaCommandSet:
    def __init__(self, ref_name, commands, replace=True, interrupt=False):
        """
        This class represents a set of instructions for a single object in the ControlAreas parallel process.
        :param str ref_name: The ref_name of the object to which to assign the commands.
        :param list commands: The list of ControlCommands to assign to the object with the given ref_name.
        :param bool replace: Whether the specified control commands should replace the object's current list of
        control commands, or should instead be appended.
        :param bool interrupt: Whether the object should interrupt any ongoing delays or animations when assigned
        new commands.
        """
        self.ref_name = ref_name
        self.commands = commands
        self.replace = replace
        self.interrupt = interrupt


class ControlAreas(ParallelProcess):
    process_id = "control_areas"

    def __init__(self):
        """
        This class represents the parallel process that assigns control commands to mobile objects when areas are
        entered. This can be used to animate automated doors, move NPCs, etc.
        """
        ParallelProcess.__init__(self)

        # Indexed elements that can be removed
        self.id_data = {}

        # Set of all area_ids that the player is in as of the previous tick.
        self._in_areas = set()

        # The ID to use in the next auto-generated area_id.
        self._next_id_nr = 0

    @classmethod
    def add_area(
            cls, start_x, end_x, start_y, end_y, enter_commands=None, leave_commands=None, game_map=None, area_id=None
    ):
        """
        Adds a new area to this parallel process.
        :param int start_x: The starting X coord of this area.
        :param int end_x: The final X coord of this area.
        :param int start_y: The starting Y coord of this area.
        :param int end_y: The final Y coord of this area.
        :param list enter_commands: A list of ControlAreaCommandSet instances that should be executed when entering
        the area.
        :param list leave_commands: A list of ControlAreaCommandSet instances that should be executed when leaving
        the area.
        :param OrthogonalTiledMap game_map: The map for which to perform this operation. Defaults to the map being
        loaded, or the map that is on screen if no map is being loaded. Will almost never have to be specified.
        :param str area_id: the id under which to index the area, by which it can be targeted for removal. If no
        area_id is given, one is automatically generated.
        """
        if enter_commands is None:
            enter_commands = []
        if leave_commands is None:
            leave_commands = []
        area_tuple = (Area(start_x, end_x, start_y, end_y), enter_commands, leave_commands)

        if area_id is None:
            # Since unique area IDs are needed for the in_areas comparison, this parallel process automatically
            # generates IDs if none are passed along.
            area_id = cls.get_next_auto_id(game_map)

        cls.get_current_instance(game_map).id_data[area_id] = area_tuple

    @classmethod
    def get_next_auto_id(cls, game_map=None):
        """
        Generates the next auto-generated area ID.
        :param OrthogonalTiledMap game_map: The map for which to perform this operation. Defaults to the map being
        loaded, or the map that is on screen if no map is being loaded. Will almost never have to be specified.
        """
        current_instance = cls.get_current_instance(game_map)  # type: ControlAreas
        next_auto_id = "auto_id_" + str(current_instance._next_id_nr)
        current_instance._next_id_nr += 1
        return next_auto_id

    @classmethod
    def drop_area(cls, area_id, game_map=None):
        """
        Drops the area with the given ID from this parallel process.
        :param str area_id: the given ID.
        :param OrthogonalTiledMap game_map: The map for which to perform this operation. Defaults to the map being
        loaded, or the map that is on screen if no map is being loaded. Will almost never have to be specified.
        """
        cls.get_current_instance(game_map).id_data.pop(area_id)

    @staticmethod
    def _handle_command_set(command_set):
        """
        Handles a single ControlAreaCommandSet.
        :param ControlAreaCommandSet command_set: the given ControlAreaCommandSet.
        """
        target = getattr(renpy.store, command_set.ref_name)

        if command_set.interrupt:
            target.interrupt_control()

        if command_set.replace:
            target.control_stack = command_set.commands[:]  # py2
        else:
            target.control_stack += command_set.commands

    def _handle_area(self, pc_coords, area, area_id, enter_commands, leave_commands):
        """
        Handles the per-tick operations for a single area.
        :param Coord pc_coords: The current central coord of the player character.
        :param Area area: the area for this variable setter.
        :param str area_id: The ID for this area.
        :param list enter_commands: A list of ControlAreaCommandSet instances that should be executed when entering
        the area.
        :param list leave_commands: A list of ControlAreaCommandSet instances that should be executed when leaving
        the area.
        """
        is_in_area = in_area(pc_coords, area)
        was_in_area = area_id in self._in_areas

        if is_in_area and not was_in_area:
            for command_set in enter_commands:
                self._handle_command_set(command_set)
            self._in_areas.add(area_id)
        elif not is_in_area and was_in_area:
            for command_set in leave_commands:
                self._handle_command_set(command_set)
            self._in_areas.remove(area_id)

    def per_tick(self, gt):
        """
        Per-tick operations for this parallel process. Will check every area to see whether the player has left or
        entered these areas on this frame, assigning any commands for entering or leaving these areas if so.
        :param float gt: the game time in seconds.
        """
        if not self.paused:
            pink_otm_current_pc = renpy.store.pink_otm_current_pc  # type: OrthogonalTiledMapGameObjectSpriteCollection
            pc_coords = pink_otm_current_pc.central_coord

            for area_id, area_tuple in self.id_data.items():
                area, enter_commands, leave_commands = area_tuple
                self._handle_area(pc_coords, area, area_id, enter_commands, leave_commands)
        ParallelProcess.per_tick(self, gt)


class VarTimesAction(object):
    def __init__(self, time_increment, action, var_name, var_value):
        """
        This class represents a single timed variable change in the VarTimes parallel process.
        :param float time_increment: The amount of seconds that should pass since the previous action before executing
        this action.
        :param str action: Whether to 'set', 'add' or 'sub' the value.
        :param str var_name: The name of the variable to alter.
        :param var_value: The value which the action should apply to the var_name.
        """
        self.time_increment = time_increment
        self.action = action
        self.var_name = var_name
        self.var_value = var_value


class VarTimes(ParallelProcess):
    process_id = "var_times"

    def __init__(self):
        """
        This class represents the parallel process that changes a variable's value as time passes.
        """
        ParallelProcess.__init__(self)

        # Indexed elements that can be removed
        self.id_data = {}

        # Dictionary with keys of timer_ids, and values of the last st said timers were triggered.
        self._last_trigger_st = {}

        # The ID to use in the next auto-generated area_id.
        self._next_id_nr = 0

    def unpause(self):
        self.paused = False
        self.increment_gt(self.last_gt)

    def st_reset(self, st):
        """
        On an ST reset (such as a load, a menu close or an event start or end), subtracts the last gt from the
        next trigger gt so that the timing remains correct
        :param float st: Last show time in seconds.
        """
        for key in self._last_trigger_st:
            self._last_trigger_st[key] -= self.last_gt + st
        self.last_gt = st

    def increment_gt(self, gt_diff):
        """
        Delays all timers by the given number of seconds
        :param float gt_diff: the quantity of time by which to delay the variable changes
        """
        for key, last_trigger_st in self._last_trigger_st.items():
            self._last_trigger_st[key] += gt_diff

    @classmethod
    def get_next_auto_id(cls, game_map=None):
        """
        Generates the next auto-generated area ID.
        :param OrthogonalTiledMap game_map: The map for which to perform this operation. Defaults to the map being
        loaded, or the map that is on screen if no map is being loaded. Will almost never have to be specified.
        """
        current_instance = cls.get_current_instance(game_map)  # type: VarTimes
        next_auto_id = "auto_id_" + str(current_instance._next_id_nr)
        current_instance._next_id_nr += 1
        return next_auto_id

    @classmethod
    def add_timer(cls, action_list, timer_id=None, game_map=None):
        """
        Adds a timer to this parallel process.
        :param list action_list: The list of VarTimesAction instances for this timer.
        :param str timer_id: the id under which to index the timer, by which it can be targeted for removal. If no
        timer_id is given, one is automatically generated.
        :param OrthogonalTiledMap game_map: The map for which to perform this operation. Defaults to the map being
        loaded, or the map that is on screen if no map is being loaded. Will almost never have to be specified.
        """
        if timer_id is None:
            # Since unique area IDs are needed for the _last_trigger_st comparison, this parallel process automatically
            # generates IDs if none are passed along.
            timer_id = cls.get_next_auto_id(game_map)

        current_instance = cls.get_current_instance(game_map)  # type: VarTimes
        current_instance.id_data[timer_id] = action_list
        current_instance._last_trigger_st[timer_id] = current_instance.last_gt

    def _handle_timer(self, gt, action_list, timer_id):
        """
        Handles the per-tick operations for a single timer.
        :param float gt: The game time in seconds.
        :param list action_list: The list of VarTimesAction instances for this timer.
        :param str timer_id: The id for this timer.
        """
        while gt > self._last_trigger_st[timer_id] + action_list[0].time_increment:
            next_action = action_list.pop(0)
            if next_action.action == "set":
                setattr(renpy.store, next_action.var_name, next_action.var_value)
            elif next_action.action == "add":
                new_value = getattr(renpy.store, next_action.var_name) + next_action.var_value
                setattr(
                    renpy.store,
                    next_action.var_name,
                    new_value)
            elif next_action.action == "sub":
                new_value = getattr(renpy.store, next_action.var_name) - next_action.var_value
                setattr(
                    renpy.store,
                    next_action.var_name,
                    new_value)
            self._last_trigger_st[timer_id] += next_action.time_increment
            action_list.append(next_action)

    def per_tick(self, gt):
        """
        Per-tick operations for this parallel process. Will check every timer to see whether their next action should
        be executed, and executes them if so. Executed actions are appended to the back of the action list.
        :param float gt: the game time in seconds.
        """
        if gt < self.last_gt:
            self.st_reset(gt)

        if not self.paused:
            for timer_id, action_list in self.id_data.items():
                self._handle_timer(gt, action_list, timer_id)
        ParallelProcess.per_tick(self, gt)


def in_area(coords, area):
    """
    Returns whether the given coordinates are within the given area
    :param coords coords: the given coordinates
    :param Area area: the given area
    :rtype: bool
    """
    return area.start_x <= coords.x <= area.end_x and area.start_y <= coords.y <= area.end_y


def get_trans_ratio(char_coords, full_area, trans_area):
    """
    This function is used to calculate how far into a transition area a character is.
    :param Coord char_coords: coords of a character
    :param Area full_area: The area in question.
    :param Area trans_area: The transition area.
    :rtype: float
    """
    # The random float translations are due to python 2 turning int divisions into ints.
    if trans_area.start_x <= char_coords.x <= full_area.start_x and (full_area.start_x - trans_area.start_x) != 0:
        x_ratio = (char_coords.x - trans_area.start_x) / (float(full_area.start_x) - trans_area.start_x)
    elif (trans_area.end_x - full_area.end_x) != 0:
        # To the right
        x_ratio = (trans_area.end_x - char_coords.x) / (float(trans_area.end_x) - full_area.end_x)
    else:
        # Within the horizontal range
        x_ratio = 1.0

    if trans_area.start_y <= char_coords.y <= full_area.start_y and (full_area.start_y - trans_area.start_y) != 0:
        #
        y_ratio = (char_coords.y - trans_area.start_y) / (float(full_area.start_y) - trans_area.start_y)
    elif (trans_area.end_y - full_area.end_y) != 0:
        y_ratio = (trans_area.end_y - char_coords.y) / (float(trans_area.end_y) - full_area.end_y)
    else:
        y_ratio = 1.0

    min_ratio = min(x_ratio, y_ratio)
    return min_ratio


def restore_rollback_settings():
    """
    Restores the rollback settings from before the pink engine was initialized.
    """
    if renpy.store.pink_otm_rollback_restore is not None:
        renpy.store.config.rollback_enabled = renpy.store.pink_otm_rollback_restore


def go_to_map(
        target_map, x_coord=0, y_coord=0, orientation=None, transition_in=None,
        transition_in_sound=None
):
    """
    Initializes the given OTM map and moves the game to said map
    :param str target_map: The path of the given OTM map
    :param int x_coord: The x coord at which to place the player character
    :param int y_coord: The y coord at which to place the player character
    :param str orientation: The orientation at which to place the player character
    :param transition_in: Which transition to use during intro to new map.
    :param transition_in_sound: Which sound effect to play as new map is opened
    """
    renpy.store.pink_otm_current_event_name = None
    if renpy.store.pink_otm_current_event_type is not None:
        end_event(renpy.store.pink_otm_current_event_type, no_jump=True)
    elif renpy.store.pink_otm_current_map:  # To prevent popping when go_to_map from outside event
        # Pops
        renpy.exports.pop_call()

        # Unfreezes old map in case the go_to_map was called from a menu screen, thus unfreezing any sprite collections
        # that might carry over
        renpy.store.pink_otm_current_map.unfreeze_map()

    # Rollback is restored, if enabled, but can't rollback to before start of event.
    restore_rollback_settings()
    renpy.exports.block_rollback()

    target_x_zoom = renpy.store.pink_otm_camera_current_xzoom
    target_y_zoom = renpy.store.pink_otm_camera_current_yzoom

    # Kills all ongoing map sounds
    renpy.store.pink_sound_manager.stop_all_sounds()

    if renpy.store.pink_otm_current_map is not None:
        renpy.store.pink_otm_current_map.stop_predicting()
        if orientation is None and renpy.store.pink_otm_current_map.player_object is not None:
            orientation = renpy.store.pink_otm_current_map.player_object.orientation
        target_x_zoom = renpy.store.pink_otm_current_map.camera.xzoom
        target_y_zoom = renpy.store.pink_otm_current_map.camera.yzoom

        # Runs the code_on_leave code for the old map
        renpy.store.pink_otm_current_map.run_code_on_leave()

    map_file = renpy.exports.file("pink_engine/orthogonal_tiled_maps/" + target_map)
    map_dict = json.load(map_file)
    new_map = OrthogonalTiledMap(map_dict, "pink_engine/orthogonal_tiled_maps/" + target_map)
    renpy.store.pink_otm_current_map = new_map

    new_map.add_object_at_coord(
        renpy.store.pink_otm_pc_init_dict, x_coord, y_coord, is_player=True, orientation=orientation)
    renpy.store.pink_otm_current_pc = new_map.player_object

    if new_map.forced_to_run():
        new_map.start_running()
    if not new_map.allowed_to_run():
        new_map.stop_running()

    # FOLLOWERS
    old_follower_objects = renpy.store.pink_otm_followers[:]  # py2
    renpy.store.pink_otm_followers = []
    for old_follower_object in old_follower_objects:
        new_follower = add_player_follower(old_follower_object.sprite_collection_path)
        new_follower.properties = old_follower_object.properties
    for follower in renpy.store.pink_otm_followers:
        follower.movement_speed = new_map.player_object.movement_speed
        follower.move_animation = new_map.player_object.move_animation
    renpy.store.pink_otm_current_pc.follower_next_command = None

    # MUSIC
    if new_map.background_music == "stop":
        renpy.exports.music.stop()
    elif new_map.background_music != "continue":
        renpy.exports.music.play(new_map.background_music, loop=True, if_changed=True)

    # AMBIENCE
    if new_map.background_ambience == "stop":
        renpy.exports.music.stop(channel='sound')
    elif new_map.background_ambience != "continue":
        renpy.exports.music.play(new_map.background_ambience, channel='sound', loop=True, if_changed=True)

    new_map.force_check_touch = True

    # sets transition and transition sound effect
    renpy.store.pink_map_transition_in = transition_in
    renpy.store.pink_map_transition_in_sound = transition_in_sound

    # Empty player's control stack of remaining commands
    new_map.player_object.control_stack = []

    # Check which keys are held, start taking the action for the relevant ones
    new_map.check_held_keys()

    # Runs the code_on_enter code for the new map.
    renpy.store.pink_otm_current_map.run_code_on_enter()

    # Resets music volume channel output level (since it might have been altered by the previous map's parallel
    #  processes)
    renpy.exports.music.set_volume(1.0, delay=0.1)

    # Calls parallel process on_init functions on the map (they have default values set by code_on enter, and may alter
    # the music volume channel, hence this needs to happen at this point.
    for parallel_process in renpy.store.pink_otm_current_map.parallel_processes.values():
        parallel_process.on_init()

    # Set at this point due to dependency on smart zoom process having been initialized.
    new_map.camera.set_x_zoom(target_x_zoom)
    new_map.camera.set_y_zoom(target_y_zoom)

    renpy.exports.jump('pink_otm_call_map')


def force_instant_transition_on_event_end():
    """
    Temporarily overrides config.window_hide_transition so as to make the pink engine not have any window hide
    transition during the current event. Necessary if you have an event that has dialogue and ends on a go_to_map
    statement, and you want that go_to_map to be performed instantly.
    """
    renpy.store.pink_otm_window_hide_cache = renpy.store.config.window_hide_transition
    renpy.store.config.window_hide_transition = None


def start_event(event_type, interaction_reaction=True):
    """
    Starts a pink engine event with the given type
    :param str event_type: The given event type (static, dynamic or continuous)
    :param bool interaction_reaction: Whether to play the default interaction reaction
    """
    # The pink engine does not expect a return statement when it calls a label, it merely uses calls to pass along
    # variables
    renpy.exports.pop_call()

    renpy.store.pink_otm_current_event_type = event_type
    renpy.store.pink_otm_current_map.disable_controls()
    renpy.store.pink_otm_event_interaction_reaction = False
    renpy.store.pink_otm_current_map.interrupt_mouse_click_move()

    # Rollback is restored, if enabled, but can't rollback to before start of event.
    restore_rollback_settings()
    renpy.exports.block_rollback()

    # Parallel process pausing
    if event_type == "static":
        renpy.store.pink_sound_manager.pause_all_sounds()
        renpy.store.pink_otm_current_map.pause_all_parallel_processes()
        if renpy.store.pink_otm_pause_timer_on_static_event:
            renpy.store.otm_timer.pause(event_pause=True)
    elif event_type == "dynamic":
        if renpy.store.pink_otm_pause_timer_on_dynamic_event:
            renpy.store.otm_timer.pause(event_pause=True)
    else:
        renpy.store.pink_otm_current_map.pause_parallel_processes(*renpy.store.pink_otm_parallel_pause)
        if renpy.store.pink_otm_pause_timer_on_continuing_event:
            renpy.store.otm_timer.pause(event_pause=True)

    # Makes player stand still, as well as stopping their running
    renpy.store.pink_otm_current_map.halt_player()

    # Uncouples followers
    renpy.store.pink_otm_current_pc.follower = None

    # Event type-dependent map stopping.
    if event_type == "static":
        renpy.store.pink_otm_current_map.freeze_map()
    elif event_type == "dynamic":
        renpy.store.pink_otm_current_map.halt_map()
    elif event_type == "continuing":
        pass

    # Stops mouse-based movement, since mouse releases during events won't register.
    renpy.store.pink_otm_current_map._mouse_state = None

    # Default interaction
    if interaction_reaction:
        if event_type == "dynamic" and hasattr(renpy.store.pink_otm_event_trigger, 'default_interaction'):
            renpy.store.pink_otm_event_interaction_reaction = True
            renpy.store.pink_otm_event_trigger.default_interaction()
        elif event_type == "continuing" and hasattr(renpy.store.pink_otm_event_trigger, 'save_and_default_interaction'):
            renpy.store.pink_otm_event_interaction_reaction = True
            renpy.store.pink_otm_event_trigger.save_and_default_interaction()

    # Show screen pink_otm_map
    renpy.exports.show_screen('pink_otm_map')


def end_event(event_type: str, no_jump: bool = False, reset_interactor: bool = True) -> None:
    """
    Ends a pink engine event with the given type
    :param event_type: The given event type (static, dynamic or continuous)
    :param no_jump: Whether to jump to the otm_call_map label at the end of this event. Should be False if the
    event ended with going to a different map.
    :param reset_interactor: Whether or not to reset the object you started the object interacting with.
    """
    # In case any objects got removed right before the end of the event
    renpy.store.pink_otm_current_map.check_conditional_objects()

    if event_type == "static":
        renpy.store.pink_sound_manager.unpause_all_sounds()
        renpy.store.pink_otm_current_map.unfreeze_map()
    elif event_type == "dynamic":
        renpy.store.pink_otm_current_map.unhalt_map()
    elif event_type == "continuing" and renpy.store.pink_otm_event_interaction_reaction is True and reset_interactor:
        renpy.store.pink_otm_event_trigger.load_and_continue()

    renpy.store.otm_timer.unpause(event_pause=True)

    renpy.store.pink_otm_event_trigger_object = None
    renpy.store.pink_otm_current_event_type = None
    renpy.store.pink_otm_current_event_name = None
    renpy.store.pink_otm_event_button = None
    renpy.store.pink_otm_event_interaction_reaction = None

    # Recouples followers
    if len(renpy.store.pink_otm_followers) > 0:
        renpy.store.pink_otm_current_pc.follower = renpy.store.pink_otm_followers[0]
        recouple_followers()

    renpy.store.pink_otm_current_map.enable_controls()
    renpy.store.pink_otm_current_map.check_held_keys()

    if renpy.store.pink_otm_current_map.forced_to_run():
        renpy.store.pink_otm_current_map.start_running()
    if not renpy.store.pink_otm_current_map.allowed_to_run():
        renpy.store.pink_otm_current_map.stop_running()

    # Parallel process unpausing
    renpy.store.pink_otm_current_map.unpause_all_parallel_processes()

    # No transition if the screen is shaking. It causes a mild visual glitch
    if renpy.store.pink_otm_current_map._overlay_manager.is_shaking:
        force_instant_transition_on_event_end()

    if not no_jump:
        renpy.exports.jump('pink_otm_call_map')


def start_static_event(interaction_reaction=True):
    """
    Starts a static event
    :param bool interaction_reaction: Whether to play the default interaction reaction
    """
    start_event('static', interaction_reaction)


def start_dynamic_event(interaction_reaction=True):
    """
    Starts a static event
    :param bool interaction_reaction: Whether to play the default interaction reaction
    """
    start_event('dynamic', interaction_reaction)


def start_continuing_event(interaction_reaction=True):
    """
    Starts a static event
    :param bool interaction_reaction: Whether to play the default interaction reaction
    """
    start_event('continuing', interaction_reaction)


def end_current_event(reset_interactor=True):
    """
    Ends the current event
    """
    end_event(renpy.store.pink_otm_current_event_type, reset_interactor=reset_interactor)


def end_static_event():  # here for the sake of compatibility.
    """
    Ends the current event
    """
    end_current_event()


def end_dynamic_event():  # here for the sake of compatibility.
    """
    Ends the current event
    """
    end_current_event()


def end_continuing_event(reset_interactor=True):  # there for the sake of consistency
    """
    Ends the current event
    """
    end_current_event(reset_interactor=reset_interactor)


def leave_otm():
    """
    Starts an event without an otm background.
    """
    if renpy.store.pink_otm_current_event_type is not None:
        # Ends any ongoing events
        end_event(renpy.store.pink_otm_current_event_type, no_jump=True)
    else:
        # Pops the call that the pink engine made.
        renpy.exports.pop_call()

    # Kills all ongoing map sounds
    renpy.store.pink_sound_manager.stop_all_sounds()

    # Variables for returning to map
    renpy.store.otm_return_coords = renpy.store.pink_otm_current_map.player_object.central_coord
    renpy.store.otm_return_map_path = renpy.store.pink_otm_current_map.path[33:]
    renpy.store.otm_return_orientation = renpy.store.pink_otm_current_pc.orientation

    # Runs any code_on_leave code
    renpy.store.pink_otm_current_map.run_code_on_leave()

    # Sets all parents on consistent objects to None so the maps don't have to remain in-memory
    for map_object in renpy.store.pink_otm_current_map.map_objects.values():
        map_object.parent = None

    # Exiting the map
    renpy.store.pink_otm_current_map.stop_predicting()
    renpy.store.pink_otm_map_name = os.path.split(renpy.store.pink_otm_current_map.path)[1]
    renpy.store.pink_otm_current_camera = None
    renpy.store.pink_otm_current_map = None
    restore_rollback_settings()
    renpy.exports.block_rollback()

    # Restore autosave_on_choice configuration
    renpy.store.config.autosave_on_choice = renpy.store.pink_otm_autosave_on_choice_cache
    renpy.store.pink_otm_autosave_on_choice_cache = None

    renpy.exports.hide_screen('pink_otm_map')


def return_to_otm(transition_in=None, transition_in_sound=None):
    """
    Returns to the orthogonal tiled map that was last active.
    :param transition_in: Which transition to use during intro to new map.
    :param transition_in_sound: Which sound effect to play as new map is opened
    """
    go_to_map(
        renpy.store.otm_return_map_path, x_coord=renpy.store.otm_return_coords.x,
        y_coord=renpy.store.otm_return_coords.y, orientation=renpy.store.otm_return_orientation,
        transition_in=transition_in, transition_in_sound=transition_in_sound)


def in_place(target_object_name, x_coord=None, y_coord=None, orientation=None, finished_moving=True):
    """
    Returns True if the character is in the given location.
    :param target_object_name: The renpy variable for the given target object
    :param int x_coord: the given x coordinate. None for wildcard.
    :param int y_coord: the given y coordinate. None for wildcard.
    :param str orientation: The given orientation. None for wildcard.
    :param bool finished_moving: Whether or not the character must have completed their movement.
    :return:
    """
    target_object = getattr(renpy.store, target_object_name)

    if target_object is None or not target_object.is_on_map():
        return False
    else:
        return target_object.in_place(
            x_coord=x_coord, y_coord=y_coord, orientation=orientation, finished_moving=finished_moving)


# Follower functions
def add_player_follower(
        sprite_collection_path: str,
        movement_sound_function: Optional[str] = None,
        movement_sound: Optional[str] = None,
        movement_sound_multiplier: Optional[float] = None
):
    """
    :param sprite_collection_path: The name of the sprite collection the follower should use.
    :param movement_sound_function: The name of the function (in the renpy store) the follower should used.
    Will use default if None.
    :param movement_sound: The filepath for the sound effect to play for successful movement when function is
    set to pink_movement_sound_static
    :param movement_sound_multiplier: the volume multiplier for the follower's movement sound.
    """
    follower_list = renpy.store.pink_otm_followers
    if len(follower_list) == 0:
        target = renpy.store.pink_otm_current_pc
    else:
        target = follower_list[len(follower_list) - 1]

    if movement_sound_function is None:
        movement_sound_function = renpy.store.pink_follower_default_movement_sound_function
    if movement_sound is None:
        movement_sound = renpy.store.pink_follower_default_movement_sound
    if movement_sound_multiplier is None:
        movement_sound_multiplier = renpy.store.pink_otm_default_follower_movement_sound_multiplier

    follower_dict = {
        'properties': [
            {"name": "sprite_collection_path", "type": "string", "value": sprite_collection_path},
            {"name": "can_always_move", "type": "bool", "value": True},
            {"name": "move_to", "type": "string", "value": None},
            {"name": "move_from", "type": "string", "value": None},
            {"name": "movement_sound_function", "type": "str", "value": movement_sound_function},
            {"name": "movement_sound", "type": "str", "value": movement_sound},
            {"name": "movement_sound_multiplier", "type": "str", "value": movement_sound_multiplier}
        ]}
    if renpy.store.pink_otm_current_map is not None:
        target_coord = target.central_coord
        follower_object = renpy.store.pink_otm_current_map.add_object_at_coord(
            follower_dict, target_coord.x, target_coord.y, orientation=renpy.store.pink_otm_current_pc.orientation)
        follower_object.movement_speed = renpy.store.pink_otm_current_map.player_object.movement_speed
        follower_object.move_animation = renpy.store.pink_otm_current_map.player_object.move_animation
        target.follower = follower_object
    else:
        property_dict = {}
        for object_property in follower_dict['properties']:
            property_dict[object_property['name']] = object_property['value']
        follower_object = OrthogonalTiledMapGameObjectSpriteCollection(
            x=0, y=0, layer=None, properties=property_dict, collection_path=sprite_collection_path)  # noqa None allowed, figure out typing later
    if len(renpy.store.pink_otm_followers) == 0:
        follower_object.control_stack = [
            ControlCommand("go_to_smart", target="pink_otm_current_pc", target_distance=1)]
    else:
        follower_object.control_stack = [
            ControlCommand(
                "go_to_smart", target=renpy.store.pink_otm_followers[-1],
                target_distance=1)]
    renpy.store.pink_otm_followers.append(follower_object)
    return follower_object


def remove_all_followers():
    """
    Removes all of the player's followers. Can be
    called even if no OTM map is currently visible.
    """
    renpy.store.pink_otm_current_pc.follower = None
    if renpy.store.pink_otm_current_map is not None:
        for follower_object in renpy.store.pink_otm_followers:
            renpy.store.pink_otm_current_map.remove_element(follower_object)

            if follower_object.sprite_collection_path.startswith('renpy.store'):
                renpy.store.pink_otm_current_map.variable_sprite_collections.remove(follower_object)

    renpy.store.pink_otm_followers = []

    _recalculate_follower_movement()


def remove_follower_by_index(index: int):
    """
    Removes one of the player's followers by index, where an index of 0 indicates the player's first follower. Can be
    called even if no OTM map is currently visible. Afterwards, all followers are teleported to the player.
    """
    if index > len(renpy.store.pink_otm_followers) - 1:
        return

    if renpy.store.pink_otm_current_map is not None:
        follower_object = renpy.store.pink_otm_followers[index]
        renpy.store.pink_otm_current_map.remove_element(follower_object)

        if follower_object.sprite_collection_path.startswith('renpy.store'):
            renpy.store.pink_otm_current_map.variable_sprite_collections.remove(follower_object)
    renpy.store.pink_otm_followers.pop(index)

    _recalculate_follower_movement()


def remove_follower_by_path(sprite_collection_path, remove_all=False):
    """
    Removes the first follower with the given sprite. If remove_all is set to True, removes all followers with the given
    sprite. Afterwards, all followers are teleported to the player.
    """
    removal_indices = []
    for x, follower in enumerate(renpy.store.pink_otm_followers):
        if follower.sprite_collection_path == sprite_collection_path:
            removal_indices.append(x)
            if follower.sprite_collection_path.startswith('renpy.store'):
                renpy.store.pink_otm_current_map.variable_sprite_collections.remove(follower)
            if not remove_all:
                break

    for index in sorted(removal_indices, reverse=True):
        if renpy.store.pink_otm_current_map is not None:
            renpy.store.pink_otm_current_map.remove_element(renpy.store.pink_otm_followers[index])
        renpy.store.pink_otm_followers.pop(index)

    _recalculate_follower_movement()


def _recalculate_follower_movement():
    """
    Gives the followers their movement logic, so that they follow the player in a row.
    """
    renpy.store.pink_otm_current_pc.follower = None
    for x, follower in enumerate(renpy.store.pink_otm_followers):
        if x == 0:
            target = renpy.store.pink_otm_current_pc
        else:
            target = renpy.store.pink_otm_followers[x - 1]
        target.follower = follower
        follower.control_stack = [
            ControlCommand("go_to_smart", target=target, target_distance=1)]

        x_coord, y_coord = target.central_coord
        follower.set_to_coords(x_coord, y_coord, orientation=target.orientation)


def get_follower(image_path: str) -> Optional[OrthogonalTiledMapGameObjectSpriteCollection]:
    for follower in renpy.store.pink_otm_followers:  # type: OrthogonalTiledMapGameObjectSpriteCollection
        if follower.sprite_collection_path == image_path:
            return follower
    return None


def uncouple_followers():
    """
    For use in cutscenes. Makes the player's followers stop following them, allowing them to be given individual
    movement commands.
    """
    renpy.store.pink_otm_current_pc.follower = None
    for follower in renpy.store.pink_otm_followers:
        follower.follower = None
        follower.control_stack = []


def recouple_followers():
    """
    Recouple's the players followers, Giving them movement commands to make them move back into line. Done
    automatically at the end of each event.
    """
    renpy.store.pink_otm_current_pc.follower = None
    for x, follower in enumerate(renpy.store.pink_otm_followers):
        if x == 0:
            target = renpy.store.pink_otm_current_pc
        else:
            target = renpy.store.pink_otm_followers[x - 1]
        target.follower = follower
        follower.control_stack = [
            ControlCommand("go_to_smart", target=target, target_distance=1)]


def hide_all_followers():
    """
    For use in cutscenes. Makes all of the player's current followers invisible. The followers will still keep
    following the player object while invisible.
    """
    for follower in renpy.store.pink_otm_followers:  # type: OrthogonalTiledMapGameObjectSpriteCollection
        follower.hide()


def reveal_all_followers():
    """
    Undoes hide_all_followers, making all of the player's followers visible again.
    """
    for follower in renpy.store.pink_otm_followers:  # type: OrthogonalTiledMapGameObjectSpriteCollection
        follower.reveal()


def teleport_followers_to_player():
    """
    Teleports all of the player's followers to them. Useful if routing to the player at the end of a cutscene is tricky
    or undesired.
    """
    _recalculate_follower_movement()


# Developer functions
def get_all_map_filenames():
    """
    :return: A list of all OTM map filenames
    :rtype: list
    """
    map_filenames = []

    all_renpy_filenames = renpy.exports.list_files()
    for renpy_filename in all_renpy_filenames:  # type: str
        if renpy_filename.startswith("pink_engine/orthogonal_tiled_maps/") and renpy_filename[-5:] == ".json":
            map_filenames.append(renpy_filename[34:])

    return map_filenames


def get_all_tileset_filenames():
    """
    :return: A list of all tileset filenames
    :rtype: list
    """
    tileset_filenames = []

    all_renpy_filenames = renpy.exports.list_files()
    for renpy_filename in all_renpy_filenames:  # type: str
        if renpy_filename.startswith("pink_engine/tilesets/") and renpy_filename[-5:] == ".json":
            tileset_filenames.append(renpy_filename[21:])

    return tileset_filenames


def get_all_sprite_filenames():
    """
    :return: A list of all sprite collection filenames
    :rtype: list
    """
    sprite_filenames = []

    all_renpy_filenames = renpy.exports.list_files()
    for renpy_filename in all_renpy_filenames:  # type: str
        if renpy_filename.startswith("pink_engine/sprite_collections/") and renpy_filename[-5:] == ".json":
            sprite_filenames.append(renpy_filename[31:])

    return sprite_filenames


def get_map_data(filename):
    """
    :param str filename: The given filename
    :return: A dictionary containing the properties of the otm map at the given filename
    :rtype: dict
    """
    json_file = renpy.exports.file("pink_engine/orthogonal_tiled_maps/" + filename)
    map_dict = json.load(json_file)

    grid_size = str(map_dict.get('width')) + "x" + str(map_dict.get('height'))
    tile_size = str(map_dict.get('tilewidth')) + "x" + str(map_dict.get('tileheight'))
    image_size = (str(map_dict.get('width') * map_dict.get('tilewidth')) +
                  "x" + str(map_dict.get('height') * map_dict.get('tileheight')))
    layer_count = str(len(map_dict.get('layers')))
    tiled_version = map_dict.get('tiledversion')

    properties = []
    if map_dict.get('properties') is not None:
        for map_property in map_dict.get('properties'):
            properties.append(map_property['name'])

    tilesets = []
    if map_dict.get('tilesets') is not None:
        for tileset_dict in map_dict.get('tilesets'):
            tilesets.append(os.path.basename(tileset_dict['source']))

    return grid_size, tile_size, image_size, layer_count, tiled_version, properties, tilesets


def get_tileset_data(filename):
    """
    :param str filename: The given filename
    :return: A dictionary containing the properties of the tileset at the given filename
    :rtype: dict
    """
    json_file = renpy.exports.file("pink_engine/tilesets/" + filename)
    tileset_dict = json.load(json_file)

    tile_count = str(len(tileset_dict.get('tiles')))
    tiled_version = tileset_dict.get('tiledversion')

    return tile_count, tiled_version


def get_sprite_data(filename):
    """
    :param str filename: The given filename
    :return: A dictionary containing the properties of the sprite collection at the given filename
    :rtype: dict
    """
    json_file = renpy.exports.file("pink_engine/sprite_collections/" + filename)
    sprite_dict = json.load(json_file)

    animation_names = set()
    animations = []

    for animation in sprite_dict['animations']:
        animation_names.add(animation['name'])

        frame_count = len(animation['images'])
        if frame_count > 1:
            ani_length = frame_count * animation['default_speed']
            animations.append(animation['name'] + " [" + str(frame_count) + " frames, " + str(ani_length) + " seconds]")
        else:
            animations.append(animation['name'] + " [static image]")

    if (
            "stand_down" in animation_names and "stand_up" in animation_names and
            "stand_left" in animation_names and "stand_right" in animation_names and
            "walk_down" in animation_names and "walk_up" in animation_names and
            "walk_left" in animation_names and "walk_right" in animation_names and
            "run_down" in animation_names and "run_up" in animation_names and
            "run_left" in animation_names and "run_right" in animation_names
    ):
        pc_sprite = True
    else:
        pc_sprite = False

    return animations, pc_sprite


def _get_controllers():
    """
    Returns a list of all initialized controllers.
    :rtype: list
    """
    try:
        controllers = [pygame.controller.Controller(x) for x in range(pygame.controller.get_count())]
        for controller in controllers:
            if not controller.get_init():
                controller.init()
    except:  # noqa
        controllers = []
    return controllers


# Functions for arbitrary event triggers
def is_in_line(viewer, view_range, target="pink_otm_current_pc", in_view=True):
    """
    Returns whether the target (by default, the PC) is standing in a line in front of the viewer within the given
    range.
    :param str|OrthogonalTiledMapGameObject viewer: The viewing object, or its ref_name
    :param str|Coord|OrthogonalTiledMapGameObject target: The target being observed, its coordinate, or its
    ref_name.
    :param int view_range: The maximum number of tiles to look.
    :param bool in_view: If True, will only return True if the view is unobstructed by impassible tiles.
    :rtype: bool
    """
    if type(viewer) is str:  # noqa
        viewer = getattr(renpy.store, viewer)
    viewer_tuple = _convert_to_coord(viewer)
    target_tuple = _convert_to_coord(target)

    x_diff = abs(target_tuple[0] - viewer_tuple[0])
    y_diff = abs(target_tuple[1] - viewer_tuple[1])

    if hasattr(viewer, 'orientation') and viewer.orientation == "left":
        in_line = target_tuple[1] == viewer_tuple[1] and viewer_tuple[0] >= target_tuple[0] and x_diff <= view_range
    elif hasattr(viewer, 'orientation') and viewer.orientation == "right":
        in_line = target_tuple[1] == viewer_tuple[1] and viewer_tuple[0] <= target_tuple[0] and x_diff <= view_range
    elif hasattr(viewer, 'orientation') and viewer.orientation == "up":
        in_line = target_tuple[0] == viewer_tuple[0] and viewer_tuple[1] >= target_tuple[1] and y_diff <= view_range
    elif hasattr(viewer, 'orientation') and viewer.orientation == "down":
        in_line = target_tuple[0] == viewer_tuple[0] and viewer_tuple[1] <= target_tuple[1] and y_diff <= view_range
    else:
        return False

    if in_line:
        if in_view:
            return is_in_sight(viewer_tuple, target_tuple, include_touched_coords=False)
        else:
            return True


def is_in_cone(viewer, view_range, target="pink_otm_current_pc", in_view=True, include_touched_coords=False):
    """
    Returns whether the target (by default, the PC) is standing in a cone in front of the viewer within the given
    range.
    :param str|OrthogonalTiledMapGameObject viewer: The viewing object, or its ref_name
    :param str|Coord|OrthogonalTiledMapGameObject target: The target being observed, its coordinate, or its
    ref_name.
    :param int view_range: The maximum number of tiles to look.
    :param bool in_view: If True, will only return True if the view is unobstructed by impassible tiles.
    :param bool include_touched_coords: If True, will also check coordinates touched by the line of sight (so where
    the view passes straight through an adjoining corner) for obstructing objects.
    :rtype: bool
    """
    if type(viewer) is str:  # noqa
        viewer = getattr(renpy.store, viewer)
    viewer_tuple = _convert_to_coord(viewer)
    target_tuple = _convert_to_coord(target)

    x_diff = abs(target_tuple[0] - viewer_tuple[0])
    y_diff = abs(target_tuple[1] - viewer_tuple[1])

    if viewer.orientation == "left":
        in_cone = viewer_tuple[0] >= target_tuple[0] and y_diff < x_diff <= view_range
    elif viewer.orientation == "right":
        in_cone = viewer_tuple[0] <= target_tuple[0] and y_diff < x_diff <= view_range
    elif viewer.orientation == "up":
        in_cone = viewer_tuple[1] >= target_tuple[1] and x_diff < y_diff <= view_range
    elif viewer.orientation == "down":
        in_cone = viewer_tuple[1] <= target_tuple[1] and x_diff < y_diff <= view_range
    else:
        return False

    if in_cone:
        if in_view:
            return is_in_sight(viewer_tuple, target_tuple, include_touched_coords=include_touched_coords)
        else:
            return True


def _convert_to_coord(convertible):
    """
    Used by the viewing functions, converts the target and viewer to coordinates. Takes strings (interpreted as
    ref_names, will return central coord of corresponding objects), game objects (will return the central coord), or
    tuples (will convert to coodinates). Will return None is object cannot be converted.
    :param str|OrthogonalTiledMapGameObject|tuple convertible: The object to convert.
    :rtype: None|Coord
    """
    if type(convertible) is str:  # noqa
        convertible_object = getattr(renpy.store, convertible)  # Py2
        if convertible_object is not None:
            converted = convertible_object.central_coord
        else:
            converted = None
    elif issubclass(type(convertible), OrthogonalTiledMapGameObject):
        converted = convertible.central_coord
    else:
        converted = Coord(convertible[0], convertible[1])  # noqa is int tuple
    return converted


def get_map_object(ref_id):
    """
    Returns the object on the current OTM map with the given ref id.
    :param int ref_id: The given ref id.
    """
    return renpy.store.pink_otm_current_map.map_objects[ref_id]


def coord_distance(coord_1, coord_2):
    """
    Calculates the distance between two coordinates.
    :param tuple coord_1: Coordinate 1.
    :param tuple coord_2: COordinate 2.
    """
    return abs(coord_1[0] - coord_2[0]) + abs(coord_1[1] - coord_2[1])


def get_walk_up_target(origin, goal):
    """
    Used to calculate the target for making an NPC walk up to an object. Will return the coordinates of the passible
    (move_to rules are 1111) side closest to the moving object.
    :param str|OrthogonalTiledMapGameObject origin: The object that is to perform the move, or its ref_name.
    :param str|OrthogonalTiledMapGameObject|tuple goal: The object, ref_name or coordinate tuple that is to be walked
    up to.
    """
    origin = _convert_to_coord(origin)
    goal = _convert_to_coord(goal)

    if coord_distance(origin, goal) < 2:
        return origin

    coords = [(goal.x + 1, goal.y), (goal.x - 1, goal.y), (goal.x, goal.y + 1), (goal.x, goal.y - 1)]
    coords.sort(key=lambda x: coord_distance(origin, x))
    for coord in coords:
        if renpy.store.pink_otm_current_map.base_grid.get_move_to(coord[0], coord[1]) == "1111":
            return coord


def is_in_range(viewer, view_range, target="pink_otm_current_pc", in_view=True, include_touched_coords=True):
    """
    Returns whether the target (by default, the PC) is standing within the given range of the viewer.
    :param str|OrthogonalTiledMapGameObject viewer: The viewing object, or its ref_name
    :param str|Coord|OrthogonalTiledMapGameObject target: The target being observed, its coordinate, or its
    ref_name.
    :param int view_range: The maximum number of tiles to look.
    :param bool in_view: If True, will only return True if the view is unobstructed by impassible tiles.
    :param bool include_touched_coords: If True, will also check coordinates touched by the line of sight (so where
    the view passes straight through an adjoining corner) for obstructing objects.
    :rtype: bool
    """
    viewer_tuple = _convert_to_coord(viewer)
    target_tuple = _convert_to_coord(target)
    if viewer_tuple is None or target_tuple is None:
        return False

    distance = coord_distance(viewer_tuple, target_tuple)
    if distance <= view_range:
        if in_view:
            return is_in_sight(viewer_tuple, target_tuple, include_touched_coords=include_touched_coords)
        else:
            return True
    return False


def is_in_sight(start_coord, end_coord, include_touched_coords=True):
    """
    Returns true if sight from the start_coord to the end_coord is unobstructed.
    :param Coord start_coord: The start coordinate, from which is looked.
    :param Coord end_coord: The end coordinate, at which is looked.
    :param bool include_touched_coords: If True, will also check coordinates touched by the line of sight (so where
    the view passes straight through an adjoining corner) for obstructing objects.
    :rtype: bool
    """
    coord_order = coords_in_line(
        start_coord=start_coord, end_coord=end_coord, include_touched_coords=include_touched_coords)
    for coord in coord_order:
        passable = renpy.store.pink_otm_current_map.base_grid.get_move_to(coord.x, coord.y) == "1111"
        if not passable:
            return False
    return True


def coords_in_line(start_coord, end_coord, include_touched_coords=True):
    """
    Retrieves all coordinates that exist on a line between the given start coordinate and the given end coordinate.
    :param Coord start_coord: the start of the line.
    :param Coord end_coord: the end of the line.
    :param bool include_touched_coords: If True, will also include coordinates touched by the line (so where
    it passes straight through an adjoining corner).
    """
    line_coord = [start_coord]

    x_diff = float(end_coord[0] - start_coord[0])
    y_diff = float(end_coord[1] - start_coord[1])

    if x_diff == y_diff == 0:
        return []
    elif abs(x_diff) > abs(y_diff):  # Find route in increments of X
        x_step = 1.0 if x_diff > 0 else -1.0  # Positive or negative increments?
        y_step = (y_diff / x_diff) * x_step   # Y per X

        curr_x, curr_y = float(start_coord.x), float(start_coord.y)
        while line_coord[-1] != end_coord:
            curr_x += x_step
            curr_x_int = floor(curr_x)
            curr_y += y_step

            prev_coord = line_coord[-1]
            y_coord_shift = curr_y - float(prev_coord.y)   # How much has Y shifted from previous coord at end of step
            half_y_shift = (y_coord_shift - 0.5 * y_step)  # How much has Y shifted halfway through line-drawing

            if 0.499999 < half_y_shift < 0.500001:
                # Line goes through bottom corner. Floating point error resistant
                if include_touched_coords:
                    line_coord.append(Coord(x=curr_x_int, y=prev_coord.y))
                    line_coord.append(Coord(x=prev_coord.x, y=prev_coord.y + 1))
                line_coord.append(Coord(x=curr_x_int, y=prev_coord.y + 1))
            elif -0.499999 > half_y_shift > -0.500001:
                # Line goes through top corner. Floating point error resistant
                if include_touched_coords:
                    line_coord.append(Coord(x=curr_x_int, y=prev_coord.y))
                    line_coord.append(Coord(x=prev_coord.x, y=prev_coord.y - 1))
                line_coord.append(Coord(x=curr_x_int, y=prev_coord.y - 1))
            elif y_coord_shift >= 0.5 > half_y_shift:  # Y change positive, change happens after x change
                line_coord.append(Coord(x=curr_x_int, y=prev_coord.y))
                line_coord.append(Coord(x=curr_x_int, y=prev_coord.y + 1))
            elif y_coord_shift >= 0.5 < half_y_shift:  # Y change positive, change happens before x change
                line_coord.append(Coord(x=prev_coord.x, y=prev_coord.y + 1))
                line_coord.append(Coord(x=curr_x_int, y=prev_coord.y + 1))
            elif y_coord_shift <= -0.5 < half_y_shift:  # Y change negative, change happens before x change
                line_coord.append(Coord(x=curr_x_int, y=prev_coord.y))
                line_coord.append(Coord(x=curr_x_int, y=prev_coord.y - 1))
            elif y_coord_shift <= -0.5 > half_y_shift:  # Y change negative, change happens after x change
                line_coord.append(Coord(x=prev_coord.x, y=prev_coord.y - 1))
                line_coord.append(Coord(x=curr_x_int, y=prev_coord.y - 1))
            else:  # No Y change this step
                line_coord.append(Coord(x=curr_x_int, y=prev_coord.y))
    else:  # Find route in increments of Y
        y_step = 1.0 if y_diff > 0 else -1.0  # Positive or negative increments?
        x_step = (x_diff / y_diff) * y_step   # X per Y

        curr_x, curr_y = float(start_coord.x), float(start_coord.y)
        while line_coord[-1] != end_coord:
            curr_x += x_step
            curr_y += y_step
            curr_y_int = floor(curr_y)

            prev_coord = line_coord[-1]
            x_coord_shift = curr_x - float(prev_coord.x)   # How much has X shifted from previous coord at end of step
            half_x_shift = (x_coord_shift - 0.5 * x_step)  # How much has X shifted halfway through line-drawing

            if 0.499999 < half_x_shift < 0.500001:
                # Line goes through right corner. Floating point error resistant
                if include_touched_coords:
                    line_coord.append(Coord(x=prev_coord.x + 1, y=prev_coord.y))
                    line_coord.append(Coord(x=prev_coord.x, y=curr_y_int))
                line_coord.append(Coord(x=prev_coord.x + 1, y=curr_y_int))
            elif -0.499999 > half_x_shift > -0.500001:
                # Line goes through left corner. Floating point error resistant
                if include_touched_coords:
                    line_coord.append(Coord(x=prev_coord.x - 1, y=prev_coord.y))
                    line_coord.append(Coord(x=prev_coord.x, y=curr_y_int))
                line_coord.append(Coord(x=prev_coord.x - 1, y=curr_y_int))
            elif x_coord_shift >= 0.5 > half_x_shift:  # X change positive, change happens after y change
                line_coord.append(Coord(x=prev_coord.x, y=curr_y_int))
                line_coord.append(Coord(x=prev_coord.x + 1, y=curr_y_int))
            elif x_coord_shift >= 0.5 < half_x_shift:  # X change positive, change happens before y change
                line_coord.append(Coord(x=prev_coord.x + 1, y=prev_coord.y))
                line_coord.append(Coord(x=prev_coord.x + 1, y=curr_y_int))
            elif x_coord_shift <= -0.5 < half_x_shift:  # X change negative, change happens after y change
                line_coord.append(Coord(x=prev_coord.x, y=curr_y_int))
                line_coord.append(Coord(x=prev_coord.x - 1, y=curr_y_int))
            elif x_coord_shift <= -0.5 > half_x_shift:  # X change negative, change happens before y change
                line_coord.append(Coord(x=prev_coord.x - 1, y=prev_coord.y))
                line_coord.append(Coord(x=prev_coord.x - 1, y=curr_y_int))
            else:  # No X change this step
                line_coord.append(Coord(x=prev_coord.x, y=curr_y_int))
    return line_coord[1:-1]


def spawn_sprite_collection(
        sprite_collection_path: str,
        x_coord: int,
        y_coord: int,
        orientation: str = "down",
        movement_speed: float = None
) -> OrthogonalTiledMapGameObjectSpriteCollection:
    """
    Spawns an object with the given sprite collection at the given coordinates, and returns the resulting object.
    :param sprite_collection_path: The path to use to spawn the sprite collection. Start with 'renpy.store.' to
    spawn an object with a variable sprite collection
    :param x_coord: The x coordinate to spawn the object at
    :param y_coord: The y coordinate to spawn the object at
    :param orientation: Which orientation the object should have. 'up', 'down', 'left' and 'right' are the only valid
    orientations.
    :param movement_speed: What movement speed should
    """
    if movement_speed is None:
        movement_speed = renpy.store.pink_otm_default_npc_move_speed

    object_init_dict = {
        "properties": [
            {"name": "sprite_collection_path", "type": "string", "value": sprite_collection_path},
            {"name": "repeat_commands", "type": "bool", "value": False},
            {"name": "movement_speed", "type": "float", "value": movement_speed}]}

    new_sprite_collection = renpy.store.pink_otm_current_map.add_object_at_coord(
        object_init_dict, x_coord, y_coord, is_player=False, orientation=orientation)
    return new_sprite_collection


class EventWaitCondition:
    """
    This is the parent class for Wait Conditions, which define waits for events to occur on pink engine maps (such as
    movement or zooming) before moving on to the next ren'py line. While a wait is going on, the menu cannot be opened
    because of an issue with loading games from such a state.
    """
    def condition_met(self) -> bool:
        """
        Returns whether the condition is currently met, meaning that this wait should end.
        """
        pass

    def instant_resolve(self):
        """
        An emergency exit for the wait, instantly resolving the current wait so that the conditions are met.
        """
        pass


class MovementWaitCondition(EventWaitCondition):
    def __init__(
            self,
            mover: OrthogonalTiledMapGameObjectMobile,
            x_coord: Optional[int],
            y_coord: Optional[int],
            orientation: Optional[str],
            finished: Optional[bool]
    ):
        """
        Defines an event wait that waits for a specific object to have performed some kind of movement.
        :param mover: Which object's movement should be waited for?
        :param x_coord: What X coordinate should the object have to end the wait? None if you're
        not waiting for a specific X coordinate.
        :param y_coord: What Y coordinate should the object have to end the wait? None if you're
        not waiting for a specific Y coordinate.
        :param orientation: What orientation should the object have to end the wait? None if you're
        not waiting for a specific X coordinate. Not relevant to non-sprite collections
        :param finished: If True, the wait will only be considered complete if the object has completed its current
        movement, and no more movement commands are present in its control stack. If False, the wait will be considered
        completed in the first frame that the conditions are met. Note that this means that it will complete once
        characters start their final movement, rather than when it's complete.
        """
        self.mover = mover
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.orientation = orientation
        self.finished = finished

    def condition_met(self) -> bool:
        """
        Returns True if the mover matches all the conditions that have been set, False if not.
        """
        if not self.mover.is_on_map():
            # Can happen if the mover is added on the same frame as the wait condition
            return False
        central_coord = self.mover.central_coord
        if self.x_coord is not None and central_coord.x != self.x_coord:
            return False
        if self.y_coord is not None and central_coord.y != self.y_coord:
            return False
        if self.orientation is not None and self.mover.orientation != self.orientation:  # noqa
            return False
        if self.finished and (self.mover._current_command is not None or len(self.mover.control_stack) > 0):  # noqa
            return False
        return True

    def instant_resolve(self) -> None:
        """
        If coordinates have been set, sets the mover to those coordinates. If an orientation has been set, sets the
        mover to that orientation.
        """
        if self.x_coord is not None and self.y_coord is not None:
            self.mover.set_to_coords(x_coord=self.x_coord, y_coord=self.y_coord)
        if self.orientation is not None:
            self.mover.orientation = self.orientation  # noqa


class ZoomWaitCondition(EventWaitCondition):
    def __init__(
            self,
            xzoom: Optional[float],
            yzoom: Optional[float],
    ):
        """
        Defines an event wait that waits for the camera to have attained a certain zoom level.
        :param xzoom: Which xzoom should the camera have to end the wait? None if you're
        not waiting for a specific xzoom.
        :param yzoom: Which yzoom should the camera have to end the wait? None if you're
        not waiting for a specific yzoom.
        """
        self.xzoom = xzoom
        self.yzoom = yzoom

    def condition_met(self) -> bool:
        """
        Returns True if the camera matches all the conditions that have been set, False if not.
        """
        if self.xzoom is not None and self.xzoom != renpy.store.pink_otm_current_camera.xzoom:
            return False
        if self.yzoom is not None and self.yzoom != renpy.store.pink_otm_current_camera.yzoom:
            return False
        return True

    def instant_resolve(self) -> None:
        """
        For each zoom level condition that has been set, instantly sets the camera to that zoom level.
        """
        if self.xzoom is not None:
            renpy.store.pink_otm_current_camera.set_x_zoom(self.xzoom)
        if self.yzoom is not None:
            renpy.store.pink_otm_current_camera.set_y_zoom(self.yzoom)


class AlphaWaitCondition(EventWaitCondition):
    def __init__(
            self,
            overlay: Overlay,
            alpha: Optional[float]
    ):
        """
        :param overlay: which overlay to wait for
        :param alpha: Which alpha would end the wait?
        """
        self.overlay = overlay
        self.alpha = alpha
        self.start_alpha = overlay.alpha

    def condition_met(self) -> bool:
        """
        Returns True if the layer matches all the conditions that have been set, False if not.
        """
        if self.alpha is not None:
            if self.start_alpha > self.alpha and self.overlay.alpha > self.alpha:
                return False
            elif self.start_alpha < self.alpha and self.overlay.alpha < self.alpha:
                return False
        return True

    def instant_resolve(self) -> None:
        """
        Instantly sets the layer to the alpha level
        """
        if self.alpha is not None:
            self.overlay.set_alpha(self.alpha, 0.0)


class OverlayMoveCondition(EventWaitCondition):
    def __init__(
            self,
            overlay: Overlay,
            x: Optional[int],
            y: Optional[int],
            width: Optional[int],
            height: Optional[int]
    ):
        """
        :param overlay: which overlay to wait for
        :param x: Which x would end the wait?
        :param y: Which y would end the wait?
        :param width: Which width would end the wait?
        :param height: Which height would end the wait?
        """
        self.overlay = overlay
        self.x = x
        self.start_x = overlay.x
        self.y = y
        self.start_y = overlay.y
        self.width = width
        self.start_width = overlay.width
        self.height = height
        self.start_height = overlay.height

    def condition_met(self) -> bool:
        """
        Returns True if the camera matches all the conditions that have been set, False if not.
        """
        if self.x is not None:
            if self.start_x > self.x and self.overlay.x > self.x:
                return False
            elif self.start_x < self.x and self.overlay.x < self.x:
                return False

        if self.y is not None:
            if self.start_y > self.y and self.overlay.y > self.y:
                return False
            elif self.start_y < self.y and self.overlay.y < self.y:
                return False

        if self.width is not None:
            if self.start_width > self.width and self.overlay.width > self.width:
                return False
            elif self.start_width < self.width and self.overlay.width < self.width:
                return False

        if self.height is not None:
            if self.start_height > self.height and self.overlay.height > self.height:
                return False
            elif self.start_height < self.height and self.overlay.height < self.height:
                return False
        return True

    def instant_resolve(self) -> None:
        """
        Instantly sets the overlay to the set dimensions.
        """
        self.overlay.set_dimensions(self.x, self.y, self.width, self.height, move_time=0.0)


class EventWait:
    # States that the wait can be in
    STATE_WAITING_FOR_START = 0  # Not started
    STATE_CONDITION_WAIT = 1  # Waiting for conditions to be met
    STATE_COMPLETION_WAIT = 2  # Waiting for additional completion wait to be done
    STATE_FINISHED = 3

    def __init__(self, max_time: Optional[float], completion_wait: float):
        """
        Instances of this class represent a wait between two lines during a ren'py event, during which certain
        conditions must be met in the pink engine (such as characters moving, or the camera zooming) for the game
        to continue.
        :param max_time: The maximum amount of time that the wait will last. If not None, the wait will always end
        after the given amount of time has passed, with the instant_resolve() function on each wait called. This
        should be used purely as an escape mechanism if you fear the game might get stuck in a perpetual wait.
        :param completion_wait: The amount of additional seconds to wait after all set conditions have been met.
        """
        self.max_time = max_time
        self.completion_wait = completion_wait

        self._conditions: List[EventWaitCondition] = []
        self._start_time: Optional[float] = None
        self._state: int = self.STATE_WAITING_FOR_START

    def add_movement_condition(
            self,
            mover: OrthogonalTiledMapGameObjectMobile,
            x_coord: Optional[int],
            y_coord: Optional[int],
            orientation: Optional[str],
            finished: Optional[bool]
    ) -> None:
        """
        Adds an event wait condition for a specific object to have performed some kind of movement.
        :param mover: Which object's movement should be waited for?
        :param x_coord: What X coordinate should the object have to end the wait? None if you're
        not waiting for a specific X coordinate.
        :param y_coord: What Y coordinate should the object have to end the wait? None if you're
        not waiting for a specific Y coordinate.
        :param orientation: What orientation should the object have to end the wait? None if you're
        not waiting for a specific X coordinate. Not relevant to non-sprite collections
        :param finished: If True, the wait will only be considered complete if the object has completed its current
        movement, and no more movement commands are present in its control stack. If False, the wait will be considered
        completed in the first frame that the conditions are met. Note that this means that it will complete once
        characters start their final movement, rather than when it's complete.
        """
        self._conditions.append(
            MovementWaitCondition(
                mover=mover, x_coord=x_coord, y_coord=y_coord, orientation=orientation, finished=finished))

    def add_zoom_condition(self, xzoom: Optional[float], yzoom: Optional[float]) -> None:
        """
        Adds an event wait condition for the camera to have attained a certain zoom level.
        :param xzoom: Which xzoom should the camera have to end the wait? None if you're
        not waiting for a specific xzoom.
        :param yzoom: Which yzoom should the camera have to end the wait? None if you're
        not waiting for a specific yzoom.
        """
        self._conditions.append(ZoomWaitCondition(xzoom=xzoom, yzoom=yzoom))

    def add_alpha_condition(self, overlay: Overlay, alpha: Optional[float]) -> None:
        """
        Adds an event wait condition for an overlay to reach a certain alpha level.
        :param overlay: which overlay to wait for
        :param alpha: Which alpha would end the wait?
        """
        self._conditions.append(AlphaWaitCondition(overlay=overlay, alpha=alpha))

    def add_overlay_movement_condition(
            self, overlay: Overlay, x: Optional[int], y: Optional[int], width: Optional[int], height: Optional[int]
    ) -> None:
        """
        Adds an event wait condition for an overlay to reach a certain alpha level.
        :param overlay: which overlay to wait for
        :param x: Which x would end the wait?
        :param y: Which y would end the wait?
        :param width: Which width would end the wait?
        :param height: Which height would end the wait?
        """
        self._conditions.append(OverlayMoveCondition(overlay=overlay, x=x, y=y, width=width, height=height))

    def st_reset(self, old_last_gt: float, new_st: float) -> None:
        """
        Ensures that the timing is kept consistent if an ST reset takes place
        :param old_last_gt: The gt for the previous frame
        :param new_st: The gt for the new frame
        """
        time_passed = old_last_gt - self._start_time
        self._start_time = time_passed + new_st

    def start_wait(self) -> None:
        """
        Starts this event wait, preventing menus from being opened, or new ren'py lines from being triggered until
        either the conditions are met and an additional amount of seconds equal to the completion_wait has passed, or
        the max_time has passed.
        """
        # Prevents screen from being opened
        renpy.store.pink_otm_game_menu_screen_cache = renpy.store._game_menu_screen  # noqa
        renpy.store._game_menu_screen = None

        self._start_time = renpy.store.pink_otm_current_map.last_gt
        self._state = self.STATE_CONDITION_WAIT

        # So that a pause is immediately triggered if conditions aren't met, and no pause is triggered if all conditions
        # are met from the start
        self.check_wait(self._start_time)

    def _check_conditions(self) -> bool:
        """
        Checks all the conditions in this wait, returns True if all conditions are met, False if not.
        """
        for condition in self._conditions:
            if not condition.condition_met():
                return False
        return True

    def _emergency_end(self) -> None:
        """
        Calls the instant_resolve function on all conditions in this wait, to force the conditions to conclude.
        """
        for condition in self._conditions:
            condition.instant_resolve()
        self._end_wait()

    def check_wait(self, st: float) -> None:
        """
        This function is called once per frame to see if the wait has been resolved yet.
        :param st: The gt for the pink engine's current frame.
        """
        if self.max_time is not None and st > self._start_time + self.max_time:
            self._emergency_end()
        else:
            if self._state == self.STATE_CONDITION_WAIT:
                if self._check_conditions():
                    self._state = self.STATE_COMPLETION_WAIT
                    self._start_time = st

            if self._state == self.STATE_COMPLETION_WAIT:
                if st >= self._start_time + self.completion_wait:
                    self._state = self.STATE_FINISHED

            if self._state == self.STATE_FINISHED:
                self._end_wait()
            else:
                # If not finished, pause ren'py processing
                return

    @staticmethod
    def _end_wait() -> None:
        """
        Ends the current wait, restoring access to the menu.
        """
        renpy.store._game_menu_screen = renpy.store.pink_otm_game_menu_screen_cache
        renpy.store.pink_otm_game_menu_screen_cache = None
        renpy.store.pink_otm_current_map.current_event_wait = None


def initiate_event_wait(max_time: Optional[float] = None, completion_wait: float = 0.0) -> None:
    """
    Tries to initiate an event wait for the current map. If an event wait already exists, calling this function
    before the last one has completed will result in a fatal error.
    :param max_time: The maximum amount of time that the wait will last. If not None, the wait will always end
    after the given amount of time has passed, with the instant_resolve() function on each wait called. This
    should be used purely as an escape mechanism if you fear the game might get stuck in a perpetual wait.
    :param completion_wait: The amount of additional seconds to wait after all set conditions have been met.
    """
    if (
            renpy.store.pink_otm_current_map is not None and
            renpy.store.pink_otm_current_event_name is not None and
            renpy.store.pink_otm_current_map.current_event_wait is None
    ):
        renpy.store.pink_otm_current_map.current_event_wait = EventWait(
            max_time=max_time, completion_wait=completion_wait)
    else:
        raise RuntimeError(
            "Invalid movement wait initiation. A movement wait can only be initiated if a Pink OTM map is currently "
            "active, an event is currently going on, and no previous movement wait exists.")


def add_movement_wait(
        mover: Union[str, OrthogonalTiledMapGameObjectMobile],
        x_coord: Optional[int] = None,
        y_coord: Optional[int] = None,
        orientation: Optional[str] = None,
        finished: Optional[bool] = True
) -> None:
    """
    Adds an event wait condition to the current event wait for a specific object to have performed some kind of
    movement. If no event wait exists, throws an error.
    :param mover: Which object's movement should be waited for?
    :param x_coord: What X coordinate should the object have to end the wait? None if you're
    not waiting for a specific X coordinate.
    :param y_coord: What Y coordinate should the object have to end the wait? None if you're
    not waiting for a specific Y coordinate.
    :param orientation: What orientation should the object have to end the wait? None if you're
    not waiting for a specific X coordinate. Not relevant to non-sprite collections
    :param finished: If True, the wait will only be considered complete if the object has completed its current
    movement, and no more movement commands are present in its control stack. If False, the wait will be considered
    completed in the first frame that the conditions are met. Note that this means that it will complete once
    characters start their final movement, rather than when it's complete.
    """
    if renpy.store.pink_otm_current_map.current_event_wait is None:
        raise RuntimeError(
            "Cannot add movement wait. No wait has been initiated.")

    if type(mover) is str:  # noqa
        moving_object: OrthogonalTiledMapGameObjectMobile = getattr(renpy.store, mover)
    else:
        moving_object: OrthogonalTiledMapGameObjectMobile = mover

    renpy.store.pink_otm_current_map.current_event_wait.add_movement_condition(
        mover=moving_object, x_coord=x_coord, y_coord=y_coord, orientation=orientation, finished=finished)


def add_zoom_wait(
        zoom: Optional[float] = None,
        xzoom: Optional[float] = None,
        yzoom: Optional[float] = None
) -> None:
    """
    Adds an event wait condition for the camera to have attained a certain zoom level. If no event wait exists, throws
    an error. If initiated without parameters, uses the current target zooms from the smooth zoom controller as
    parameters.
    :param zoom: used to set xzoom and yzoom at once.
    :param xzoom: Which xzoom should the camera have to end the wait?
    :param yzoom: Which yzoom should the camera have to end the wait?
    """
    if renpy.store.pink_otm_current_map.current_event_wait is None:
        raise RuntimeError(
            "Cannot add movement wait. No wait has been initiated.")

    if zoom is not None:
        xzoom = zoom
        yzoom = zoom
    else:
        if xzoom is None:
            xzoom = renpy.store.pink_otm_zoom_controller.target_xzoom
        if yzoom is None:
            yzoom = renpy.store.pink_otm_zoom_controller.target_yzoom

    renpy.store.pink_otm_current_map.current_event_wait.add_zoom_condition(
        xzoom=xzoom, yzoom=yzoom)


def add_alpha_wait(
        overlay: Overlay,
        alpha: Optional[float] = None
) -> None:
    """
    Adds an event wait condition for an overlay to have attained a certain level of alpha. If no event wait exists,
    throws an error. If initiated without parameters, uses the target_alpha of the given overlay.
    :param overlay: which overlay to wait for
    :param alpha: Which alpha would end the wait?
    """
    if renpy.store.pink_otm_current_map.current_event_wait is None:
        raise RuntimeError(
            "Cannot add movement wait. No wait has been initiated.")

    if alpha is None:
        alpha = overlay.target_alpha

    renpy.store.pink_otm_current_map.current_event_wait.add_alpha_condition(
        overlay=overlay, alpha=alpha)


def add_overlay_movement_wait(
        overlay: Overlay,
        x: int = None,
        y: int = None,
        width: int = None,
        height: int = None
) -> None:
    """
    Adds an event wait condition for an overlay to have attained certain dimensions. If no event wait exists,
    throws an error. If initiated without parameters, uses the target_dimensions of the given overlay.
    :param overlay: which overlay to wait for
    :param x: Which x would end the wait?
    :param y: Which y would end the wait?
    :param width: Which width would end the wait?
    :param height: Which height would end the wait?
    """
    if renpy.store.pink_otm_current_map.current_event_wait is None:
        raise RuntimeError(
            "Cannot add movement wait. No wait has been initiated.")

    if x is None:
        x = overlay.target_x
    if y is None:
        y = overlay.target_y
    if width is None:
        width = overlay.target_width
    if height is None:
        height = overlay.target_height

    renpy.store.pink_otm_current_map.current_event_wait.add_overlay_movement_condition(
        overlay=overlay, x=x, y=y, width=width, height=height)


def start_event_wait():
    """
    Starts the currently initialized event wait, preventing menus from being opened until the event wait is resolved.
    """
    if renpy.store.pink_otm_current_map.current_event_wait is not None:
        renpy.store.pink_otm_current_map.current_event_wait.start_wait()
    else:
        raise RuntimeError(
            "Cannot start movement wait. No wait has been initiated.")


def change_walk_speed(new_speed: float):
    """
    More sensibly located synonym for the change_walk_speed function on the map.
    """
    renpy.store.pink_otm_current_map.change_walk_speed(new_speed)


def change_run_speed(new_speed: float):
    """
    More sensibly located synonym for the change_run_speed function on the map.
    """
    renpy.store.pink_otm_current_map.change_walk_speed(new_speed)


def play_locational_sound(
        path: str,
        x_coord: int,
        y_coord: int,
        pan: bool = True,
        scale: bool = True,
        max_volume_distance: float = 1,
        min_volume_distance: Optional[float] = None,
        min_volume: float = 0.0,
        max_volume: float = 1.0,
        max_pan_distance: float = None,
        no_pan_distance: Optional[float] = 0,
        max_pan: float = 1.0,
        mixer: str = 'sfx'
):
    renpy.store.pink_sound_manager.play_sound(
        sound_file=path,
        emitter=Coord(x_coord, y_coord),
        pan=pan,
        scale=scale,
        max_volume_distance=max_volume_distance,
        min_volume_distance=min_volume_distance,
        min_volume=min_volume,
        max_volume=max_volume,
        max_pan_distance=max_pan_distance,
        no_pan_distance=no_pan_distance,
        max_pan=max_pan,
        mixer=mixer)
    

def disable_rendering():
    renpy.store.pink_render_enabled = False


def enable_rendering():
    renpy.store.pink_render_enabled = True


# Bug fix: Switching from a sprite collection with directional animations to one with non-directional animations
#  no longer causes a crash
# Bug fix: added a run to the empty sprite collection so it can be used to replace followers
# bug fix: slight shift on ST reset for shakers
# bug fix: pause shaking and overlay shifting during screen freeze, but not static event.
# Default values for screen shakes
# Added pink_otm_nearest variable, so you can adjust the nearest value during your game.


# TODO Next release:
#  -Smooth zooming near the edges of maps ain't that smooth
#  - DONE
#  -Smooth zooming on large maps aint't that smooth.
#  -A shaker with a duration of None makes the screen shake until interrupted.
#  -Animated screen overlay with cloud cover and rain effects.
#  -Universal timer
#   - Basics done, with code and event triggerable both. Still needs test
#   - Added pause functionality, still needs to test.
#   - Want to add config options that auto-pause on event classes.
#   - Added pause on screen freeze functionality still need to test.
#   - Cancelling timed event and then retriggering doesn't work.
#  -Diagonal movement.
#  -player_interaction no longer has mandatory arguments.

# Added is_moving
# Added click-to-move.
# Fixed issue where object was redefined due to shadow naming (pink_otm_movement_wait redefined the basic 'object'
# of ren'py)


# TODO make switch_target take ref_name
# TODO More elegant reset system for events
# TODO room and conditional layer test map
# TODO hopping cutscene, rather than hopping movement.
# TODO Follower movement prefer valid movement over non-valid?
# TODO Random Delay

# TODO Room A010B - mild glitching when interacting with sign. This one is gonna be tricky.

# Delayed until later releases:
# TODO: Bug where using end of game door after tiled map doors fails to work properly
# TODO clearer error on go_to_map out of bounds.

# TODO standard event for tmd maps

# TODO fancy map sidescroller
# TODO fancy map push boxes
# TODO fancy map custom special movement
# TODO more extensive code_on_leave example

# TODO rotation and flipping
#  Added TODOS in tiled_game.py for flipping of tiles. These flips together add up to 90 degree rotations as well,
#  which is suppported by tiled.
#   Sample map, constructed from just three tiles on tile layers:
#    - Floor tile. Two green corners, one blue corner, one empty corner, together can form a floor pattern through both
#       rotating and flipping.
#    - Wall tile. Boundary on one side, used for both floor and ceiling.
#    - Boundary tile. Rotatable edge, used to define edge of floors and ceilings alike.

# TODO layered sprite collection creation
#  Define different 'body parts'. A sprite is constructed by attaching the appropriate body parts along the appropriate
#   attachment points.
#  A body part has
#   attachment points (coordinates for where it connects to other things, like where arms connect to the body)
#   A color index (indicating replaceable colors)
#   animation list (the animation of a sprite collection is defined by the sum of animation of its body parts. If a
#   body part is present but has no set animation for an animation, it will appear in its default state.)
#   Layer index (to indicate on what layer it should be drawn)
#   Tags
#   Logic to display a different version depending on tags.
#  a body part is defined in a folder that contains a file called bodypart.txt as well as a list of images. The text
#  file contains all the body part data.
#  Examples with different types of complexity. One is just a body, hair, a clothing overlay, and an eyes overlay.
#  The other is the full gamut, with every distinct body part being its own, well, body part, clothing being similarly
#  split.
#  Have to start thinking about what all the 'default' animations are before starting to work on this.
