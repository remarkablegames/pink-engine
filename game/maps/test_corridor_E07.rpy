label test_corridor_E07_npc_touch:
    $ pink.otm.start_dynamic_event()
    """You have been caught!"""
    $ pink.otm.force_instant_transition_on_event_end()
    $ pink.otm.go_to_map(target_map='test_corridor_E.json', x_coord=25, y_coord=3, orientation="down")

label test_corridor_E07_sign:
    $ pink.otm.start_continuing_event()
    """This room tests arbitrary code triggers that are used to detect when an NPC has you in his sights.

    In this room, the NPCs see in a full 360 degrees around themselves. The range of their intended view is marked on
    the floor."""
    $ pink.otm.end_current_event()
