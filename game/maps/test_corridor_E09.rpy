label test_corridor_E09_npc_touch:
    $ pink.otm.start_dynamic_event()
    """You have been caught!"""
    $ pink.otm.force_instant_transition_on_event_end()
    $ pink.otm.go_to_map(target_map='test_corridor_E.json', x_coord=31, y_coord=3, orientation="down")

label test_corridor_E09_sign:
    $ pink.otm.start_continuing_event()
    """This room tests the disengage_range function for the pursuit script. The minotaur should stop chasing you and
    return to origin if you manage to get more than six squares away."""
    $ pink.otm.end_current_event()
