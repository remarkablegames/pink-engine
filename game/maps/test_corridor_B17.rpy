default test_corridor_B17_npc_phase = 1

label test_corridor_B17_npc_1:
    $ pink.otm.start_dynamic_event()
    $ pink.otm.force_instant_transition_on_event_end()
    "Youth" "It is possible to end a pink engine event with a move to a different map."
    "Youth" "Let's try it now."
    $ test_corridor_B17_npc_phase = 2
    $ pink.otm.go_to_map(target_map='test_corridor_B17a.json', x_coord=4, y_coord=4, orientation="left")

label test_corridor_B17_npc_2:
    $ pink.otm.start_dynamic_event()
    "Youth" """One advantage of this is that, when coupled with properly set conditionals and touch events, this allows
    you to chain together events in different maps"""
    $ test_corridor_B17_npc_phase = 3
    $ pink.otm.end_current_event()

label test_corridor_B17_npc_3:
    $ pink.otm.start_dynamic_event()
    menu:
        "Youth" "Would you like to reset this test?"

        "Yes":
            $ test_corridor_B17_npc_phase = 1
        "No":
            $ test_corridor_B17_npc_phase = 3
    $ pink.otm.end_current_event()
