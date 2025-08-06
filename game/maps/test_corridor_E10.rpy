label test_corridor_E10_sign:
    $ pink.otm.start_continuing_event()
    """This room tests arbitrary event triggers that are initiated on entering a map.

    This room is a copy of test room E08, except the conditional code trigger is initialized in the map properties,
    rather than through a map object.

    It should function identically from the perspective of a player."""
    $ pink.otm.end_current_event()

label test_corridor_E10_run:
    $ pink.otm.start_dynamic_event()
    """This very annoying event is triggered whenever you try to run in this room."""
    $ pink.otm.end_dynamic_event()