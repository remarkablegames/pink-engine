import collections
import renpy   # noqa - import necessary for conditional_met evaluations, otherwise those can't access renpy vars.

from typing import NamedTuple

Area = collections.namedtuple('Area', 'start_x end_x start_y end_y')


class Coord(NamedTuple):
    x: int
    y: int

    @property
    def left(self) -> 'Coord':
        return Coord(self.x - 1, self.y)

    @property
    def right(self) -> 'Coord':
        return Coord(self.x + 1, self.y)

    @property
    def up(self) -> 'Coord':
        return Coord(self.x, self.y - 1)

    @property
    def down(self) -> 'Coord':
        return Coord(self.x, self.y + 1)

    def direction(self, direction: str) -> 'Coord':
        if direction == "left":
            return self.left
        elif direction == "right":
            return self.right
        elif direction == "up":
            return self.up
        elif direction == "down":
            return self.down


class MapElement(object):
    def __init__(self, element_dict, parent=None):
        """
        The parent class of all images that appear on maps.

        :param dict element_dict: Dictionary describing the element, as imported from a .json file.
        :param MapElement parent: Parent object, to copy properties from.
        Parent class for items displayed on Pink Engine maps.
        """
        self._image_width = 0  # Overwritten by children
        self._image_height = 0  # Overwritten by children
        self._image = ""  # Overwritten by children

        if parent:
            self.properties = parent.properties.copy()
        else:
            self.properties = {}

        if element_dict.get('properties'):
            for element_property in element_dict['properties']:
                self.properties[element_property['name']] = element_property['value']

    @property
    def move_from(self):
        """
        :return: The movement allowed from a square occupied by this object.
        :rtype: str or NoneType
        """
        if "move_from" in self.properties:
            return self.properties["move_from"]
        else:
            return None

    @property
    def move_to(self):
        """
        :return: The movement allowed to a square occupied by this object.
        :rtype: str or NoneType
        """
        if "move_to" in self.properties:
            return self.properties["move_to"]
        else:
            return None

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
            return self.image_width

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
            return self.image_height

    @property
    def event_on_activate(self):
        """
        :return: The name of the event triggered by interacting with the object.
        :rtype: str or NoneType
        """
        if "event_on_activate" in self.properties:
            return self.properties["event_on_activate"]
        else:
            return None

    @property
    def event_on_touch(self):
        """
        :return: The name of the event triggered by touching the object (standing on the same tile)
        :rtype: str or NoneType
        """
        if "event_on_touch" in self.properties:
            return self.properties["event_on_touch"]
        else:
            return None

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
    def code_on_activate(self):
        """
        :return: The code triggered by interacting with the object.
        :rtype: str or NoneType
        """
        if "code_on_activate" in self.properties:
            return self.properties["code_on_activate"]
        else:
            return None

    def run_code_on_activate(self):
        exec(self.code_on_activate)

    @property
    def code_on_touch(self):
        """
        :return: The code to be run when touching the object (standing on the same tile)
        :rtype: str or NoneType
        """
        if "code_on_touch" in self.properties:
            return self.properties["code_on_touch"]
        else:
            return None

    def run_code_on_touch(self):
        exec(self.code_on_activate)

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
    def conditional(self):
        """"
        :return: A string that equates to a condition under which the object should appear on the map.
        :rtype: str
        """
        if "conditional" in self.properties:
            return self.properties["conditional"]
        else:
            return "True"

    @property
    def conditional_met(self):
        """
        :return: Whether or not the conditional is currently met.
        :rtype: bool
        """
        return eval(self.conditional)

    @property
    def image(self):
        """
        :return: path to image representing this object.
        :rtype: str or NoneType
        """
        return self._image

    @property
    def image_height(self):
        """
        :return: path to image representing this object.
        :rtype: str or NoneType
        """
        return self._image_height

    @property
    def image_width(self):
        """
        :return: path to image representing this object.
        :rtype: str or NoneType
        """
        return self._image_width
