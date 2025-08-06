default test_corridor_E06_npc_triggered = False

label test_corridor_E06_npc:
    $ pink.otm.start_continuing_event()

    $ pink.otm.initiate_event_wait()
    $ pink.otm.add_movement_wait(pink_otm_current_pc, finished=True)
    call pink_otm_event_wait

    $ pink_otm_walk_up_to_character(test_corridor_E06_npc, pink_otm_current_pc)
    $ pink.otm.initiate_event_wait()
    $ pink.otm.add_movement_wait(test_corridor_E06_npc, finished=True)
    call pink_otm_event_wait

    if not test_corridor_E06_npc_triggered:
        "Minotaur" "Foolish human! I am the Greatly Besighted Minotaur, capable of looking in cones, rather than mere lines!"
    else:
        "Greatly Besighted Minotaur" "Neat, eh?"
    $ test_corridor_E06_npc_triggered = True
    $ pink.otm.end_current_event()

label test_corridor_E06_sign_01:
    $ pink.otm.start_continuing_event()
    """This room tests arbitrary code triggers that are used to detect when an NPC has you in his sights.

    Unlike the NPCs in room E04, the minotaur in this room has cone-based sight, rather than line-based sight."""
    $ pink.otm.end_current_event()

label test_corridor_E06_sign_02:
    $ pink.otm.start_continuing_event()
    """Beware His gaze..."""
    $ pink.otm.end_current_event()