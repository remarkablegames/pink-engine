label test_corridor_E03_npc_touch:
    $ pink.otm.start_dynamic_event()
    """The minotaur has caught you!"""
    $ pink.otm.force_instant_transition_on_event_end()  # Makes pink engine instantly transition rather than fade.
    $ pink.otm.go_to_map(target_map='test_corridor_E03.json', x_coord=8, y_coord=81, orientation="down")

label test_corridor_E03_teleporter_touch:
    $ pink.otm.start_dynamic_event()
    """You have successfully reached the end of the hallway!"""
    $ pink.otm.force_instant_transition_on_event_end()  # Makes pink engine instantly transition rather than fade.
    $ pink.otm.go_to_map(target_map='test_corridor_E03.json', x_coord=8, y_coord=81, orientation="down", transition_in_sound=renpy.store.pink_otm_teleporting_noise)

label test_corridor_E03_sign:
    $ pink.otm.start_continuing_event()
    """This room tests arbitrary code triggers that are used to detect when an NPC has you in his sights.

    Each of the minotaurs in this room can see ten squares ahead in a straight line. Unlike the previous rooms, these
    minotaurs care not for line of sight, and can see through pillars."""
    $ pink.otm.end_current_event()