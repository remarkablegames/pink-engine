default test_corridor_E12_start_event = 0

label test_corridor_E12_sign:
    $ pink.otm.start_continuing_event()
    """
    This room further builds on the StartMapEvents functionality demonstrated in room E11.

    It is possible to specify a specific condition for an event to be triggered on map start. For example, this map has
    the following code_on_enter property set:

    StartMapEvents.add_event(event='test_corridor_E12_event1', condition='renpy.store.test_corridor_E12_start_event == 1')
    StartMapEvents.add_event(event='test_corridor_E12_event2', condition='renpy.store.test_corridor_E12_start_event == 2')

    The value of test_corridor_E12_start_event is set to 0 by default, and is altered by interacting with the computer.
    The triggered events set the value to 0 again, to prevent it from retriggering until reset.
    """
    $ pink.otm.end_current_event()

label test_corridor_E12_event1:
    $ pink.otm.start_continuing_event()
    """You have chosen to trigger event 1 on entering this room."""
    $ test_corridor_E12_start_event = 0
    $ pink.otm.end_current_event()

label test_corridor_E12_event2:
    $ pink.otm.start_continuing_event()
    """You have chosen to trigger event 2 on entering this room."""
    $ test_corridor_E12_start_event = 0
    $ pink.otm.end_current_event()

label test_corridor_E12_computer:
    $ pink.otm.start_continuing_event()
    menu:
        "Which event should trigger upon entering room E12?"

        "Event 1":
            $ test_corridor_E12_start_event = 1
        "Event 2":
            $ test_corridor_E12_start_event = 2
        "No Event":
            $ test_corridor_E12_start_event = 0
    $ pink.otm.end_current_event()