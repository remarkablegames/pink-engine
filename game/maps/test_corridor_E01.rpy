label test_corridor_E01_npc_touch:
    $ pink.otm.start_dynamic_event()
    """The minotaur has caught you!"""
    $ pink.otm.force_instant_transition_on_event_end()  # Makes pink engine instantly transition rather than fade.
    $ pink.otm.go_to_map(target_map='test_corridor_E01.json', x_coord=2, y_coord=14, orientation="down")

label test_corridor_E01_teleporter_touch:
    $ pink.otm.start_dynamic_event()
    """You have successfully reached the end of the maze!"""
    $ pink.otm.force_instant_transition_on_event_end()  # Makes pink engine instantly transition rather than fade.
    $ pink.otm.go_to_map(target_map='test_corridor_E01.json', x_coord=2, y_coord=14, orientation="down", transition_in_sound=renpy.store.pink_otm_teleporting_noise)

label test_corridor_E01_sign:
    $ pink.otm.start_continuing_event()
    """This room tests arbitrary code triggers that are used to detect when an NPC has you in his sights.

    Each of the minotaurs in this room can see ten squares ahead in a straight line. Should the player enter that sight,
    the minotaurs will start to pursue them. They are faster than the player, so the player has little hope of escape.

    Try to remain out of sight and reach the purple thingie at the end of the maze."""
    $ pink.otm.end_current_event()