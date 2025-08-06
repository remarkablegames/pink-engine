from typing import Optional

import renpy  # noqa


class ControlCommand(object):
    untimed_types = {"change_stand_animation", "change_move_animation", "change_movement_speed", "go_custom"}

    def __init__(self, command_type, **kwargs):
        """
        This class represents a single command, to be given to a sprite to change its position or animation.
        :param str command_type: the type of the command.
        """
        self.type = command_type

        self.properties = {}

        for property_name in kwargs:
            self.properties[property_name] = kwargs[property_name]

        if 'never_repeat' not in self.properties:
            if renpy.store.pink_otm_current_event_type is not None:
                self.properties['never_repeat'] = renpy.store.default_never_repeat_during_event
            else:
                self.properties['never_repeat'] = False

    @property
    def turn_and_move(self):
        """
        :return: Used for 'go' commands, specifies whether to turn and move in a single command (if true), or do just
        one of the two. True by default.
        :rtype: bool
        """
        if 'turn_and_move' in self.properties:
            return self.properties['turn_and_move']
        else:
            return True

    @property
    def stand_on_turn(self):
        """
        :return: Used for the 'turn' commands, specifying whether to switch to the a stand animation when turning. True
        by default.
        :rtype: bool
        """
        if 'stand_on_turn' in self.properties:
            return self.properties['stand_on_turn']
        else:
            return True

    @property
    def animate_invalid_move(self):
        """
        :return: Used for the 'move' command, specifying whether to continue using the walk animation when a move is
        deemed invalid. True by default.
        :rtype: bool
        """
        if 'animate_invalid_move' in self.properties:
            return self.properties['animate_invalid_move']
        else:
            return True

    @property
    def pop_invalid_move(self):
        """
        :return: Used for the 'move command', specifying whether to remove a command from the stack when invalid,
        or whether to retry it on the next move.
        :rtype: bool
        """
        if 'pop_invalid_move' in self.properties:
            return self.properties['pop_invalid_move']
        else:
            return False

    @property
    def quantity(self):
        """
        :return: Used in various functions, to specify a numeric input value.
        :rtype: float
        """
        if 'quantity' in self.properties:
            return self.properties['quantity']
        else:
            return None

    @property
    def animation_name(self):
        """
        :return: Used in the play_animation, change_stand_animation and change_move_animation commands, to provide an
        animation name.
        :rtype: str
        """
        if 'animation_name' in self.properties:
            return self.properties['animation_name']
        else:
            return ""

    @property
    def animation_speed(self):
        """
        :return: Used in the play_animation function, to provide an animation speed.
        :rtype: float
        """
        if 'animation_speed' in self.properties:
            return self.properties['animation_speed']
        else:
            return None

    @property
    def set_movement_time(self):
        """
        :return: Whether this animation updates the most recent movement time (if not, causes next command to execute
        immediately). Used by all commands.
        :rtype bool
        """
        if 'set_movement_time' in self.properties:
            return self.properties['set_movement_time']
        else:
            if self.type in self.untimed_types:
                return False
            else:
                return True

    @property
    def target(self):
        """
        :return: Used by the move_to command, determining the target.
        :rtype: Union[tuple, str]
        """
        if 'target' in self.properties:
            return self.properties['target']
        else:
            return 0, 0

    @property
    def prev_coord(self):
        """
        :return: Used by the go_to command, making the movement go to the object's previous target rather than its
        current.
        :rtype: bool
        """
        if 'prev_coord' in self.properties:
            return self.properties['prev_coord']
        else:
            return False

    @property
    def exclude_current_direction(self):
        """
        :return: Used by the 'turn_random' command, whether the current direction should be excluded.
        :rtype: bool
        """
        if 'exclude_current_direction' in self.properties:
            return self.properties['exclude_current_direction']
        else:
            return True

    @property
    def max_x(self):
        """
        :return: Used by the 'go_random' command, determining the bounds of the random movement.
        :rtype: int
        """
        if 'max_x' in self.properties:
            return self.properties['max_x']
        else:
            pink_otm_current_map = renpy.store.pink_otm_current_map  # Py2
            return pink_otm_current_map.grid_size.x - 1

    @property
    def max_y(self):
        """
        :return: Used by the 'go_random' command, determining the bounds of the random movement.
        :rtype: int
        """
        if 'max_y' in self.properties:
            return self.properties['max_y']
        else:
            pink_otm_current_map = renpy.store.pink_otm_current_map  # Py2
            return pink_otm_current_map.grid_size.y

    @property
    def min_x(self):
        """
        :return: Used by the 'go_random' command, determining the bounds of the random movement.
        :rtype: int
        """
        if 'min_x' in self.properties:
            return self.properties['min_x']
        else:
            return 0

    @property
    def min_y(self):
        """
        :return: Used by the 'go_random' command, determining the bounds of the random movement.
        :rtype: int
        """
        if 'min_y' in self.properties:
            return self.properties['min_y']
        else:
            return 0

    @property
    def single_step(self):
        """
        :return: Used by the go_to command. If True, causes the movement to only cause a single step.
        :rtype: bool
        """
        if 'single_step' in self.properties:
            return self.properties['single_step']
        else:
            return False

    @property
    def never_repeat(self):
        """
        :return: Prevents the command from being repeated. Used if one command spawns more commands.
        :rtype: bool
        """
        if 'never_repeat' in self.properties:
            return self.properties['never_repeat']
        else:
            return False

    @property
    def move_by_x(self):
        """
        :return: Used by the go_custom command, setting the x movement in the next movement.
        :rtype: int
        """
        if 'move_by_x' in self.properties:
            return self.properties['move_by_x']
        else:
            return 0

    @property
    def move_by_y(self):
        """
        :return: Used by the go_custom command, setting the y movement in the next movement.
        :rtype: int
        """
        if 'move_by_y' in self.properties:
            return self.properties['move_by_y']
        else:
            return 0

    @property
    def movement_time(self):
        """
        :return: Used to set a custom movement_time for only a single movement.
        :rtype: float
        """
        if 'movement_time' in self.properties:
            return self.properties['movement_time']
        else:
            return None

    @property
    def instant(self):
        """
        :return: When this command is consumed, the code immediately starts consuming the next command, without waiting
        for a tick to pass. WARNING: This can cause infinite recursion errors, and nasty crashes. Should only be used
        if you really know what you are doing.
        :rtype: bool
        """
        if 'instant' in self.properties:
            return self.properties['instant']
        else:
            return None

    @property
    def path(self):
        """
        :return: Used to specify filepaths in commands.
        :rtype: str
        """
        if 'path' in self.properties:
            return self.properties['path']
        else:
            return None

    @property
    def channel(self):
        """
        :return: Used to specify audio channels in commands
        :rtype: str
        """
        if 'channel' in self.properties:
            return self.properties['channel']
        else:
            return None

    @property
    def pathfinding_path(self):
        """
        :return: Automatically set by pathfinding function, don't set manually. Contains the path currently calculated
        by the pathfinding function
        :rtype: list
        """
        if 'pathfinding_path' in self.properties:
            return self.properties['pathfinding_path']
        else:
            return None

    @pathfinding_path.setter
    def pathfinding_path(self, value):
        self.properties['pathfinding_path'] = value

    @property
    def path_target(self):
        """
        :return: Automatically set by pathfinding function, don't set manually. Contains the target that the pathfinding
        path was calculated for. Used to determine whether the target has moved and the path must be recalculated.
        :rtype: tuple
        """
        if 'path_target' in self.properties:
            return self.properties['path_target']
        else:
            return None

    @path_target.setter
    def path_target(self, value):
        self.properties['path_target'] = value

    @property
    def max_path_length(self):
        """
        :return: the maximum amount of steps generated by the pathfinding algorithm
        :rtype: int
        """
        if 'max_path_length' in self.properties:
            return self.properties['max_path_length']
        else:
            return 10

    @property
    def ignore_elements(self):
        """
        :return: Which objects to ignore the movement rules of during movement
        :rtype: list
        """
        if 'ignore_elements' in self.properties:
            return self.properties['ignore_elements']
        else:
            return []

    @property
    def arc_height(self):
        """
        :return: The arc height to attach to a movement, causing the y to be incremented with an inverted parabola
        with the given value as the maximum height.
        :rtype: float
        """
        if 'arc_height' in self.properties:
            return self.properties['arc_height']
        else:
            return 0.0

    @property
    def orientation(self):
        """
        :return: Which direction a character should face during a 'special move'
        :rtype: str|None
        """
        if 'orientation' in self.properties:
            return self.properties['orientation']
        else:
            return None

    @property
    def target_distance(self) -> int:
        """
        :return: Used by the go_to_smart command, to set the distance a smart movement should take an object from
        its target.
        """
        if 'target_distance' in self.properties:
            return self.properties['target_distance']
        else:
            return 0

    @property
    def code(self) -> str:
        """
        :return: used by the execute_code command, this is the code that should be run in string form.
        """
        if 'code' in self.properties:
            return self.properties['code']
        else:
            return 'pass'

    @property
    def scale_sound(self) -> bool:
        """
        :return: used by any sound-emitting commands, this determines if the sound volume should scale based off the
        distance between the emitter and the center of the camera.
        """
        if 'scale_sound' in self.properties:
            return self.properties['scale_sound']
        else:
            return False

    @property
    def max_volume_distance(self) -> int:
        """
        :return: used by any sound-emitting commands, the distance in tiles up to which the sound will play at maximum
        volume
        """
        if 'max_volume_distance' in self.properties:
            return self.properties['max_volume_distance']
        else:
            return 1

    @property
    def min_volume_distance(self) -> int:
        """
        :return: used by any sound-emitting commands, the distance in tiles from which the sound will play at the
        minimum volume
        """
        if 'min_volume_distance' in self.properties:
            return self.properties['min_volume_distance']
        else:
            return renpy.store.pink_otm_default_min_volume_distance

    @property
    def min_volume(self) -> float:
        """
        :return: used by any sound-emitting commands, minimum volume to which sound scaling can reduce the sound.
        """
        if 'min_volume' in self.properties:
            return self.properties['min_volume']
        else:
            return 0.0

    @property
    def max_volume(self) -> float:
        """
        :return: used by any sound-emitting commands, maximum volume to which sound scaling can increase the sound.
        """
        if 'max_volume' in self.properties:
            return self.properties['max_volume']
        else:
            return 1.0

    @property
    def pan_sound(self) -> bool:
        """
        :return: used by any sound-emitting commands, this determines if the sound panning should change based off the
        horizontal distance between the emitter and the center of the camera.
        """
        if 'pan_sound' in self.properties:
            return self.properties['pan_sound']
        else:
            return False

    @property
    def max_pan_distance(self) -> int:
        """
        :return: used by any sound-emitting commands, the distance in tiles from which the sound will play fully panned.
        """
        if 'max_pan_distance' in self.properties:
            return self.properties['max_pan_distance']
        else:
            return renpy.store.pink_otm_default_max_pan_distance

    @property
    def no_pan_distance(self) -> int:
        """
        :return: used by any sound-emitting commands, the distance in tiles up to which the sound object will not pan
        """
        if 'no_pan_distance' in self.properties:
            return self.properties['no_pan_distance']
        else:
            return 0

    @property
    def max_pan(self) -> float:
        """
        :return: used by any sound-emitting commands, the absolute maximum level of panning that can be achieved by
        changing position relative to the emitting object. Note that this sets the value for both the maximum left
        pan and right pan.
        """
        if 'max_pan' in self.properties:
            return self.properties['max_pan']
        else:
            return 1.0

    @property
    def mixer(self) -> str:
        """
        :return: used by any sound-emitting commands. Which sound mixer (sound slider in the settings) should be used
        to control the volume of the sound. This only valid options are the default mixers of 'sfx', 'music' and
        'voice', with no built-in support for custom mixers. Defaults to 'sfx', which is the sound slider.
        """
        if 'mixer' in self.properties:
            return self.properties['mixer']
        else:
            return 'sfx'

    @property
    def interact_on_fail(self) -> bool:
        """
        :return: used in move commands, indicating that if the movement is not possible, an interaction should be
        executed instead. Used when controlling a character by holding a mouse, letting you interact with stuff by
        running into it.
        """
        if 'interact_on_fail' in self.properties:
            return self.properties['interact_on_fail']
        else:
            return False

    def __repr__(self):
        return self.type
