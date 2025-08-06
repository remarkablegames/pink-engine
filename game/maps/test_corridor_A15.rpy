label test_corridor_A15_sign:
    $ pink.otm.start_continuing_event()
    """This room tests the ability to change the camera's focus. Interacting with the NPC in this room will make the
    camera follow them, rather than the player. The PC will still answer to keyboard inputs.

    Leaving the room will reset the camera's focus to follow the player.
    """
    $ pink.otm.end_current_event()


label test_corridor_A15_npc:
    $ pink.otm.start_continuing_event(interaction_reaction=False)
    $ pink_otm_current_camera.switch_target(test_corridor_A15_youth)
    $ pink.otm.end_current_event()
