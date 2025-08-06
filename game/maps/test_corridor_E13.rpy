label test_corridor_E13_sign:
    $ pink.otm.start_continuing_event()
    """
    This room further builds on the StartMapEvents functionality demonstrated in room E11 and E12

    In addition to taking conditions, the add_event function also takes priority as an argument. That way, you can
    ensure which event is triggered when conditions for multiple events are met simultaneously.

    The code_on_enter segment for this map is

    StartMapEvents.add_event(event='test_corridor_E13_event1', priority=1)
    StartMapEvents.add_event(event='test_corridor_E13_event2', priority=2)

    test_corridor_E13_event2 exists in the code, but will never be triggered.
    """
    $ pink.otm.end_current_event()

label test_corridor_E13_event1:
    $ pink.otm.start_continuing_event()
    """This is room E13 event 1. Event 2 should never trigger."""
    $ pink.otm.end_current_event()

label test_corridor_E13_event2:
    $ pink.otm.start_continuing_event()
    """This is room E13 event 2. If you see this, the pink productions team has done something wrong."""
    $ pink.otm.end_current_event()
