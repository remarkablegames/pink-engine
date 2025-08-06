init python:
    def test_corridor_A27_computer_1():
        if renpy.store.otm_timer.exists('test_corridor_A27_timer'):
            renpy.store.otm_timer.remove_timed_code('test_corridor_A27_timer')
        renpy.store.otm_timer.add_timed_event(renpy.store.otm_timer.time + 5, 'test_corridor_A27_timed_event', 'test_corridor_A27_timer')

    def test_corridor_A27_computer_3():
        if renpy.store.otm_timer.exists('test_corridor_A27_timer2'):
            renpy.store.otm_timer.remove_timed_code('test_corridor_A27_timer2')
        renpy.store.otm_timer.add_timed_event(renpy.store.otm_timer.time + 36000, 'test_corridor_A27_timed_event2', 'test_corridor_A27_timer2')

    def test_corridor_A27_computer_4():
        renpy.store.otm_timer.increment(3600)

label test_corridor_A27_sign:
    $ pink.otm.start_continuing_event()
    """This room exists to test timed events. Interact with the first computer on the right, and an event should
    trigger in 5 seconds.

    To prevent the event from triggering, interact with the second computer.

    Note that the timer will persist upon leaving the room. This makes the function great for giving the player timed
    tasks, like defusing a bomb."""
    $ pink.otm.end_current_event()

label test_corridor_A27_sign2:
    $ pink.otm.start_continuing_event()
    """There are situations where you want to increment your timer, simulating a large portion of time passing all at
    once.

    Think of the player only having ten hours to solve a mystery, but traveling between maps subtracts from that time.

    For these cases, you can use the 'increment' function to increase the progress of all timers.

    Interact with the computer on the right to start a timer for an event that happens in 10 hours.

    Every interaction with the second computer will increment the global timer by 1 hour."""
    $ pink.otm.end_current_event()

label test_corridor_A27_timed_event:
    $ pink.otm.start_continuing_event()
    """This is a timed event, which has been triggered after 5 seconds have passed."""
    $ pink.otm.end_current_event()

label test_corridor_A27_timed_event2:
    $ pink.otm.start_continuing_event()
    """This is a timed event, which has been triggered after 10 hours have passed."""
    $ pink.otm.end_current_event()

label test_corridor_A27_computer_2:
    $ pink.otm.start_continuing_event()
    if not renpy.store.otm_timer.exists('test_corridor_A27_timer'):
        "You cannot deactivate the event, no timer is currently running..."
    else:
        $ _time_left = renpy.store.otm_timer.remaining_time('test_corridor_A27_timer')
        $ renpy.store.otm_timer.remove_timed_event('test_corridor_A27_timer')
        "You deactivated the event with [_time_left] seconds to spare..."
    $ pink.otm.end_current_event()

label test_corridor_A27_computer_4:
    $ pink.otm.start_continuing_event()
    if not renpy.store.otm_timer.exists('test_corridor_A27_timer2'):
        "You cannot deactivate the event, no timer is currently running..."
    else:
        $ _time_left = renpy.store.otm_timer.remaining_time('test_corridor_A27_timer')
        $ renpy.store.otm_timer.remove_timed_event('test_corridor_A27_timer')
        "You deactivated the event with [_time_left] seconds to spare..."
    $ pink.otm.end_current_event()
