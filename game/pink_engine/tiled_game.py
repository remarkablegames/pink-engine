import renpy  # noqa
import pygame  # noqa
import json
from math import ceil, floor, pow, sqrt, sin, pi
from collections import OrderedDict
from typing import List, Optional, Dict, Tuple
import os

from pink_engine.commons import Coord
from pink_engine.tileset import Tileset, TilesetTile, TilesetAnimatedTile, pink_tileset_dict

Dimensions = Tuple[int, int, int, int]  # start x, start y, width, height

# ======================================================================================================================
# =============================================GLOBAL SETTINGS==========================================================
# ======================================================================================================================

LAYER_PRIORITY = {
    'sub': 0,
    'move_sub': 1,
    'dynamic': 2,
    'move_dynamic': 3,
    'super': 4,
    'move_super': 5,
    'interaction': 6}
VISIBLE_LAYERS = {'sub', 'dynamic', 'super'}


# ======================================================================================================================
# =============================================VISUAL===================================================================
# ======================================================================================================================

class GameTimerTimedCode:
    def __init__(self, time: float, code: str, code_id: Optional[str]):
        """
        Instances of this class represent a single piece of code that is on a timer, and will be played when that
        timer is hit.
        :param time: The amount of time (in seconds) the timer clock needs to reach to trigger this code
        :param code: The code to trigger
        :param code_id: The ID for this code. Giving a timer an ID is necessary if you want the option of canceling it
        later, or showing how much time remains.
        """
        self.time = time
        self.code = code
        self.code_id = code_id

    def execute(self) -> None:
        """
        Executes the code in this timer.
        """
        exec(self.code)


class GameTimerTimedEvent:
    def __init__(self, time: float, event: str, event_args: tuple, event_kwargs: dict, event_id: Optional[str]):
        """
        Instances of this class represent a single event that is on a timer, and should be called when the time is hit.
        The actual event-calling code is found in the specific game map.
        timer is hit.
        :param time: The amount of time (in seconds) the timer clock needs to reach to trigger this event.
        :param event: The label of the event to trigger to trigger
        :param event_args: The args to pass along to the label.
        :param event_kwargs: The kwargs to pass along to the label.
        :param event_id: The ID for this event. Giving a timer an ID is necessary if you want the option of canceling it
        later, or showing how much time remains.
        """
        self.time = time
        self.event = event
        self.event_args = event_args
        self.event_kwargs = event_kwargs
        self.event_id = event_id


class GameTimer:
    def __init__(self):
        """
        Instances of this class represents the timer for a single game mode. It checks for both code and events that
        should be called at specific times.
        """
        # Represents the amount of seconds that a particular game mode has been played.
        self.raw_time: float = 0.0

        # The raw time, plus the amount of incremented time, used to keep track of in-game time.
        self.time: float = 0.0

        self.next_code_trigger: Optional[float] = None
        self.next_event_trigger: Optional[float] = None

        self._code_ids: Dict[str, GameTimerTimedCode] = {}
        self._event_ids: Dict[str, GameTimerTimedEvent] = {}

        self._timed_code_dict: Dict[float, List[GameTimerTimedCode]] = {}
        self._timed_event_dict: Dict[float, List[GameTimerTimedEvent]] = {}

        # Two different pause variables allow for an event to be paused by an event in addition to being manually
        # paused without one undoing the other.
        self.paused = False
        self.event_paused = False

    def per_tick(self, st_diff: float) -> None:
        """
        This function is called every single game tick, incrementing the timer, and checking for code to trigger.
        Events are not called as part of this loop. Instead, calling events is left up to the game map class, to ensure
        that timed events do not trigger during other events.
        :param st_diff: Amount of time that has passed in seconds since the last call.
        """
        if not (self.paused or self.event_paused):
            self.raw_time += st_diff
            self.time += st_diff

            self.trigger_timed_codes()

    def increment(self, seconds: float) -> None:
        """
        Increments the timer by the given amount of seconds. Designed to be called by in-game events that simulate
        large amount of times passing at once.
        :param seconds: The amount of time (in seconds) to increment the timer by.
        """
        self.time += seconds

    def pause(self, event_pause=False) -> None:
        """
        Pauses the timer. Designed to be used by both automated events, and be called by in-game events that want the
        timers to pause. The argument event_pause is used to differentiate between the two scenarios. The timer
        will only run if both event_paused and paused are False.
        :param event_pause: Used to differentiate between automated pauses by the pink engine (True), and explicit
        calls made in pink engine events (False).
        """
        if event_pause:
            self.event_paused = True
        else:
            self.paused = True

    def unpause(self, event_pause=False) -> None:
        """
        Undoes the effect of the pause function
        :param event_pause: Used to differentiate between automated pauses by the pink engine (True), and explicit
        calls made in pink engine events (False).
        """
        if event_pause:
            self.event_paused = False
        else:
            self.paused = True

    def trigger_timed_codes(self) -> None:
        """
        Checks if there is any code whose time to trigger has passed, and then runs that code.
        """
        if self.next_code_trigger is not None and self.time >= self.next_code_trigger:
            triggered_keys = [x for x in self._timed_code_dict.keys() if x <= self.next_code_trigger]

            for triggered_key in triggered_keys:
                triggered_codes = self._timed_code_dict.pop(triggered_key)

                for triggered_code in triggered_codes:
                    # If this timed code has an ID, removes the ID from the memory
                    if triggered_code.code_id is not None:
                        self._code_ids.pop(triggered_code.code_id)

                    # Executes timed codes
                    triggered_code.execute()

            if len(self._timed_code_dict) == 0:
                # If no timed code remains, sets the next_code_trigger to None
                self.next_code_trigger = None
            else:
                # Sets the next timed code trigger to the earliest following event.
                self.next_code_trigger = sorted(self._timed_code_dict.keys())[0]

    def add_timed_code(self, time: float, code: str, code_id: Optional[str] = None) -> None:
        """
        Adds a timed code execution to this timer.
        :param time: The amount of time (in seconds) the timer clock needs to reach to trigger this code
        :param code: The code to trigger
        :param code_id: The ID for this code. Giving a timer an ID is necessary if you want the option of canceling it
        later, or showing how much time remains.
        """
        if time < self.time:
            return

        if self.next_code_trigger is None or time < self.next_code_trigger:
            self.next_code_trigger = time

        if time not in self._timed_code_dict:
            self._timed_code_dict[time] = []
        new_timed_code = GameTimerTimedCode(time=time, code=code, code_id=code_id)
        self._timed_code_dict[time].append(new_timed_code)

        if code_id is not None:
            # If the code ID already exists, removes the ID from the old code:
            if code_id in self._code_ids:
                self._code_ids[code_id].code_id = None

            # Adds the code id to the code id index
            self._code_ids[code_id] = new_timed_code

    def check_timed_event(self) -> Tuple[str, tuple, dict]:
        """
        Checks if there is any event whose time to trigger has passed, and then returns the event name, as well as
        appropriate args and kwargs.
        """
        if self.next_event_trigger is not None and self.time >= self.next_event_trigger:
            triggered_keys = [x for x in self._timed_event_dict.keys() if x <= self.next_event_trigger]

            for triggered_key in triggered_keys:
                while len(self._timed_event_dict[triggered_key]) > 0:
                    triggered_event = self._timed_event_dict[triggered_key].pop(0)

                    # If there's no more events for the timestamp, removes the timestamp from the dict.
                    if len(self._timed_event_dict[triggered_key]) == 0:
                        self._timed_event_dict.pop(triggered_key)

                    # Determines the next event trigger
                    if len(self._timed_event_dict) == 0:
                        self.next_event_trigger = None
                    else:
                        self.next_event_trigger = sorted(self._timed_event_dict.keys())[0]

                    # If triggered event has an ID, removes it from the ID dict
                    if triggered_event.event_id is not None:
                        self._event_ids.pop(triggered_event.event_id)

                    return triggered_event.event, triggered_event.event_args, triggered_event.event_kwargs

    def add_timed_event(self, time: float, event: str, event_id: Optional[str] = None, *args, **kwargs) -> None:
        """
        Adds a timed event execution to this timer.
        :param time: The amount of time (in seconds) the timer clock needs to reach to trigger this event.
        :param event: The label of the event to trigger to trigger
        :param args: The args to pass along to the label.
        :param kwargs: The kwargs to pass along to the label.
        :param event_id: The ID for this event. Giving a timer an ID is necessary if you want the option of canceling it
        later, or showing how much time remains.
        """
        if time < self.time:
            return

        if self.next_event_trigger is None or time < self.next_event_trigger:
            self.next_event_trigger = time

        if time not in self._timed_event_dict:
            self._timed_event_dict[time] = []
        new_timed_event = GameTimerTimedEvent(
            time=time, event=event, event_args=args, event_kwargs=kwargs, event_id=event_id)
        self._timed_event_dict[time].append(new_timed_event)

        if event_id is not None:
            # If the code ID already exists, removes the ID from the old code:
            if event_id in self._event_ids:
                self._event_ids[event_id].event_id = None

            # Adds the code id to the code id index
            self._event_ids[event_id] = new_timed_event

    def remove_timed_code(self, code_id: str) -> None:
        """
        Removes a timed code execution from this timer. No error will be raised if the code is no longer scheduled by
        the time this function is called.
        :param code_id: The ID for the timed code execution to remove. Timed code executions without a code ID cannot
        be removed.
        """
        if code_id in self._code_ids:
            code_to_remove = self._code_ids[code_id]

            self._timed_code_dict[code_to_remove.time].remove(code_to_remove)
            if len(self._timed_code_dict[code_to_remove.time]) == 0:
                self._timed_code_dict.pop(code_to_remove.time)
            self._code_ids.pop(code_id)

    def remove_timed_event(self, event_id: str) -> None:
        """
        Removes a timed event call from this timer. No error will be raised if the event is no longer scheduled by
        the time this function is called.
        :param event_id: The ID for the timed event call to remove. Timed event calls without a event ID cannot
        be removed.
        """
        if event_id in self._event_ids:
            event_to_remove = self._event_ids[event_id]
            self._timed_event_dict[event_to_remove.time].remove(event_to_remove)
            if len(self._timed_event_dict[event_to_remove.time]) == 0:
                self._timed_event_dict.pop(event_to_remove.time)

            self._event_ids.pop(event_id)

    def remaining_time(self, code_id: str) -> float:
        """
        Returns the amount of time remaining (in seconds) for the timed code execution or event call with the given ID.
        :param code_id: The given ID.
        """
        if code_id in self._code_ids:
            return self._code_ids[code_id].time - self.time
        elif code_id in self._event_ids:
            return self._event_ids[code_id].time - self.time
        else:
            return 0.0

    def exists(self, code_id: str) -> bool:
        """
        Returns True if the given ID is being used for code or an event.
        :param code_id: The given ID.
        """
        return code_id in self._code_ids or code_id in self._event_ids


class ScreenShaker:
    def __init__(
            self,
            x_amp: float,
            y_amp: float,
            frequency: float,
            phase: float,
            duration: float,
            manager: 'OverlayManager'
    ):
        """
        The Screen shaker class controls the shaking of the pink engine map screen. This functions wholly independently
        from ren'py shake transition, as the pink engine doesn't 'transition', making that effect somewhat unreliable.
        A single screenshaker takes the form of a sine function describing the movement, though with separate
        simultaneous amplitudes for the x and y coord.
        Multiple screen shakers with different settings can be active at one to create a more irregular shake.
        :param x_amp: The amplitude of the x axis in pixels.
        :param y_amp: The amplitude of the y axis in pixels.
        :param frequency: The frequency in shakes per seconds
        :param phase: The starting phase of the shake, in radians.
        :param duration: How long the shake should last, in seconds.
        :param manager: The OverlayManager object managing this shaker.
        """
        self.x_amp = x_amp
        self.y_amp = y_amp
        self.frequency = frequency
        self.phase = phase
        self.manager = manager
        self.start_st = self.last_st
        self.stop_st = self.start_st + duration

    def rebase_st(self, gt) -> None:
        """
        To be called after gt has been reset for whatever reason, causing this object to rebase its current attributes
        off the given new gt.
        :param float gt: The new game time in seconds
        """
        diff = self.last_st - gt
        self.start_st -= diff
        self.stop_st -= diff

    def increment_gt(self, gt_diff: float) -> None:
        """
        To be called when the engine skips over a period of time, incrementing the internal time counters by
        the appropriate amount.
        :param gt_diff: The amount of seconds by which to increment the timers.
        """
        self.start_st += gt_diff
        self.stop_st += gt_diff

    def get_current_offsets(self, st) -> Tuple[float, float, bool]:
        """
        Called every frame, this function returns the amount of pixels to offset the screen by for the sine function
        of this screen shaker. It also returns a boolean that indicates whether this shaker's duration has finished and
        it should no longer be checked from now on.
        :return: x_offset, y_offset, whether to destroy this shaker.
        """
        if st > self.stop_st:
            return 0, 0, True

        func_time = st - self.start_st
        x_offset = self.x_amp * sin(2 * pi * self.frequency * func_time + self.phase)
        y_offset = self.y_amp * sin(2 * pi * self.frequency * func_time + self.phase)
        return x_offset, y_offset, False

    @property
    def last_st(self) -> float:
        """
        The last st on which this screen shaker was updated.
        """
        return self.manager.last_st


class Overlay(renpy.exports.Displayable):
    def __init__(
            self,
            fade_time: float,
            alpha: float,
            consistent: bool,
            start_dimensions: Dimensions,
            target_dimensions: Optional[Dimensions],
            move_time: float,
            manager: 'OverlayManager',
            x_arc: int,
            y_arc: int
    ):
        """
        This is the parent class of all Overlay classes, providing the common functionalities. It is not functional
        on its own, and no object of this class should be instantiated.
        :param fade_time: The amount of time in seconds the overlay takes to fade to its target alpha. If 0.0, no
        fade takes place, but the overlay instantly transitions.
        :param alpha: The alpha value the overlay should have at the end of its fade. 0.0 for completely transparent,
        1.0 for 100% visible.
        :param consistent: Whether or not the overlay lasts between maps.
        :param start_dimensions: A four-integer tuple (x, y, width, height) that indicate the dimensions the overlay
        should have when initially created.
        :param target_dimensions: A four-integer tuple (x, y, width, height) that indicate the dimensions the overlay
        should have at the end of its move. Set to None if the overlay should not move on its creation.
        :param move_time: The amount of time in seconds it should take to transition between the start_dimensions and
        target_dimensions.
        :param manager: The OverlayManager managing this object.
        :param x_arc: If set to a value other than 0, adds horizontal arcing to the movement from start_dimensions to
        target_dimensions. The arcing is parabolic, with the greatest extent being the value of x_arc.
        :param y_arc: If set to a value other than 0, adds vertical arcing to the movement from start_dimensions to
        target_dimensions. The arcing is parabolic, with the greatest extent being the value of y_arc.
        """
        self.fade_time = fade_time
        self.move_time = move_time

        if fade_time == 0.0:
            self.alpha = alpha
        else:
            self.alpha = 0.0
        self.start_alpha = self.alpha
        self.target_alpha = alpha

        self.dimensions = start_dimensions
        self.start_dimensions = start_dimensions
        self.target_dimensions = target_dimensions if target_dimensions is not None else start_dimensions
        self.x_arc = x_arc
        self.y_arc = y_arc

        self.manager = manager
        self._start_fade_st = self.last_st
        self._target_fade_st = self.last_st + fade_time
        self._start_move_st = self.last_st
        self._target_move_st = self.last_st + move_time

        self.consistent = consistent

        renpy.exports.Displayable.__init__(self)  # Py2

    def tick_update(self, st: float) -> None:
        """
        Called every frame, updating the overlay's alpha and dimensions.
        :param st: The current show time, in seconds.
        """
        # Updates the alpha
        if self.alpha != self.target_alpha:
            if st >= self._target_fade_st or self._target_fade_st == self._start_fade_st:
                self.alpha = self.target_alpha
                self.start_alpha = self.target_alpha
            else:
                proportion = (st - self._start_fade_st) / (self._target_fade_st - self._start_fade_st)
                self.alpha = self.start_alpha + (self.target_alpha - self.start_alpha) * proportion

        # Updates the dimensions
        if self.dimensions != self.target_dimensions:
            if st >= self._target_move_st or self._target_move_st == self._start_move_st:
                self.dimensions = self.target_dimensions
                self.start_dimensions = self.target_dimensions
            else:
                new_dimensions = []
                proportion = (st - self._start_move_st) / (self._target_move_st - self._start_move_st)

                x_arc_neg = True if self.x_arc < 0 else False
                y_arc_neg = True if self.y_arc < 0 else False

                x_arc = (- pow((2 * sqrt(abs(self.x_arc)) * proportion) - sqrt(abs(self.x_arc)), 2) + abs(self.x_arc))
                y_arc = (- pow((2 * sqrt(abs(self.y_arc)) * proportion) - sqrt(abs(self.y_arc)), 2) + abs(self.y_arc))

                x_arc = x_arc * -1 if x_arc_neg else x_arc
                y_arc = y_arc * -1 if y_arc_neg else y_arc

                for c, dimension in enumerate(self.start_dimensions):
                    target_dimension = self.target_dimensions[c]
                    if dimension == target_dimension:
                        if c == 0:
                            dimension += x_arc
                        elif c == 1:
                            dimension += y_arc
                        new_dimensions.append(dimension)
                    else:
                        updated_dimension = dimension + (target_dimension - dimension) * proportion
                        if c == 0:
                            updated_dimension += x_arc
                        elif c == 1:
                            updated_dimension += y_arc
                        new_dimensions.append(updated_dimension)
                self.dimensions = tuple(new_dimensions)

    def should_redraw(self) -> bool:
        """
        Whether or not the Overlay should be redrawn next frame. Returns True if the current alpha or dimensions
        do not match the target alpha or dimensions.
        """
        return self.target_alpha != self.alpha or self.target_dimensions != self.dimensions

    def get_render_dimensions(self) -> Tuple[int, int]:
        """
        Returns the size of this overlay's render.
        """
        return int(self.width), int(self.height)

    def render(self, width: int, height: int, st: float, at: float) -> renpy.exports.Render:  # noqa
        """
        :param width: The width of the object this overlay is drawn into (Note: Not the width this overlay should
        by drawn at)
        :param height:  The height of the object this overlay is drawn into (Note: Not the height this overlay
        should by drawn at)
        :param st: The shown time (in seconds).
        :param at: The animation time (in seconds).
        """
        # Updates the alpha
        if not self.paused:
            self.tick_update(st)

        # Creates the render
        width, height = self.get_render_dimensions()
        if self.alpha == 0.0:
            # Fully translucent, returns an empty render
            t = renpy.display.transform.Transform()
            child_render = renpy.exports.render(t, width, height, st, at)
        else:
            child = self.child
            t = renpy.display.transform.Transform(
                child, alpha=self.alpha, xysize=(width, height))
            child_render = renpy.exports.render(t, width, height, st, at)

        if self.should_redraw():
            renpy.exports.redraw(self, 0)
        return child_render

    def set_alpha(self, alpha: float, fade_time: float = 0.0) -> None:
        """
        Starts an alpha fade to the given alpha
        :param alpha: The target alpha of the fade.
        :param fade_time: The amount of time the fade should take. If 0.0 (the default), no fade takes place, and the
        alpha is transitioned instantly.
        """
        if fade_time == 0.0:
            self.alpha = alpha
            self.target_alpha = alpha
            self.start_alpha = alpha
        else:
            self.target_alpha = alpha
            self.start_alpha = self.alpha

        self._start_fade_st = self.last_st
        self._target_fade_st = self.last_st + fade_time
        # Necessary for reloading, otherwise it can double-trigger if saved on a
        # line which includes set_alpha.
        renpy.exports.restart_interaction()
        renpy.exports.redraw(self, 0)

    def set_dimensions(
            self,
            x: Optional[int] = None,
            y: Optional[int] = None,
            width: Optional[int] = None,
            height: Optional[int] = None,
            move_time: float = 0.0,
            x_arc: int = 0,
            y_arc: int = 0
    ) -> None:
        """
        Starts a movement to give this overlay the given dimensions. Dimensions that are not given are copied from
        the current dimensions.
        :param x: The x the overlay should have at the end of the move.
        :param y: The y the overlay should have at the end of the move.
        :param width: The width the overlay should have at the end of the move.
        :param height: The height the overlay should have at the end of the move.
        :param move_time: The time in seconds the move should take.
        :param x_arc: If set to a value other than 0, adds horizontal arcing to the movement. The arcing is parabolic,
        with the greatest extent being the value of x_arc.
        :param y_arc: If set to a value other than 0, adds vertical arcing to the movement. The arcing is parabolic,
        with the greatest extent being the value of y_arc.
        """
        x = self.x if x is None else x
        y = self.y if y is None else y
        width = self.width if width is None else width
        height = self.height if height is None else height

        if move_time == 0.0:
            self.dimensions = (x, y, width, height)
            self.target_dimensions = (x, y, width, height)
            self.start_dimensions = (x, y, width, height)
        else:
            self.target_dimensions = (x, y, width, height)
            self.start_dimensions = (self.x, self.y, self.width, self.height)

        self._start_move_st = self.last_st
        self._target_move_st = self.last_st + move_time
        self.x_arc = x_arc
        self.y_arc = y_arc
        # Necessary for reloading, otherwise it can double-trigger if saved on a
        # line which includes set_dimensions.
        renpy.exports.restart_interaction()
        renpy.exports.redraw(self, 0)

    def rebase_st(self, gt: float) -> None:
        """
        To be called after gt has been reset for whatever reason, causing this object to rebase its current attributes
        off the given new gt.
        :param gt: The new game time in seconds
        """
        diff = self.last_st - gt
        self._start_fade_st -= diff
        self._target_fade_st -= diff
        self._start_move_st -= diff
        self._target_move_st -= diff

    def increment_gt(self, gt_diff: float) -> None:
        """
        To be called when the engine skips over a period of time, incrementing the internal time counters by
        the appropriate amount.
        :param gt_diff: The amount of seconds by which to increment the timers.
        """
        self._start_fade_st += gt_diff
        self._target_fade_st += gt_diff
        self._start_move_st += gt_diff
        self._target_move_st += gt_diff

    @property
    def x(self) -> int:
        """
        The current x.
        """
        return self.dimensions[0]

    @property
    def y(self) -> int:
        """
        The current y.
        """
        return self.dimensions[1]

    @property
    def width(self) -> int:
        """
        The current width.
        """
        return self.dimensions[2]

    @property
    def height(self) -> int:
        """
        The current height.
        """
        return self.dimensions[3]

    @property
    def target_x(self) -> int:
        """
        The target x.
        """
        return self.target_dimensions[0]

    @property
    def target_y(self) -> int:
        """
        The target y.
        """
        return self.target_dimensions[1]

    @property
    def target_width(self) -> int:
        """
        The target width.
        """
        return self.target_dimensions[2]

    @property
    def target_height(self) -> int:
        """
        The target height.
        """
        return self.target_dimensions[3]

    @property
    def last_st(self) -> float:
        """
        The last st on which this overlay was updated.
        """
        return self.manager.last_st

    @property
    def paused(self) -> bool:
        """
        Whether this overlay is currently paused.
        """
        return self.manager.paused


class OverlayImage(Overlay):
    def __init__(
            self,
            image_name: str,
            fade_time: float,
            alpha: float,
            consistent: bool,
            start_dimensions: Dimensions,
            target_dimensions: Optional[Dimensions],
            move_time: float,
            manager: 'OverlayManager',
            x_arc: int,
            y_arc: int
    ):
        """
        This is an overlay that overlays an image.
        :param image_name: the filepath for the image to be shown.
        :param fade_time: The amount of time in seconds the overlay takes to fade to its target alpha. If 0.0, no
        fade takes place, but the overlay instantly transitions.
        :param alpha: The alpha value the overlay should have at the end of its fade. 0.0 for completely transparent,
        1.0 for 100% visible.
        :param consistent: Whether or not the overlay lasts between maps.
        :param start_dimensions: A four-integer tuple (x, y, width, height) that indicate the dimensions the overlay
        should have when initially created.
        :param target_dimensions: A four-integer tuple (x, y, width, height) that indicate the dimensions the overlay
        should have at the end of its move. Set to None if the overlay should not move on its creation.
        :param move_time: The amount of time in seconds it should take to transition between the start_dimensions and
        target_dimensions.
        :param manager: The OverlayManager managing this object.
        :param x_arc: If set to a value other than 0, adds horizontal arcing to the movement from start_dimensions to
        target_dimensions. The arcing is parabolic, with the greatest extent being the value of x_arc.
        :param y_arc: If set to a value other than 0, adds vertical arcing to the movement from start_dimensions to
        target_dimensions. The arcing is parabolic, with the greatest extent being the value of y_arc.
        """
        Overlay.__init__(
            self, fade_time, alpha, consistent, start_dimensions, target_dimensions, move_time, manager, x_arc, y_arc)
        self.child = filepath_to_reg_image(image_name)

    def set_image(self, image_name: str) -> None:
        """
        Changes the image shown by this overlay.
        """
        self.child = filepath_to_reg_image(image_name)
        renpy.exports.redraw(self, 0)


class OverlayText(Overlay):
    def __init__(
            self,
            text: str,
            fade_time: float,
            alpha: float,
            consistent: bool,
            start_dimensions: Dimensions,
            target_dimensions: Optional[Dimensions],
            move_time: float,
            manager: 'OverlayManager',
            autosize: bool,
            x_arc: int,
            y_arc: int
    ):
        """
        This is an overlay that overlays text.
        :param text: The text to show in this overlay. Can include ren'py formatting.
        :param fade_time: The amount of time in seconds the overlay takes to fade to its target alpha. If 0.0, no
        fade takes place, but the overlay instantly transitions.
        :param alpha: The alpha value the overlay should have at the end of its fade. 0.0 for completely transparent,
        1.0 for 100% visible.
        :param consistent: Whether or not the overlay lasts between maps.
        :param start_dimensions: A four-integer tuple (x, y, width, height) that indicate the dimensions the overlay
        should have when initially created.
        :param target_dimensions: A four-integer tuple (x, y, width, height) that indicate the dimensions the overlay
        should have at the end of its move. Set to None if the overlay should not move on its creation.
        :param move_time: The amount of time in seconds it should take to transition between the start_dimensions and
        target_dimensions.
        :param manager: The OverlayManager managing this object.
        :param autosize: Whether to autosize this overlay. If True, automatically sets the width and height of this
        overlay to be that of the underlying text at 1.0 zoom, preventing any stretching.
        :param x_arc: If set to a value other than 0, adds horizontal arcing to the movement from start_dimensions to
        target_dimensions. The arcing is parabolic, with the greatest extent being the value of x_arc.
        :param y_arc: If set to a value other than 0, adds vertical arcing to the movement from start_dimensions to
        target_dimensions. The arcing is parabolic, with the greatest extent being the value of y_arc.
        """
        Overlay.__init__(
            self, fade_time, alpha, consistent, start_dimensions, target_dimensions, move_time, manager, x_arc, y_arc)
        self.text = text
        self._autosize = autosize

    def get_render_dimensions(self) -> Tuple[int, int]:
        """
        Returns the size of this overlay's render.
        """
        if not self.autosize:
            return int(self.width), int(self.height)
        else:
            width_float, height_float = self.child.size()
            return int(width_float), int(height_float)

    def set_text(self, text: str) -> None:
        """
        Changes the text shown by this overlay.
        """
        self.text = text
        renpy.exports.redraw(self, 0)

    def should_redraw(self) -> bool:
        """
        Whether or not the Overlay should be redrawn next frame. Always returns True for a text overlay, since the text
        might include variables.
        """
        return True

    @property
    def child(self):
        # Whenever the child is called for this function, it is freshly generated. This ensures that any ren'py
        # variables present in the text are updated.
        return renpy.text.text.Text(self.text)

    @property
    def autosize(self) -> bool:
        # Turned into a property to allow a setter to be used
        return self._autosize

    @autosize.setter
    def autosize(self, value: bool) -> None:
        # Turned into a setter so that redraw can be triggered on changing the value.
        self._autosize = value
        renpy.exports.redraw(self, 0)


class OverlaySolid(Overlay):
    def __init__(
            self,
            color: str,
            fade_time: float,
            alpha: float,
            consistent: bool,
            start_dimensions: Dimensions,
            target_dimensions: Optional[Dimensions],
            move_time: float,
            manager: 'OverlayManager',
            x_arc: int,
            y_arc: int
    ):
        """
        This is an overlay that overlays a solid color.
        :param color: the color (has the format '#rrggbb').
        :param fade_time: The amount of time in seconds the overlay takes to fade to its target alpha and color. If 0.0,
        no fade takes place, but the overlay instantly transitions.
        :param alpha: The alpha value the overlay should have at the end of its fade. 0.0 for completely transparent,
        1.0 for 100% visible.
        :param consistent: Whether or not the overlay lasts between maps.
        :param start_dimensions: A four-integer tuple (x, y, width, height) that indicate the dimensions the overlay
        should have when initially created.
        :param target_dimensions: A four-integer tuple (x, y, width, height) that indicate the dimensions the overlay
        should have at the end of its move. Set to None if the overlay should not move on its creation.
        :param move_time: The amount of time in seconds it should take to transition between the start_dimensions and
        target_dimensions.
        :param manager: The OverlayManager managing this object.
        :param x_arc: If set to a value other than 0, adds horizontal arcing to the movement from start_dimensions to
        target_dimensions. The arcing is parabolic, with the greatest extent being the value of x_arc.
        :param y_arc: If set to a value other than 0, adds vertical arcing to the movement from start_dimensions to
        target_dimensions. The arcing is parabolic, with the greatest extent being the value of y_arc.
        """
        Overlay.__init__(
            self, fade_time, alpha, consistent, start_dimensions, target_dimensions, move_time, manager, x_arc, y_arc)
        self.child = renpy.display.image.Solid(color)

        self._current_color = color
        self._target_color = color
        self._start_color = color

    def tick_update(self, st: float) -> None:
        """
        Called every frame, updating the overlay's color, alpha and dimensions.
        :param st: The current show time, in seconds.
        """
        # Updates the color
        if self._current_color != self._target_color:
            if st >= self._target_fade_st or self._target_fade_st == self._start_fade_st:
                self._current_color = self._target_color
                self._start_color = self._target_color
            else:
                proportion = (st - self._start_fade_st) / (self._target_fade_st - self._start_fade_st)

                start_red, start_green, start_blue = \
                    int(self._start_color[1:3], 16), int(self._start_color[3:5], 16), \
                    int(self._start_color[5:7], 16)
                target_red, target_green, target_blue = \
                    int(self._target_color[1:3], 16), int(self._target_color[3:5], 16), \
                    int(self._target_color[5:7], 16)

                # Changed red
                inter_red = int(start_red + (target_red - start_red) * proportion)
                inter_green = int(start_green + (target_green - start_green) * proportion)
                inter_blue = int(start_blue + (target_blue - start_blue) * proportion)

                inter_red_str = str(hex(inter_red))[2:4] if len(str(hex(inter_red))) == 4 \
                    else "0" + str(hex(inter_red))[2:3]
                inter_green_str = str(hex(inter_green))[2:4] if len(str(hex(inter_green))) == 4 \
                    else "0" + str(hex(inter_green))[2:3]
                inter_blue_str = str(hex(inter_blue))[2:4] if len(str(hex(inter_blue))) == 4 \
                    else "0" + str(hex(inter_blue))[2:3]

                self._current_color = "#" + inter_red_str + inter_green_str + inter_blue_str

            self.child = renpy.display.image.Solid(self._current_color)

        # Updates the alpha and dimensions
        Overlay.tick_update(self, st)

    def should_redraw(self) -> bool:
        """
        Whether or not the Overlay should be redrawn next frame. Returns True if the current alpha, dimensions, color
        do not match the target alpha, dimensions or color.
        """
        return \
            self.target_alpha != self.alpha or \
            self._target_color != self._current_color or \
            self.target_dimensions != self.dimensions

    def set_color(self, color: str, fade_time: float = 0.0) -> None:
        """
        Starts an fade to the given color
        :param color: The target color (has the format '#rrggbb').
        :param fade_time: The amount of time the fade should take. If 0.0 (the default), no fade takes place, and the
        color is transitioned instantly.
        """
        if not color[0] == '#':
            raise RuntimeError(
                f"Trying to set color {color}. Color must be a hexadecimal sequence starting with the `#` symbol.")

        if fade_time == 0.0:
            self._current_color = color
            self._target_color = color
            self._start_color = color
        else:
            self._target_color = color
            self._start_color = self._current_color

        self._start_fade_st = self.last_st
        self._target_fade_st = self.last_st + fade_time

        # Necessary for reloading, otherwise it can double-trigger if saved on a
        # line which includes set_alpha.
        renpy.exports.restart_interaction()
        renpy.exports.redraw(self, 0)


class OverlayManager(renpy.exports.Displayable):
    def __init__(self):
        """
        The Class that manages the triggering of Overlays and ScreenShakers.
        """
        renpy.exports.Displayable.__init__(self)  # Py2

        self.last_st = 0.0
        self.active_overlays: Dict[int, Overlay] = {}
        self.active_shakers: Dict[int, ScreenShaker] = {}

        self.shake_x = 0.0
        self.shake_y = 0.0
        self.paused = False

    def render(self, width: int, height: int, st: float, at: float) -> renpy.exports.Render:  # noqa
        """
        Renders all overlays and turns them into a single image. Also calls all the screen shakers.
        :param int width: The width of the screen the manager is drawn into.
        :param int height: The height of the screen the manager is drawn into.
        :param float st: The shown time (in seconds).
        :param float at: The animation time (in seconds).
        """
        if not self.paused:
            if st < self.last_st:
                self.rebase_st(st)

            self.last_st = st
        renpy.exports.redraw(self, 0)

        # initiate render object
        render = renpy.exports.Render(width, height)

        # Overlays have their pause logic incorporated.
        for overlay in self.active_overlays.values():
            render.place(overlay, overlay.x, overlay.y)

        if not self.paused:
            total_offset_x = 0.0
            total_offset_y = 0.0

            new_active_shakers = {}
            for screen_shaker in self.active_shakers.values():
                shake_x, shake_y, destroy = screen_shaker.get_current_offsets(st)
                total_offset_x += shake_x
                total_offset_y += shake_y

                if not destroy:
                    new_active_shakers[id(screen_shaker)] = screen_shaker
            self.active_shakers = new_active_shakers
            self.shake_x = total_offset_x
            self.shake_y = total_offset_y

        return render

    def rebase_st(self, gt: float) -> None:
        """
        To be called after gt has been reset for whatever reason, causing this object to rebase its current attributes
        off the given new gt.
        :param gt: The new game time in seconds
        """
        for overlay in self.active_overlays.values():
            overlay.rebase_st(gt)
        for shaker in self.active_shakers.values():
            shaker.rebase_st(gt)
        self.last_st = gt

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
        start_dimensions = (x, y, width, height)
        if target_x is None and target_y is None and target_width is None and target_height is None:
            target_dimensions = None
        else:
            target_dimensions = (
                target_x if target_x is not None else x,
                target_y if target_y is not None else y,
                target_width if target_width is not None else width,
                target_height if target_height is not None else height)

        new_overlay = OverlayImage(
            image_name=image_name, fade_time=fade_time, alpha=alpha, consistent=consistent,
            start_dimensions=start_dimensions, target_dimensions=target_dimensions, move_time=move_time,
            manager=self, x_arc=x_arc, y_arc=y_arc)
        self.active_overlays[id(new_overlay)] = new_overlay

        return new_overlay

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
        start_dimensions = (x, y, width, height)
        if target_x is None and target_y is None and target_width is None and target_height is None:
            target_dimensions = None
        else:
            target_dimensions = (
                target_x if target_x is not None else x,
                target_y if target_y is not None else y,
                target_width if target_width is not None else width,
                target_height if target_height is not None else height)

        new_overlay = OverlayText(
            text=text, fade_time=fade_time, alpha=alpha, consistent=consistent,
            start_dimensions=start_dimensions, target_dimensions=target_dimensions, move_time=move_time,
            manager=self, autosize=autosize, x_arc=x_arc, y_arc=y_arc)
        self.active_overlays[id(new_overlay)] = new_overlay

        return new_overlay

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
        start_dimensions = (x, y, width, height)
        if target_x is None and target_y is None and target_width is None and target_height is None:
            target_dimensions = None
        else:
            target_dimensions = (
                target_x if target_x is not None else x,
                target_y if target_y is not None else y,
                target_width if target_width is not None else width,
                target_height if target_height is not None else height)

        new_overlay = OverlaySolid(
            color=color, fade_time=fade_time, alpha=alpha, consistent=consistent,
            start_dimensions=start_dimensions, target_dimensions=target_dimensions, move_time=move_time,
            manager=self, x_arc=x_arc, y_arc=y_arc)
        self.active_overlays[id(new_overlay)] = new_overlay

        return new_overlay

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
        new_shaker = ScreenShaker(
            duration=duration, frequency=frequency, x_amp=x_amp, y_amp=y_amp, phase=phase, manager=self)
        self.active_shakers[id(new_shaker)] = new_shaker

    @staticmethod
    def remove_overlay(overlay: Overlay, fade_time: float = 0.0) -> None:
        """
        Removes the target overlay. Note that it technically doesn't remove, it just makes invisible.
        :param overlay: the overlay to make invisible.
        :param fade_time: The amount of time the removal should take, with the overlay fading away. If 0.0 (the
        default), no fade takes place, and the overlay is removed instantly.
        """
        overlay.set_alpha(0.0, fade_time=fade_time)

    def remove_all_overlays(self, fade_time: float = 0.0) -> None:
        """
        Removes all overlays. Note that it technically doesn't remove, it just makes invisible.
        :param fade_time: The amount of time the removal should take, with the overlays fading away. If 0.0 (the
        default), no fade takes place, and the overlays are removed instantly.
        """
        for overlay in self.active_overlays.values():
            overlay.set_alpha(0.0, fade_time=fade_time)

    def get_consistent_overlays(self) -> List[Overlay]:
        """
        Retrieves a list of consistent overlays.
        """
        return [x for x in self.active_overlays.values() if x.consistent]

    def add_consistent_overlays(self, consistent_overlays: List[Overlay]) -> None:
        """
        Adds the list of consistent overlays to this manager. This function is automatically called when a new map
        is initiated, and should not be called by a pink engine designer.
        :param consistent_overlays: The list of overlays to add.
        """
        for consistent_overlay in consistent_overlays:
            consistent_overlay.manager = self
            self.active_overlays[id(consistent_overlay)] = consistent_overlay

    def pause(self) -> None:
        """
        Pauses all overlays and shakers.
        """
        self.paused = True

    def unpause(self) -> None:
        """
        Unpauses all overlays and shakers.
        """
        self.paused = False

    def increment_all_gt(self, gt_diff: float) -> None:
        """
        Increments the gts on all overlays and shakers.
        """
        for overlay in self.active_overlays.values():
            overlay.increment_gt(gt_diff)
        for shaker in self.active_shakers.values():
            shaker.increment_gt(gt_diff)

    def visit(self) -> List[renpy.exports.Displayable]:
        """
        Returns the list of all overlays. Note that this does not return ScreenShakers, as those do not affect the
        manager's renders.
        """
        return list(self.active_overlays.values())

    def stop_shaking(self) -> None:
        """
        Instantly stops and deletes all ScreenShakers.
        """
        self.active_shakers = {}
        self.shake_x = 0.0
        self.shake_y = 0.0

    @property
    def is_shaking(self) -> bool:
        """
        Returns True if there are any Screen Shakers still in existence.
        """
        return len(self.active_shakers) > 0


class TiledMap(renpy.exports.Displayable):
    def __init__(self, game_object, **kwargs):
        """
        The displayable object that represents a single pink engine map.
        :param TiledMapGame game_object: The game that this object displays.
        """
        renpy.exports.Displayable.__init__(self, **kwargs)  # Py2

        # The associated gameplay object. Should set a number of variables.
        self.game_object = game_object

        # The grid of all displayable objects.
        self.render_grid = []
        self.render_grid_x_size = ceil(self.game_object.image_size.x / self.game_object.tile_size.x)
        self.render_grid_y_size = ceil(self.game_object.image_size.y / self.game_object.tile_size.y)
        for x in range(self.render_grid_x_size):
            self.render_grid.append([])
            for y in range(self.render_grid_y_size):
                self.render_grid[x].append({})

        # All elements on the map have their own unique id. This allows us to make sure each renders only once,
        # as well as letting us find and delete them with relative ease.
        self.next_id = 0
        self.map_elements = {}

        #

    def get_next_id(self):
        """
        :return: The id that should be used for the next displayable element
        :rtype: int
        """
        next_id = self.next_id
        self.next_id += 1
        return next_id

    def remove_from_grid(self, element):
        """
        Removes the given element from this object's render grid
        :param TiledMapElement element: The element to remove from the render grid
        """
        for column in element.get_columns():
            for row in element.get_rows():
                if 0 <= row < self.render_grid_y_size and 0 <= column < self.render_grid_x_size:
                    self.render_grid[column][row].pop(element.element_id)

    def add_to_grid(self, element):
        """
        Adds the given element to this object's render grid
        :param TiledMapElement element: The element to add to the render grid
        """
        for column in element.get_columns():
            for row in element.get_rows():
                if 0 <= row < self.render_grid_y_size and 0 <= column < self.render_grid_x_size:
                    self.render_grid[column][row][element.element_id] = element

    def add_element(self, x, y, layer, game_object):
        """
        Adds the given game object at the given x and y on the given layer
        :param int x: The x (in pixels) at which the given object's image is displayed
        :param int y: The y (in pixels) at which the given object's image is displayed
        :param TiledMapGameLayer layer: The layer the object exists on
        :param TiledMapGameTile|TiledMapGameObject game_object: The given game object
        :return: The displayable ID of the added object
        :rtype: int
        """
        element_id = self.get_next_id()
        new_element = TiledMapElement(self, element_id, x, y, layer, game_object)
        self.map_elements[element_id] = new_element
        self.add_to_grid(new_element)

        if game_object.single_display:
            game_object.displayable_id = element_id

        return element_id

    def remove_element(self, element_id):
        """
        Removes the element with the given ID from this displayable
        :param int element_id: The given element id
        """
        element = self.map_elements[element_id]
        self.remove_from_grid(element)
        self.map_elements.pop(element_id)

        if element.game_object.single_display:
            element.game_object.displayable_id = None

    def move_element(self, element_id, new_x, new_y):
        """
        Moves the element with the given ID to the given new x and y
        :param int element_id: The given element id
        :param int new_x: The new x (in pixels)
        :param int new_y: The new y (in pixels)
        """
        element = self.map_elements[element_id]
        self.remove_from_grid(element)
        element.x = new_x
        element.y = new_y
        element.set_priority_tuple()
        self.add_to_grid(element)

    def render(self, width, height, st, at):  # noqa
        """
        :param int width:
        :param int height:
        :param float st: The shown time (in seconds).
        :param float at: The animation time (in seconds).
        :rtype: renpy.exports.Render
        """
        renpy.exports.redraw(self, 0)

        # initiate render object
        render = renpy.exports.Render(width, height)

        if not self.game_object.check_existence():  # prevents crash on completion of game
            return render
        if renpy.store.pink_render_enabled:
            self.game_object.camera.center_on_target()
            objects_in_frame = self.get_objects_in_frame()
            objects_in_frame = self.sort_objects(objects_in_frame)

            for child in objects_in_frame:
                render.place(child, child.x, child.y)

        return render

    def get_objects_in_frame(self):
        """
        :return: a list of objects currently in frame.
        :rtype: list
        """
        camera = self.game_object.camera

        # Pixel maximums covered by the screen, plus a bit of margin to accommodate high framerates.
        min_x = camera.x.value - 10
        max_x = camera.x.value + camera.viewport_width + 10
        min_y = camera.y.value - 10
        max_y = camera.y.value + camera.viewport_height + 10

        min_x_bound = int(min_x / (self.game_object.tile_size.x * camera.xzoom))
        max_x_bound = int(max_x / (self.game_object.tile_size.x * camera.xzoom))
        min_y_bound = int(min_y / (self.game_object.tile_size.y * camera.yzoom))
        max_y_bound = int(max_y / (self.game_object.tile_size.y * camera.yzoom))

        # Slice render_grid to get matrix of objects currently in frame.
        slices = []
        frame_matrix = self.render_grid[min_x_bound:max_x_bound + 1]
        for sliced_row in frame_matrix:
            slices.append(sliced_row[min_y_bound:max_y_bound + 1])

        # Translates matrix to dictionary, using object id to get rid of doubles.
        objects_in_frame = {}
        for sliced_row in slices:
            for sliced_tile in sliced_row:
                for object_id, map_object in sliced_tile.items():
                    objects_in_frame[object_id] = map_object

        return list(objects_in_frame.values())

    @staticmethod
    def sort_objects(objects_to_sort):
        """
        :param list objects_to_sort: The list of objects to sort
        :return: The given list of objects sorted according to their priority dictionary, so that they are in the order
        in which they should be rendered.
        :rtype: list
        """
        priority_dict = {}
        for map_object in objects_to_sort:
            priority_tuple = map_object.priority_tuple
            priority_dict[priority_tuple] = map_object

        sorted_objects = []
        for key in sorted(priority_dict):
            sorted_objects.append(priority_dict[key])

        return sorted_objects

    def visit(self):
        return list(self.map_elements.values())


class TiledMapElement(renpy.exports.Displayable):
    def __init__(self, parent_map, element_id, x, y, layer, game_object, **kwargs):
        """
        A single displayable object in the TiledMap object.
        :param TiledMapGame parent_map: The game map which this element is part of the display of
        :param element_id:
        :param x: The distance in pixels between this object's image's left side and the left border of the map
        :param y: The distance in pixels between this object's image's left side and the left border of the map
        :param layer: The layer on which this object exists
        :param game_object: The game object which this element is displaying
        """
        renpy.exports.Displayable.__init__(self, **kwargs)  # Py2

        self.parent_map = parent_map
        self.element_id = element_id
        self.x = x
        self.y = y
        self.game_object = game_object
        self.layer = layer

        if self.game_object.parent.orientation == "orthogonal" and self.layer.layer_type == 'dynamic':
            self._priority_tuple = (
                LAYER_PRIORITY[self.layer.layer_type], self.render_y, self.layer.z_order,
                self.y + self.game_object.height, self.x, -self.element_id)
        else:
            self._priority_tuple = (
                LAYER_PRIORITY[self.layer.layer_type], self.layer.z_order, self.render_y, self.x, self.element_id)

    def render(self, width, height, st, at):  # noqa
        """
        :param int width:
        :param int height:
        :param float st: The shown time (in seconds).
        :param float at: The animation time (in seconds).
        :rtype: renpy.exports.Render
        """
        child = self.game_object.image

        if child is None:
            # Object with an image of None, returns an empty render
            t = renpy.display.transform.Transform()
            child_render = renpy.exports.render(t, width, height, st, at)
        elif not self.game_object.render_dict:
            # Object with no special rendering features, just renders the image as is.
            child_render = renpy.exports.load_image(child)
        else:
            # Object with special rendering features, creates a transform for that image with the feature and then
            # renders it.
            t = renpy.display.transform.Transform(child=child, **self.game_object.render_dict)
            child_render = renpy.exports.render(t, width, height, st, at)

        if self.game_object.is_animated:
            renpy.exports.redraw(self, 0.05)
            # TODO issues when next frame time is changed. Maybe create class for keeping track?
            # renpy.exports.redraw(self, st - self.game_object.next_frame_time)
        return child_render

    def get_columns(self):
        """
        :return: The range of columns of the render grid occupied by this element
        :rtype: range
        """
        start_x_coord = int(self.x / self.parent_map.game_object.tile_size.x)
        end_x_coord = int((self.x + self.game_object.width - 1) / self.parent_map.game_object.tile_size.x)
        return range(start_x_coord, end_x_coord + 1)

    def get_rows(self):
        """
        :return: The range of rows of the render grid occupied by this element
        :rtype: range
        """
        start_y_coord = int(self.y / self.parent_map.game_object.tile_size.y)
        end_y_coord = int((self.y + self.game_object.height - 1) / self.parent_map.game_object.tile_size.y)
        return range(start_y_coord, end_y_coord + 1)

    @property
    def priority_tuple(self):
        """
        :return: This object's priority tuple (a tuple determining the order in which objects are rendered)
        :rtype: tuple
        """
        return self._priority_tuple

    @property
    def render_y(self):
        """
        :return: The y coordinate at which this object is regarded as being placed for the sake of determining its
        render order on dynamic layers
        :rtype: int
        """
        try:
            return self.game_object.occultates_as_y
        except AttributeError:
            pass
        if self.game_object.parent.orientation == "orthogonal":
            return floor((self.y + self.game_object.height - 2) / self.game_object.parent.tile_size.y)
        else:
            return self.y + self.game_object.height - 1

    def set_priority_tuple(self):
        """
        Updates this object's priority tuple
        """
        if self.game_object.parent.orientation == "orthogonal" and self.layer.layer_type == 'dynamic':
            self._priority_tuple = (
                LAYER_PRIORITY[self.layer.layer_type], self.render_y, self.layer.z_order,
                self.y + self.game_object.height, self.x, -self.element_id)
        else:
            self._priority_tuple = (
                LAYER_PRIORITY[self.layer.layer_type], self.layer.z_order, self.render_y, self.x, self.element_id)

# TODO OrthogonalTiledMapPolygon


# ======================================================================================================================
# ===========================================GAMEPLAY===================================================================
# ======================================================================================================================


# Base Images
class TiledMapGameTile(object):
    is_conditional = False
    is_animated = False
    single_display = False  # If True, Indicates that this object corresponds to only a single visual object.

    def __init__(self, parent_map, parent_tile):
        """
        A single tile on a Tiled Map (note, all instances of a tile in a game refer to the same object, whereas all
        objects on a game map have their own object)
        :param TiledMapGame parent_map: The game map that uses this tile
        :param TilesetTile parent_tile: The tile in the tileset that this tile is using the properties of.
        """
        self.parent = parent_map
        self.image = filepath_to_reg_image(parent_tile.image)
        self.parent.registered_images.add(self.image)

        self.height = parent_tile.image_height
        self.width = parent_tile.image_width
        self.properties = parent_tile.properties.copy()

    def is_on_map(self):
        """
        Returns whether or not this object is currently present on the map. For Tiles, this is always true, this
        function is included for the sake of all objects being able to pass through the same code.
        # TODO use parent class instead.
        """
        return True

    @property
    def render_dict(self):
        """
        :return: The render dictionary that should be used to render displayable elements linked to this tile
        :rtype: dict
        """
        return {}

    @property
    def sound_tag(self) -> Optional[str]:
        """
        :return: The tag for movement sound played when moving into this tile. Note that the tag should correspond
        to a key in the pink_otm_terrain_noises dictionary defined in standard_events.rpy.
        """
        return self.properties.get('sound_tag')


class TiledMapGameTileAnimated(TiledMapGameTile):
    is_animated = True

    def __init__(self, parent_map, parent_tile):
        """
        A single tile on a Tiled Map (note, all instances of a tile in a game refer to the same object, whereas all
        objects on a game map have their own object)
        :param TiledMapGame parent_map: The game map that uses this tile
        :param TilesetAnimatedTile parent_tile: The tile in the tileset that this tile is using the properties of.
        """
        TiledMapGameTile.__init__(self, parent_map, parent_tile)

        self.frames = OrderedDict()
        for animation_time, frame_id in parent_tile.frames.items():
            animation_time = float(animation_time) / 1000
            frame_image = filepath_to_reg_image(parent_tile.parent.get_tile(frame_id).image)
            self.frames[animation_time] = frame_image
            self.parent.registered_images.add(frame_image)

        self.next_frame_key = next(iter(self.frames))
        self.next_frame_time = next(iter(self.frames))
        self.image = self.frames[self.next_frame_key]
        self.latest_frame_gt = self.parent.last_gt
        self.paused = False

    def pause_animation(self):
        """
        Pauses the animation on a map freeze.
        """
        self.paused = True

    def unpause_animation(self):
        """
        Unpauses the animation on a map unfreeze
        """
        self.paused = False

    def increment_gt(self, gt_diff):
        """
        Delays the time at which the next animated frame appears by the given quantity.
        :param float gt_diff: the quantity of time by which to delay the next frame (in seconds)
        """
        self.next_frame_time += gt_diff

    def update_frame(self, gt):
        """
        Updates this object's displayed frame to the frame it should have at the given game time.
        :param float gt: Game time in seconds.
        """
        self.latest_frame_gt = gt
        if not self.paused:
            while gt > self.next_frame_time:
                prev_frame_key = self.next_frame_key

                old_frame = self.frames.pop(self.next_frame_key)
                self.frames[self.next_frame_key] = old_frame

                self.next_frame_key = next(iter(self.frames))
                if self.next_frame_key > prev_frame_key:
                    self.next_frame_time = self.next_frame_time + self.next_frame_key - prev_frame_key
                else:
                    self.next_frame_time = self.next_frame_time + self.next_frame_key

            self.image = self.frames[self.next_frame_key]

    def st_reset_frames(self, st):
        """
        Rebases this animation's next frame time based on the given st. This function was designed to
        be used after st resets when displaying a map.
        :param float st: Game time in seconds.
        """
        self.next_frame_time = self.next_frame_time - self.latest_frame_gt + st

    def post_load_frame_restoration(self):
        """
        This function is called after the game is loaded, ensuring the object's animation is not halted after
        loading.
        """
        self.next_frame_time = self.next_frame_time - self.latest_frame_gt
        self.latest_frame_gt = 0.0


class TiledMapSpriteCollectionElement(object):
    def __init__(self, element_dict, parent_sprite_collection):
        """
        This class represents a single element in a SpriteCollection. It can be either a still image, or
        an animation, depending on the number of images in the element.
        :param dict element_dict: A json-derived dictionary that describes the contents of this element.
        :param TiledMapSpriteCollection parent_sprite_collection: The sprite collection this element is a part of.
        """
        self.parent_sprite_collection = parent_sprite_collection

        self.name = element_dict["name"]
        self.images = []
        for image_path in element_dict["images"]:
            reg_path = filepath_to_reg_image(image_path)
            self.images.append(reg_path)
        self.default_speed = element_dict["default_speed"]  # type: float
        self.image_width = element_dict["image_width"]  # type: int
        self.image_height = element_dict["image_height"]  # type: int

        self.properties = {}
        for element_property in element_dict['properties']:
            self.properties[element_property['name']] = element_property['value']


class TiledMapSpriteCollection(object):  # TODO Mutual parent class for this and tile
    is_animated = True

    def __init__(self, json_file, start_time=0.0):
        """
        This class represents all images that belong to a single on-screen sprite, either a character or an object.
        These images are collected into elements, forming either still images or animations, depending on the number of
        images in the element. One element is the "current_animation", which is the element that is currently being
        displayed by the sprite.
        :param json_file: The file that contains this sprite collection's data.
        :param float start_time: the start time for this sprite collection.
        """
        sprite_collection_dict = json.load(json_file)

        # Initialize individual animations
        self.data = {}
        for element_dict in sprite_collection_dict['animations']:
            self.data[element_dict["name"]] = TiledMapSpriteCollectionElement(
                element_dict=element_dict, parent_sprite_collection=self)

        # Animation variables
        self.current_animation = None
        self.frames = OrderedDict()
        self.next_frame_time = start_time
        self.next_frame_key = 0.0
        self.current_speed = 1.0
        self._image = None
        self._changed_animation_this_frame = True

        # Pause variables
        self.paused = False
        self.latest_frame_gt = start_time

    def get_all_images(self):
        """
        :return: a list of all image names displayed by this sprite collection.
        :rtype: list
        """
        all_images = []
        for animation in self.data.values():
            for frame_image in animation.images:
                all_images.append(frame_image)
        return all_images

    def increment_gt(self, gt_diff):
        """
        Delays the time at which the next animated frame appears by the given quantity.
        :param float gt_diff: the quantity of time by which to delay the next frame (in seconds)
        """
        self.next_frame_time += gt_diff

    def pause_animation(self):
        """
        Pauses the animation on a map freeze.
        """
        self.paused = True

    def unpause_animation(self):
        """
        Unpauses the animation on a map unfreeze.
        """
        self.paused = False

    def update_frame(self, gt):
        """
        Updates this object's displayed frame to the frame it should have at the given game time.
        :param float gt: Game time in seconds.
        """
        self.latest_frame_gt = gt
        self._changed_animation_this_frame = False
        if not self.paused and self.current_animation is not None:
            while gt > self.next_frame_time:
                prev_frame_key = self.next_frame_key

                old_frame = self.frames.pop(prev_frame_key)
                self.frames[prev_frame_key] = old_frame

                self.next_frame_key = next(iter(self.frames))
                if self.next_frame_key > prev_frame_key:
                    self.next_frame_time = self.next_frame_time + self.next_frame_key - prev_frame_key
                else:
                    self.next_frame_time = self.next_frame_time + self.next_frame_key

            self._image = self.frames[self.next_frame_key]

    def st_reset_frames(self, st):
        """
        Rebases this animation's next frame time based on the given st. This function was designed to
        be used after st resets when displaying a map.
        :param float st: Game time in seconds.
        """
        if not self._changed_animation_this_frame:
            self.next_frame_time = self.next_frame_time - self.latest_frame_gt + st
            self.latest_frame_gt = st
        else:
            self.next_frame_time = st
            self.latest_frame_gt = st

    @staticmethod
    def _get_frames(animation, time_per_frame):
        """
        Returns an ordered dictionary that represents the st key/frame value combinations to play the given animation
        at the given speed from the given start time.
        :param TiledMapSpriteCollectionElement animation: The animation in question
        :param float time_per_frame: the time in seconds between frames of the animation
        :rtype: OrderedDict
        """
        frame_time = time_per_frame
        frames = OrderedDict()
        for image_path in animation.images:
            frames[frame_time] = image_path
            frame_time += time_per_frame
        return frames

    def set_animation(self, element_name, speed=None):
        """
        Changes the current_animation to the element with the given name. Can also override default speed.
        :param str element_name: The name of the element to change the current_animation to.
        :param float speed: Sets the speed for the animation. If None, the animation will play at its default speed.
        None by default.
        """
        # Do nothing if already displaying this animation
        if self.current_animation and speed == self.current_speed and element_name == self.current_animation.name:
            return

        if element_name in self.data:
            self.current_animation = self.data[element_name]
            if speed is None:
                self.current_speed = self.current_animation.default_speed
            else:
                self.current_speed = speed
            self.frames = self._get_frames(self.current_animation, self.current_speed)

            self.next_frame_time = self.latest_frame_gt + next(iter(self.frames))
            self.next_frame_key = next(iter(self.frames))
            self._changed_animation_this_frame = True  # For when an animation changes at the moment an event starts.
            self._image = self.frames[self.next_frame_key]

        else:
            self.current_animation = None
            self.frames = OrderedDict()
            self.next_frame_time = 0.0
            self.next_frame_key = 0.0
            self.current_speed = 1.0
            self._image = None

    @property
    def width(self):
        """
        :return: Width of the image, Inherited from current animation of set, 0 if not.
        :rtype: int
        """
        if self.current_animation:
            return self.current_animation.image_width
        else:
            return 0

    @property
    def height(self):
        """
        :return: Height of the image, Inherited from current animation of set, 0 if not.
        :rtype: int
        """
        if self.current_animation:
            return self.current_animation.image_height
        else:
            return 0

    @property
    def image(self):
        """
        Retrieves the renpy name for the image currently being portrayed by this collection.
        :return: The path to the image currently being portrayed by this collection.
        :rtype: str|None
        """
        if self.current_animation:
            return self._image
        else:
            return None


# Objects
class TiledMapGameObject(object):
    single_display = True

    def __init__(self, parent_rpg_tile, x, y, width, height, layer, properties):
        """
        Represents a single object on the map. Unlike tiles, objects can have individual settings, allowing them to
        move, be scaled, have conditional properties, etc.
        :param TiledMapGameTile|TiledMapSpriteCollection parent_rpg_tile: The tile or sprite collection that this
        object is displaying.
        :param int x: The distance in pixels between this object's image's left side and the left border of the map
        :param int y: The distance in pixels between this object's image's left side and the left border of the map
        :param int width: The width in pixels of this object
        :param int height: The height in pixels of this object
        :param TiledMapGameLayer layer: The layer on which this object exists
        :param dict properties: The dictionary of properties for this object
        """
        self.parent_rpg_tile = parent_rpg_tile
        self.layer = layer
        if layer is not None:
            self.parent = layer.parent
        else:
            # Rare cases where you initiate an object without a map, like creating a new OTM follower when no OTM
            #  map is visible.
            self.parent = None

        if self.should_load_consistent(properties):
            old_incarnation = getattr(renpy.store, properties['ref_name'], None)  # type: TiledMapGameObject
            self.x = old_incarnation.x
            self.y = old_incarnation.y
            self._width = old_incarnation.width
            self._height = old_incarnation.height
            self.properties = old_incarnation.properties
            self.state = old_incarnation.state

        else:
            self.x = x
            self.y = y
            self._width = width
            self._height = height
            self.state = {}

            self.properties = properties

        self.xzoom, self.yzoom = self._get_zoom()

        if 'conditional' in self.properties:
            self.is_conditional = True
        else:
            self.is_conditional = False

        if parent_rpg_tile.is_animated:
            self.is_animated = True
        else:
            self.is_animated = False

        # ID used by object in the displayable, can mutate as object is added and removed, objects that are not visible
        #  have no displayable ID.
        self.displayable_id = None

        # ID used in the map, does not change without map reloading (though objects may have different IDs on entering
        # and leaving map), objects that are not displayable still have IDs.
        self.map_id = None

        # If this object emits sound, the channel id over which it does so will be assigned to this attribute
        self.sound_channel = None

        if type(self) is TiledMapGameObject and self.ref_name is not None:
            # Type comparison ensures this only happens at the end of the final loading
            setattr(renpy.store, self.ref_name, self)

    def set_state(self, state_name, value):
        """
        Sets the given state name to the given value
        :param str state_name: the given state name
        :param value: the given value
        :rtype: None
        """
        self.state[state_name] = value

    def get_state(self, state_name):
        """
        Gets the current value of the given state name
        :param str state_name: the given state name
        """
        return self.state.get(state_name)

    def is_on_map(self):
        """
        Returns whether or not this object is currently present on the map
        """
        if self.displayable_id is not None:
            return True
        return False

    @staticmethod
    def should_load_consistent(properties):
        """
        :param dict properties: the given properties
        :return: Whether an object with the given properties should result in an old instance of said object
        being loaded
        :rtype: bool
        """
        return (
                'ref_name' in properties and
                getattr(renpy.store, properties['ref_name'], None) is not None and
                properties.get('consistent') is not False)

    def _get_zoom(self):
        """
        :return: A tuple containing the x and y scaling of this object relative to the original tile.
        :rtype: tuple
        """
        xzoom = float(self.width) / float(self.parent_rpg_tile.width)
        yzoom = float(self.height) / float(self.parent_rpg_tile.height)

        return xzoom, yzoom

    @property
    def ref_name(self):
        """
        :return: the reference name used for this object. If set, creates a renpy variable that corresponds to this
        object, allowing it to be targeted during events.
        :rtype: str|None
        """
        if 'ref_name' in self.properties:
            return self.properties['ref_name']
        else:
            return None

    @property
    def width(self):
        """
        :return: the width of this object in pixels.
        :rtype: int
        """
        return self._width

    @property
    def height(self):
        """
        :return: the height of this object in pixels.
        :rtype: int
        """
        return self._height

    @property
    def render_dict(self):
        """
        :return: The render dictionary that should be used to render displayable elements linked to this object
        :rtype: dict
        """
        if self.xzoom != 1.0 or self.yzoom != 1.0:
            return {'xzoom': self.xzoom, 'yzoom': self.yzoom, 'subpixel': True}
        return {}

    @property
    def image(self):
        """
        Retrieves the renpy name for the image currently being portrayed by this object.
        :return: The path to the image currently being portrayed by this object.
        :rtype: str|None
        """
        return self.parent_rpg_tile.image

    @property
    def occultates_as_y(self):
        """
        :return: The y coordinate at which this object is regarded as being placed for the sake of determining its
        render order on dynamic layers
        :rtype: int
        """
        if 'occultates_as_y' in self.properties:
            return self.properties['occultates_as_y']
        if self.parent.orientation == "orthogonal":
            return ceil((self.y + self.height - 2) / self.parent.tile_size.y)
        else:
            return self.y + self.height - 1

    @property
    def next_frame_time(self):
        """
        :return: The frame time at which this object should display its next frame.
        """
        return self.parent_rpg_tile.next_frame_time

    def condition_met(self):
        """
        :return: Whether or not this object's conditional properties are currently met
        :rtype: bool
        """
        if not self.is_conditional:
            return True
        return eval(self.properties['conditional'])

    @property
    def emits_sound(self) -> Optional[str]:
        """
        :return: The path to the looping sound effect that emanates from this object.
        """
        if 'emits_sound' in self.properties:
            return self.properties['emits_sound']
        else:
            return None

    @property
    def emits_sound_scale(self) -> bool:
        """
        :return: Whether or not the sound effect emanating from this object should scale with distance. Has
        no effect if emits_sound is None. Defaults to True.
        """
        if 'emits_sound_scale' in self.properties:
            return self.properties['emits_sound_scale']
        else:
            return True

    @property
    def emits_sound_min_volume(self) -> float:
        """
        :return: Minimum volume to which sound scaling can reduce the sound. If at any level other than 0.0,
        this means that the sound can be heard from anywhere in the map. Should be lower than emits_sound_max_volume.
        Has no effect if emits_sound_scale is False. Defaults to 0.0.
        """
        if 'emits_sound_min_volume' in self.properties:
            return self.properties['emits_sound_min_volume']
        else:
            return 0.0

    @property
    def emits_sound_max_volume(self) -> float:
        """
        :return: Maximum volume to which sound scaling can increase the sound. 1.0 is 100% volume, 0.0 is 0% volume.
        Should be higher than emits_sound_max_volume. Has no effect if emits_sound_scale is False.
        """
        if 'emits_sound_max_volume' in self.properties:
            return self.properties['emits_sound_max_volume']
        else:
            return 1.0

    @property
    def emits_sound_min_volume_distance(self) -> int:
        """
        :return: The distance in tiles from which the emitted sound from this object will play at the minimum volume.
        If not set, defaults to the value of pink_otm_default_min_volume_distance. Has no effect if emits_sound_scale
        is False.
        """
        if 'emits_sound_min_volume_distance' in self.properties:
            return self.properties['emits_sound_min_volume_distance']
        else:
            return renpy.store.pink_otm_default_min_volume_distance

    @property
    def emits_sound_max_volume_distance(self) -> int:
        """
        :return: The distance in tiles up to which the emitted sound from this object will play at maximum volume.
        If not set, defaults to 1. Has no effect if emits_sound_scale is False.
        """
        if 'emits_sound_max_volume_distance' in self.properties:
            return self.properties['emits_sound_max_volume_distance']
        else:
            return 1

    @property
    def emits_sound_pan(self) -> bool:
        """
        :return: Whether the sound effect emanating from this object should pan with horizontal distance. Has
        no effect if emits_sound is None. Defaults to True.
        """
        if 'emits_sound_pan' in self.properties:
            return self.properties['emits_sound_pan']
        else:
            return True

    @property
    def emits_sound_max_pan(self) -> float:
        """
        :return: The absolute maximum level of panning that can be achieved by changing position relative to the
        emitting object. Note that this sets the value for both the maximum left pan and right pan. Defaults to
        1.0.
        """
        if 'emits_sound_max_pan' in self.properties:
            return self.properties['emits_sound_max_pan']
        else:
            return 1.0

    @property
    def emits_sound_mixer(self) -> str:
        """
        :return: Which sound mixer (sound slider in the settings) should be used to control the volume of the sound
        emanating from this object. Valid values are 'sfx', 'music' and 'voice'.
        """
        if 'emits_sound_mixer' in self.properties:
            return self.properties['emits_sound_mixer']
        else:
            return 'sfx'

    @property
    def emits_sound_max_pan_distance(self) -> int:
        """
        :return: The distance in tiles from which the emitted sound from this object will play fully panned.
        If not set, defaults to the value of pink_otm_default_max_pan_distance. Has no effect if emits_sound_scale
        is False.
        """
        if 'emits_sound_max_pan_distance' in self.properties:
            return self.properties['emits_sound_max_pan_distance']
        else:
            return renpy.store.pink_otm_default_max_pan_distance

    @property
    def emits_sound_no_pan_distance(self) -> int:
        """
        :return: The distance in tiles up to which emitted sound from this object will not pan. Defaults to 0.
        Has no effect if emits_sound_scale is False.
        """
        if 'emits_sound_no_pan_distance' in self.properties:
            return self.properties['emits_sound_no_pan_distance']
        else:
            return 0

    @property
    def sound_tag(self) -> Optional[str]:
        """
        :return: The tag for movement sound played when moving into this object. Note that the tag should correspond
        to a key in the pink_otm_terrain_noises dictionary defined in standard_events.rpy.
        """
        return self.properties.get('sound_tag')


class TiledMapGameObjectSpriteCollection(TiledMapGameObject):
    def __init__(
            self, x, y, layer, properties, collection_path
    ):
        """
        :param int x: The distance in pixels between this object's image's left side and the left border of the map
        :param int y: The distance in pixels between this object's image's left side and the left border of the map
        :param TiledMapGameLayer layer: The layer on which this object exists
        :param dict properties: The dictionary of properties for this object
        :param str collection_path: The path to this object's sprite collection
        """
        if self.should_load_consistent(properties):
            old_incarnation = getattr(renpy.store, properties['ref_name'], None)  # type: TiledMapGameObjectSpriteCollection  # noqa
            if old_incarnation.sprite_collection_path.startswith('renpy.store'):
                self._initiate_consistent_variable_sprite_collection(old_incarnation=old_incarnation)
            else:
                self.sprite_collection_path = old_incarnation.sprite_collection_path  # note can be a variable name
                self.sprite_collection = old_incarnation.sprite_collection
            self.sprite_collection.st_reset_frames(0.0)
            self.sprite_collection.latest_frame_gt = 0.0
        else:
            if not hasattr(self, 'sprite_collection'):
                self.sprite_collection_path = collection_path
                if collection_path.startswith('renpy.store'):
                    collection_path = eval(collection_path)
                self.sprite_collection = TiledMapSpriteCollection(renpy.exports.file(collection_path))

        TiledMapGameObject.__init__(
            self, self.sprite_collection, x, y, self.sprite_collection.width,
            self.sprite_collection.height, layer, properties)

        self.current_animation_name = None  # Set by _set_animation
        if self.should_load_consistent(properties):
            old_incarnation = getattr(renpy.store, properties['ref_name'], None)  # type: TiledMapGameObjectSpriteCollection  # noqa

            self._orientation = old_incarnation._orientation
            self._set_animation(old_incarnation.current_animation_name)
            self.st_reset_frames(0.0)
        else:
            # These need properties to initialize, so are after the parent class initialization
            self._orientation = self.start_orientation
            self._set_animation(self.default_animation)

        if self.parent is not None:
            # Rare cases where you create an object without a map being visible, such as adding OTM followers when no
            # OTM map is onscreen.
            self.parent.animated_tiles.append(self.sprite_collection)

        if type(self) is TiledMapGameObjectSpriteCollection and self.ref_name is not None:
            # Type comparison ensures this only happens at the end of the final loading
            setattr(renpy.store, self.ref_name, self)

    def _initiate_consistent_variable_sprite_collection(
            self, old_incarnation: 'TiledMapGameObjectSpriteCollection'
    ):
        self.sprite_collection_path = old_incarnation.sprite_collection_path
        self._orientation = old_incarnation.orientation
        self.current_animation_name = None
        self.sprite_collection = TiledMapSpriteCollection(renpy.exports.file(eval(self.sprite_collection_path)))
        self._set_animation(old_incarnation.current_animation_name)

    def _set_animation(self, animation_name, speed=None):
        """
        This function is called to set the object's current animation set. It calls an oriented animation
        (ex. walk_left) if one is available.
        :param str animation_name: Name of the new animation
        :param float speed: The speed at which to play the animation. None if the default speed should be used.
        """
        if animation_name is None:
            return

        oriented_name = animation_name + "_" + self._orientation
        if oriented_name in self.sprite_collection.data:
            if oriented_name != self.current_animation_name:
                self.current_animation_name = oriented_name
                self.sprite_collection.set_animation(oriented_name, speed=speed)
        else:
            if animation_name != self.current_animation_name:
                self.current_animation_name = animation_name
                self.sprite_collection.set_animation(animation_name, speed=speed)

    def st_reset_frames(self, st):
        """
        :param float st: Game time in seconds.
        :return: Rebases this animation's next frame time based on the given st. This function was designed to
        be used after st resets when displaying a map.
        """
        self.sprite_collection.st_reset_frames(st)

    def _get_zoom(self):
        """
        :return: A tuple containing the x and y scaling of this object relative to the original tile.
        :rtype: tuple
        """
        return 1.0, 1.0

    @property
    def width(self):
        """
        :return: the width of this object in pixels.
        :rtype: int
        """
        return self.sprite_collection.width

    @property
    def height(self):
        """
        :return: the height of this object in pixels.
        :rtype: int
        """
        return self.sprite_collection.height

    @property
    def start_orientation(self):
        """
        :return: the orientation this sprite collection object should start out with.
        :rtype: str
        """
        if 'start_orientation' in self.properties:
            return self.properties['start_orientation']
        else:
            return 'down'

    @property
    def stand_animation(self):
        """
        :return: the name of the animation to display when this object is standing still.
        :rtype: str
        """
        if 'stand_animation' in self.properties:
            return self.properties['stand_animation']
        else:
            return 'stand'

    @stand_animation.setter
    def stand_animation(self, value):
        """
        :param str value: The new stand_animation name
        """
        if (
                self.current_animation_name == self.stand_animation or
                self.current_animation_name == self.stand_animation + "_" + self._orientation
        ):
            currently_standing = True
        else:
            currently_standing = False

        self.properties['stand_animation'] = value

        if currently_standing:
            self._set_animation(value)

    @property
    def move_animation(self):
        """
        :return: the name of the animation to display when this object is moving.
        :rtype: str
        """
        if 'move_animation' in self.properties:
            return self.properties['move_animation']
        else:
            return 'walk'

    @move_animation.setter
    def move_animation(self, value):
        """
        :param str value: The new move_animation name
        """
        if (
                self.current_animation_name == self.move_animation or
                self.current_animation_name == self.move_animation + "_" + self._orientation
        ):
            currently_moving = True
        else:
            currently_moving = False

        self.properties['move_animation'] = value

        if currently_moving:
            self._set_animation(value)

    @property
    def default_animation(self):
        """
        :return: the name of the animation to display when this object is initialized
        :rtype: str
        """
        if 'default_animation' in self.properties:
            return self.properties['default_animation']
        else:
            return self.stand_animation

    @property
    def orientation(self):
        """
        :return: The object's current orientation
        :rtype: str
        """
        return self._orientation

    @orientation.setter
    def orientation(self, value):
        """
        :param str value: Changes the object's orientation to the given orientation
        """
        uvalue = "_" + value
        current_animation_name = self.current_animation_name.\
            replace('_up', uvalue).replace('_down', uvalue).replace('_left', uvalue).replace('_right', uvalue)

        self._orientation = value
        self._set_animation(current_animation_name)

    @property
    def image(self):
        """
        Retrieves the renpy name for the image currently being portrayed by this collection object.
        :return: The path to the image currently being portrayed by this collection object.
        :rtype: str|None
        """
        if self.sprite_collection is None:
            return None
        else:
            return self.sprite_collection.image

    def switch_sprite_collection(self, target_sprite_collection):
        """
        Switches to a new sprite collection, ensuring that coordinates and animation name are kept the same.
        :param str target_sprite_collection: Path of the new sprite collection.
        :return:
        """
        if self.parent is not None:
            self.parent.animated_tiles.remove(self.sprite_collection)
        animation_name = self.current_animation_name
        start_time = self.sprite_collection.latest_frame_gt
        if self.parent is not None:
            self.parent.remove_element(self)
        self.current_animation_name = None  # So new animation doesn't register as the same
        self.sprite_collection = TiledMapSpriteCollection(renpy.loader.transfn(
                "pink_engine/sprite_collections/" + target_sprite_collection), start_time)
        self._set_animation(animation_name)

        if self.parent is not None:
            self.parent.add_element(self.x, self.y, self.layer, self)
            self.parent.animated_tiles.append(self.sprite_collection)


class TiledMapCamera(object):
    def __init__(self, game_map):
        """
        This class serves as the in-game camera for the Pink Engine maps, with the x and y being used as the
        viewport adjustment variables in Pink Engine map screens.
        :param TiledMapGame game_map: The game map this is the camera of
        """
        config = renpy.store.config
        self.map = game_map

        self.viewport_x_offset = 0
        self.viewport_y_offset = 0
        self.viewport_width = config.screen_width
        self.viewport_height = config.screen_height

        self.x = renpy.display.behavior.Adjustment(value=0, range=game_map.image_size.x)
        self.y = renpy.display.behavior.Adjustment(value=0, range=game_map.image_size.y)

        self.xzoom = renpy.store.pink_tmd_camera_default_zoom  # TODO property of map
        self.yzoom = renpy.store.pink_tmd_camera_default_zoom  # TODO property of map

    def center_on_target(self):
        """
        Makes the camera center on its current target.
        """
        pass


class TiledMapGame(renpy.exports.Displayable):
    tile_class = TiledMapGameTile
    tile_animated_class = TiledMapGameTileAnimated
    sprite_collection_class = TiledMapSpriteCollection

    object_class = TiledMapGameObject
    object_sprite_collection_class = TiledMapGameObjectSpriteCollection

    camera_class = TiledMapCamera

    def __init__(self, map_dict, path, **kwargs):
        """
        The parent class of all Pink Engine game maps.
        :param dict map_dict: The initialization dictionary for this map
        :param str path: The path at which this map can be found.
        """
        renpy.exports.Displayable.__init__(self, **kwargs)  # Py2

        """Location of the file. Also serve as the unique ID for the map."""
        self.path = path

        # ----
        self.last_gt = 0.0

        # ----

        # ---------------------------------Pink Engine Properties-----------------------------------------------------
        self.properties = {}
        if map_dict.get('properties'):
            for layer_property in map_dict['properties']:
                self.properties[layer_property['name']] = layer_property['value']

        # ---------------------------------Simple Global Properties---------------------------------------------------
        self.orientation = map_dict["orientation"]
        self.render_order = map_dict["renderorder"]

        """Size of map in tiles."""
        self.grid_size = Coord(x=map_dict.get('width'), y=map_dict.get('height'))

        """Size of the tiles in the map"""
        self.tile_size = Coord(x=map_dict.get('tilewidth'), y=map_dict.get('tileheight'))

        """Size of map in pixels"""
        if self.orientation == "isometric":
            self.image_size = Coord(
                x=int((self.grid_size.x * self.tile_size.x * 0.5) + (self.grid_size.y * self.tile_size.x * 0.5)),
                y=int((self.grid_size.x * self.tile_size.y * 0.5) + (self.grid_size.y * self.tile_size.y * 0.5)))
        elif self.orientation == "staggered":
            self.image_size = Coord(
                x=int((self.grid_size.x + 0.5) * self.tile_size.x),
                y=int(((self.grid_size.y + 1) * self.tile_size.y * 0.5)))
        elif self.orientation == "hexagonal":
            self.image_size = Coord(
                x=int((self.grid_size.x + 0.5) * self.tile_size.x),
                y=int(((self.grid_size.y + 0.75) * self.tile_size.y * 0.75)))
        else:  # Orthogonal
            self.image_size = Coord(x=self.grid_size.x * self.tile_size.x, y=self.grid_size.y * self.tile_size.y)

        # --- init global
        self.camera = self.camera_class(self)
        self.config = renpy.store.config

        # ---------------------------------Initiate Displayables--------------------------------------------------------
        self._displayable = TiledMap(self, **kwargs)
        self._overlay_manager = OverlayManager()

        # ---------------------------------Initiate Indexes--------------------------------------------------------
        self.tilesets = self._get_tilesets_from_dict(map_dict)

        # A list of all registered images used in this map. Used to start and stop image prediction. Tiles and objects
        # add the images they use as they load.
        self.registered_images = set()

        # Index with all objects. Allows you to target specific objects on the map
        self.map_objects = {}
        self.next_id = 0

        # Index of base tiles. Used so that every tile only needs to be looked up once.
        self.base_tiles = {}

        # ---------------------------------Initiate Per-frame lists-----------------------------------------------------
        # List of animated tiles. Used to update animation state during every frame
        self.animated_tiles = []

        # List of conditional objects. Used to add and remove objects every frame
        self.conditional_objects = []

        # Variable sprite collections set, used to update sprite collections with a variable name.
        self.variable_sprite_collections: List[TiledMapGameObjectSpriteCollection] = []

        # ---------------------------------Initiate Layers--------------------------------------------------------
        self.layers = []
        for layer_dict in map_dict.get('layers'):
            self.add_layer(layer_dict=layer_dict)

        # ----
        self.event_type_functions = {}
        self.controls_enabled = True

        # ----
        self.start_predicting()

    def recheck_variable_sprite_collections(self):
        """
        For every object with a variable sprite collection, checks if the value of the variable has changed, and
        then switches the sprite collection if so.
        """
        for variable_sprite_collection_object in self.variable_sprite_collections:
            if (
                    variable_sprite_collection_object.is_conditional and
                    not variable_sprite_collection_object.condition_met()
            ):
                continue

            variable_sprite_collection_object.switch_sprite_collection(
                variable_sprite_collection_object.sprite_collection_path)

    def get_next_id(self):
        """
        :return: The id that should be used for the next displayable element
        :rtype: int
        """
        next_id = self.next_id
        self.next_id += 1
        return next_id

    def check_existence(self):
        return renpy.store.pink_tmd_current_map is not None

    def move_element(self, element_id, new_x, new_y):
        """
        Moves the element with the given ID to the given new x and y
        :param int element_id: The given element id
        :param int new_x: The new x (in pixels)
        :param int new_y: The new y (in pixels)
        """
        self._displayable.move_element(element_id, new_x, new_y)

    def add_layer(self, layer_dict):
        """
        Adds a new layer to this map and returns it.
        :param dict layer_dict: The initialization dictionary for tne new layer
        :return: the new layer
        :rtype: TiledMapGameLayer
        """
        new_layer = TiledMapGameLayer(self, layer_dict)
        self.layers.append(new_layer)
        return new_layer

    def render(self, width, height, st, at):
        """
        :param int width:
        :param int height:
        :param float st: The shown time (in seconds).
        :param float at: The animation time (in seconds).
        """
        # initiate render object
        render = renpy.exports.Render(width, height)

        if not self.check_existence():  # prevents crash on completion of game
            return render

        self.game_tick(st)

        renpy.exports.redraw(self, 0)
        return render

    def event(self, ev, x, y, st):  # noqa mandatory variables
        """
        Makes this game object respond to events, such as key presses.
        """
        if self.controls_enabled:
            if ev.type in self.event_type_functions:
                self.event_type_functions[ev.type](self, ev, x, y, st)

    def game_tick(self, gt):
        """
        Core gameplay loop, advancing the game by a single tick per run.
        :param float gt: The current game time in seconds
        """
        self.check_animated_tiles(gt)
        self.check_conditional_objects()
        self.last_gt = gt

    def check_animated_tiles(self, gt):
        """
        Updates the current frame of all animated tiles.
        """
        for animated_tile in self.animated_tiles:
            animated_tile.update_frame(gt)

    def check_conditional_objects(self):
        """
        Checks all conditional objects, adding and removing them according to whether or not their condition is
        currently met.
        """
        for conditional_object in self.conditional_objects:
            self.check_conditional_object(conditional_object)

    def check_conditional_object(self, conditional_object):
        """
        Checks the given object's conditionality, adding and removing it according to whether or not their condition is
        currently met.
        :param TiledMapGameObject conditional_object: The object to check the conditionality of
        """
        if not conditional_object.is_on_map() and conditional_object.condition_met():
            if conditional_object.layer.layer_type in VISIBLE_LAYERS:
                self._displayable.add_element(
                    x=conditional_object.x, y=conditional_object.y, layer=conditional_object.layer,
                    game_object=conditional_object)
        elif conditional_object.is_on_map() and not conditional_object.condition_met():
            if conditional_object.displayable_id is not None:
                self._displayable.remove_element(conditional_object.displayable_id)

    @staticmethod
    def _get_tilesets_from_dict(map_dict):
        tilesets = {}
        for tileset in map_dict.get('tilesets'):
            tileset_source = tileset.get('source')

            """Gets the id at which the tileset starts."""
            first_gid = tileset.get('firstgid')

            """If the tileset has not yet been loaded, does so."""
            tileset_source = renpy.loader.transfn("pink_engine/orthogonal_tiled_maps/" + tileset_source)
            if tileset_source not in pink_tileset_dict:
                Tileset(tileset_source)
            tilesets[first_gid] = pink_tileset_dict[tileset_source]
        return tilesets

    def get_tile_object(self, gid):
        """
        :param int gid: The given gid
        :return: The object from the tileset with the given gid.
        :rtype: TiledMapGameTile
        """
        if gid not in self.base_tiles:
            source_tile = self.get_tile(gid)
            if type(source_tile) is TilesetTile:
                new_tile = self.tile_class(self, source_tile)
            else:
                new_tile = self.tile_animated_class(self, source_tile)  # noqa
                self.animated_tiles.append(new_tile)

            self.base_tiles[gid] = new_tile
        base_tile = self.base_tiles[gid]

        return base_tile

    def add_object(self, object_dict, x, y, layer):
        """
        Adds a new object to this game. This function handles the object being created and added to this class' relevant
        indexes, whereas add_element adds it to the game map proper
        :param dict object_dict: The object dictionary to initialize the new object
        :param int x: The distance in pixels between the object's image's left side and the left border of the map
        :param int y: The distance in pixels between this object's image's left side and the left border of the map
        :param TiledMapGameLayer layer: The layer on which this object will exist
        """
        # pulled out of the dict)
        property_list = object_dict.get('properties')
        if property_list is None:
            property_list = []

        # Get object properties
        object_properties = {}
        for object_property in property_list:
            object_properties[object_property['name']] = object_property['value']

        # Add base tile properties
        sprite_path = None
        gid = object_dict.get('gid')  # manually added objects, such as player, don't have a gid.
        if gid is not None:
            base_tile = self.get_tile_object(gid)
            for property_key in base_tile.properties:
                if property_key not in object_properties:  # don't override object properties of the same name
                    object_properties[property_key] = base_tile.properties[property_key]
        if "sprite_collection_path" in object_properties:
            sprite_path = object_properties['sprite_collection_path']

        if gid is None and sprite_path is None:
            # An object with neither a gid nor a sprite collection is not added to the map. It is either a Tiled
            #  base shape, or an improperly formatted manually added object.
            return

        # Initialize actual object
        if sprite_path is not None:
            new_object = self.object_sprite_collection_class(x, y, layer, object_properties, sprite_path)
            if sprite_path.startswith('renpy.store'):
                self.variable_sprite_collections.append(new_object)
        else:
            width, height, gid = object_dict['width'], object_dict['height'], object_dict['gid']
            base_tile = self.get_tile_object(gid)
            new_object = self.object_class(base_tile, x, y, width, height, layer, object_properties)

        # Gives the object an id and adds it to the map's index
        new_object.map_id = self.get_next_id()
        self.map_objects[new_object.map_id] = new_object

        # Add the object to the game
        self.add_element(new_object.x, new_object.y, layer, new_object)
        return new_object

    def add_tile(self, tile, x, y, layer):
        """
        Adds an instance of a tile to this game map
        :param self.tile_class|self.tile_animated_class tile: The tile the new tile instance is an instance of
        :param int x: The distance in pixels between the tile's image's left side and the left border of the map
        :param int y: The distance in pixels between this tile's image's left side and the left border of the map
        :param TiledMapGameLayer layer: The layer on which this object will exist
        """
        self.add_element(x, y, layer, tile)

    def add_element(self, x, y, layer, game_object, already_in_conditional=False):
        """
        Adds a new element (tile or object) to this game map
        :param int x: The distance in pixels between the tile's image's left side and the left border of the map
        :param int y: The distance in pixels between this tile's image's left side and the left border of the map
        :param TiledMapGameLayer layer: The layer on which this object will exist
        :param self.tile_class|self.tile_animated_class|self.object_class game_object:
        :param bool already_in_conditional: Set to True when adding an object that is already present in the
        conditional list, so that it does not get re-added.
        """
        if game_object.is_conditional and not already_in_conditional:
            self.conditional_objects.append(game_object)
            if game_object.condition_met() and layer.layer_type in VISIBLE_LAYERS:
                self._displayable.add_element(x=x, y=y, layer=layer, game_object=game_object)
        elif layer.layer_type in VISIBLE_LAYERS:
            self._displayable.add_element(x=x, y=y, layer=layer, game_object=game_object)

    def remove_element(self, element):
        """
        Removes the given element from this map
        :param self.tile_class|self.tile_animated_class|self.object_class element: The element to be removed from this
        map
        """
        element_id = element.displayable_id

        if element_id is not None:
            self._displayable.remove_element(element_id)

    def get_overlay_manager(self) -> OverlayManager:
        """
        :return: This object's overlay manager
        """
        return self._overlay_manager

    def get_displayable(self) -> TiledMap:
        """
        :return: This object's displayable
        """
        return self._displayable

    def get_tile(self, tile_id):
        """
        Returns the image path for the tile that uses the given ID in this map.

        :param int tile_id: The id used by the given tile on this map. Is equal to the tile's ID within its own tileset
        plus the first_gid for the tileset in this map.
        :return: The tile with the given id.
        :rtype: TilesetTile
        """
        if tile_id == 0:
            return None  # Empty tile

        if tile_id > 2147483648:  # TODO horizontal flip, currently not supported
            tile_id -= 2147483648
        if tile_id > 1073741824:  # TODO vertical flip, currently not supported
            tile_id -= 1073741824
        if tile_id > 536870912:  # TODO diagonal flip, currently not supported
            tile_id -= 536870912

        """First identifies which tileset the image id is from, then retrieves the appropriate tile"""
        first_gids = sorted(self.tilesets, reverse=True)
        prev_gid = first_gids[0]

        while len(first_gids) > 0:
            prev_gid = first_gids.pop(0)
            if tile_id >= prev_gid:
                break

        tile_object = self.tilesets[prev_gid].get_tile(tile_id - prev_gid)

        return tile_object

    def start_predicting(self):
        """
        Causes renpy to start predicting all the images on this map
        """
        for image_name in self.registered_images:
            renpy.exports.start_predict(image_name)

    def stop_predicting(self):
        """
        Causes renpy to stop predicting all the images on this map
        """
        for image_name in self.registered_images:
            renpy.exports.stop_predict(image_name)


class TiledMapGameLayer(object):
    def __init__(self, parent, layer_dict):
        """
        A single layer of a pink engine map
        :param TiledMapGame parent: The game map this layer is a part of
        :param dict layer_dict: The dictionary used to initialize this layer
        """
        self.parent = parent

        # Initializes custom properties
        self.properties = {}
        if layer_dict.get('properties'):
            for layer_property in layer_dict['properties']:
                self.properties[layer_property['name']] = layer_property['value']

        # Returns if condition not met
        if not self.condition_met:
            return

        # Executes orientation/type-specific init script.
        if layer_dict.get('type') == "tilelayer" and self.layer_type in LAYER_PRIORITY:
            if self.parent.orientation == "orthogonal":
                self._init_orthogonal_tile_layer(layer_dict=layer_dict)
            elif self.parent.orientation == "isometric":
                self._init_isometric_tile_layer(layer_dict=layer_dict)
            elif self.parent.orientation == "staggered":
                self._init_staggered_tile_layer(layer_dict=layer_dict)
            elif self.parent.orientation == "hexagonal":
                self._init_hexagonal_tile_layer(layer_dict=layer_dict)
        elif layer_dict.get('type') == "objectgroup" and self.layer_type in LAYER_PRIORITY:
            if self.parent.orientation == "orthogonal":
                self._init_orthogonal_object_layer(layer_dict=layer_dict)
            elif self.parent.orientation == "isometric":
                self._init_isometric_object_layer(layer_dict=layer_dict)
            elif self.parent.orientation == "staggered":
                self._init_staggered_object_layer(layer_dict=layer_dict)
            elif self.parent.orientation == "hexagonal":
                self._init_hexagonal_object_layer(layer_dict=layer_dict)

    def _init_orthogonal_tile_layer(self, layer_dict):
        """
        Initializes a tile layer for an orthogonal map
        :param dict layer_dict: The dictionary used to initialize this layer
        """
        xoffset = layer_dict['offsetx'] if layer_dict.get('offsetx') is not None else 0
        yoffset = layer_dict['offsety'] if layer_dict.get('offsety') is not None else 0
        x, c, y = xoffset, 0, yoffset
        if layer_dict.get('data') is None:
            return
        for gid in layer_dict['data']:
            if gid != 0:
                tile = self.parent.get_tile_object(gid)
                place_y = y - tile.height + self.parent.tile_size.y
                self.parent.add_tile(x=x, y=place_y, layer=self, tile=tile)
            x += self.parent.tile_size.x
            c += 1
            if c == self.parent.grid_size.x:
                y += self.parent.tile_size.y
                c, x = 0, xoffset

    def _init_orthogonal_object_layer(self, layer_dict):
        """
        Initializes an object layer for an orthogonal map
        :param dict layer_dict: The dictionary used to initialize this layer
        """
        xoffset = layer_dict['offsetx'] if layer_dict.get('offsetx') is not None else 0
        yoffset = layer_dict['offsety'] if layer_dict.get('offsety') is not None else 0
        if layer_dict.get('objects') is None:
            return
        for layer_object in layer_dict['objects']:
            x = layer_object['x'] + xoffset
            y = layer_object['y'] - layer_object['height'] + yoffset

            self.parent.add_object(layer_object, x, y, self)

    def _init_isometric_tile_layer(self, layer_dict):
        """
        Initializes a tile layer for an isometric map
        :param dict layer_dict: The dictionary used to initialize this layer
        """
        xoffset = layer_dict['offsetx'] if layer_dict.get('offsetx') is not None else 0
        yoffset = layer_dict['offsety'] if layer_dict.get('offsety') is not None else 0
        xcount, ycount = 0, 0
        if layer_dict.get('data') is None:
            return

        for gid in layer_dict['data']:
            if gid != 0:
                tile = self.parent.get_tile_object(gid)
                place_x = ((self.parent.grid_size.y - 1) * self.parent.tile_size.x * 0.5) + \
                          (self.parent.tile_size.x * xcount * 0.5) - (self.parent.tile_size.y * ycount * 0.5) + xoffset
                place_y = (self.parent.tile_size.x * xcount * 0.5) + (self.parent.tile_size.y * ycount * 0.5) - \
                    tile.height + self.parent.tile_size.y + yoffset
                self.parent.add_tile(x=place_x, y=place_y, layer=self, tile=tile)
            xcount += 1
            if xcount == self.parent.grid_size.x:
                xcount = 0
                ycount += 1

    def _init_isometric_object_layer(self, layer_dict):
        """
        Initializes an object layer for an isometric map
        :param dict layer_dict: The dictionary used to initialize this layer
        """
        xoffset = layer_dict['offsetx'] if layer_dict.get('offsetx') is not None else 0
        yoffset = layer_dict['offsety'] if layer_dict.get('offsety') is not None else 0
        if layer_dict.get('objects') is None:
            return
        for layer_object in layer_dict['objects']:
            width, height = layer_object['width'], layer_object['height']
            x = (self.parent.grid_size.y * self.parent.tile_size.x * 0.5) + (layer_object['x'] * 0.5) - \
                (layer_object['y'] * 0.5) - (width * 0.5) + xoffset
            y = (layer_object['x'] * 0.5) + (layer_object['y'] * 0.5) - height + yoffset

            self.parent.add_object(layer_object, x, y, self)

    def _init_staggered_tile_layer(self, layer_dict):
        """
        Initializes a tile layer for a staggered  map
        :param dict layer_dict: The dictionary used to initialize this layer
        """
        xoffset = layer_dict['offsetx'] if layer_dict.get('offsetx') is not None else 0
        yoffset = layer_dict['offsety'] if layer_dict.get('offsety') is not None else 0
        xcount, ycount = 0, 0
        if layer_dict.get('data') is None:
            return
        for gid in layer_dict['data']:
            if gid != 0:
                tile = self.parent.get_tile_object(gid)
                place_x = xcount * self.parent.tile_size.x + xoffset
                if ycount % 2 != 0:
                    place_x += int(self.parent.tile_size.x * 0.5)
                place_y = int(self.parent.tile_size.y * ycount * 0.5) - tile.height + self.parent.tile_size.y + \
                    yoffset
                self.parent.add_tile(x=place_x, y=place_y, layer=self, tile=tile)
            xcount += 1
            if xcount == self.parent.grid_size.x:
                xcount = 0
                ycount += 1

    def _init_staggered_object_layer(self, layer_dict):
        """
        Initializes an object layer for a staggered map
        :param dict layer_dict: The dictionary used to initialize this layer
        """
        xoffset = layer_dict['offsetx'] if layer_dict.get('offsetx') is not None else 0
        yoffset = layer_dict['offsety'] if layer_dict.get('offsety') is not None else 0
        if layer_dict.get('objects') is None:
            return
        for layer_object in layer_dict['objects']:
            x = layer_object['x'] + xoffset
            y = layer_object['y'] - int(layer_object['height']) + yoffset

            self.parent.add_object(layer_object, x, y, self)

    def _init_hexagonal_tile_layer(self, layer_dict):
        """
        Initializes a tile layer for a hexagonal map
        :param dict layer_dict: The dictionary used to initialize this layer
        """
        xoffset = layer_dict['offsetx'] if layer_dict.get('offsetx') is not None else 0
        yoffset = layer_dict['offsety'] if layer_dict.get('offsety') is not None else 0
        xcount, ycount = 0, 0
        if layer_dict.get('data') is None:
            return
        for gid in layer_dict['data']:
            if gid != 0:
                tile = self.parent.get_tile_object(gid)
                place_x = xcount * self.parent.tile_size.x + xoffset
                if ycount % 2 != 0:
                    place_x += int(self.parent.tile_size.x * 0.5)
                place_y = int(self.parent.tile_size.y * ycount * (3.0/4.0)) - tile.height + \
                    self.parent.tile_size.y + yoffset
                self.parent.add_tile(x=place_x, y=place_y, layer=self, tile=tile)
            xcount += 1
            if xcount == self.parent.grid_size.x:
                xcount = 0
                ycount += 1

    def _init_hexagonal_object_layer(self, layer_dict):
        """
        Initializes an object layer for a hexagonal map
        :param dict layer_dict: The dictionary used to initialize this layer
        """
        xoffset = layer_dict['offsetx'] if layer_dict.get('offsetx') is not None else 0
        yoffset = layer_dict['offsety'] if layer_dict.get('offsety') is not None else 0
        if layer_dict.get('objects') is None:
            return
        for layer_object in layer_dict['objects']:
            x = layer_object['x'] + xoffset
            y = layer_object['y'] - int(layer_object['height']) + yoffset + 1

            self.parent.add_object(layer_object, x, y, self)

    @property
    def layer_type(self):
        """
        :return: The layer's type (super, sub, dynamic, movement, interaction). Super renders over dynamic, which
        renders over sub. Independent from the tile layer and object layer distinction.
        :rtype: str
        """
        if "layer_type" in self.properties:
            return self.properties["layer_type"]
        else:
            return "sub"

    @property
    def z_order(self):
        """
        :return: The layer's z-order (priority order for rendering). Lower z-orders of the same type render below higher
        z-orders of the same type.
        :rtype: int
        """
        if "z_order" in self.properties:
            return self.properties["z_order"]
        else:
            return 0

    @property
    def condition_met(self):
        if 'conditional' in self.properties:
            return eval(self.properties['conditional'])
        else:
            return True


def filepath_to_reg_image(image_filepath):
    """
    :param str image_filepath: The given image filepath
    :return: The
    :rtype: str
    """
    folder_path, file_name = os.path.split(image_filepath)
    file_name, file_ext = os.path.splitext(file_name)
    return renpy.exports.get_registered_image(file_name.lower())


# TODO When checking mobile objects and animated object, use the next gt for their animation/movement, rather than
#  looping through all. That way, objects with slow animations or rare movements won't affect tps.
# TODO restore interaction and movement layer functionality?

# TODO matrix effect
