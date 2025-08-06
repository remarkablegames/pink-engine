default test_corridor_A26_minute = 0
default test_corridor_A26_hour = 7

default test_corridor_A26_day = 1

init python:
    def test_corridor_A26_code_on_enter():
        if not renpy.store.otm_timer.exists('test_corridor_A26_day_timer'):
            renpy.store.A26_time_overlay = pink_otm_current_map.add_overlay_text(
                "day [test_corridor_A26_day]: [test_corridor_A26_hour]:[test_corridor_A26_minute]", 0.5, 0.75, consistent=True)
            renpy.store.otm_timer.add_timed_code(renpy.store.otm_timer.time + 1, 'renpy.store.test_corridor_A26_minute_pass()', 'test_corridor_A26_day_timer')

    def test_corridor_A26_minute_pass():
        renpy.store.test_corridor_A26_minute += 20
        if renpy.store.test_corridor_A26_minute == 60:
            renpy.store.test_corridor_A26_minute = 0
            renpy.store.test_corridor_A26_hour += 1
            if renpy.store.test_corridor_A26_hour == 24:
                renpy.store.test_corridor_A26_hour = 0
        renpy.store.otm_timer.add_timed_code(renpy.store.otm_timer.time + 1, 'renpy.store.test_corridor_A26_minute_pass()', 'test_corridor_A26_day_timer')

label test_corridor_A26_sign:
    $ pink.otm.start_continuing_event()
    """This room exists to test recursive timed code. While you're in this room, twenty in-universe minutes will pass
    for every second of game time, meaning a day will take a little over 1 minute.

    This room will have flowers in it every day between 8PM and midnight.

    Note: Implementing a timer in this manner is not actually a good idea for a game, as it does not interact with the
    increment function (demonstrated in the next room).

    It is only intended as an example of recursive timed code."""
    $ pink.otm.end_current_event()

label test_corridor_A26_sign_2:
    $ pink.otm.start_continuing_event()
    """You can make it so that timers automatically pause during certain classes of events.

    This is governed by the variables 'pink_otm_pause_timer_on_static_event', 'pink_otm_pause_timer_on_dynamic_event'
    and 'pink_otm_pause_timer_on_continuing_event'.

    These variables are defined in pink_config.rpy."""
    $ pink.otm.end_current_event()

label test_corridor_A26_sign_s:
    $ pink.otm.start_static_event()
    """This is a static event. The setting 'pink_otm_pause_timer_on_static_event' is set to [pink_otm_pause_timer_on_static_event]"""
    $ pink.otm.end_current_event()

label test_corridor_A26_sign_d:
    $ pink.otm.start_dynamic_event()
    """This is a dynamic event. The setting 'pink_otm_pause_timer_on_dynamic_event' is set to [pink_otm_pause_timer_on_dynamic_event]"""
    $ pink.otm.end_current_event()

label test_corridor_A26_sign_c:
    $ pink.otm.start_continuing_event()
    """This is a dynamic event. The setting 'pink_otm_pause_timer_on_continuing_event' is set to [pink_otm_pause_timer_on_continuing_event]"""
    $ pink.otm.end_current_event()
