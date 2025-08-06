default test_corridor_A14_cutscene_active = True

label test_corridor_A14_sign:
    $ pink.otm.start_continuing_event()
    """This room plays a single cutscene. To reset the cutscene, interact with the central NPC.
    """
    $ pink.otm.end_current_event()

label test_corridor_A14_npc:
    $ pink.otm.start_dynamic_event()
    menu:
        "Adventurer" "Would you like to reset the cutscene?"

        "Yes":
            $ test_corridor_A14_cutscene_active = True
        "No":
            $ test_corridor_A14_cutscene_active = False

    $ pink.otm.end_dynamic_event()

label test_corridor_A14_cutscene:
    $ pink.otm.start_dynamic_event()
    $ test_corridor_A14_cutscene_active = False

    # Example of how to implement a wait in a cutscene
    # Initiate mid-event wait
    $ pink.otm.initiate_event_wait()

    # Assign movement instructions
    $ test_corridor_room14_mino1.control_stack = [
        pink.otm.ControlCommand("go_to",target=(3, 7), never_repeat=True),
        pink.otm.ControlCommand("turn_right", never_repeat=True)]
    $ test_corridor_room14_mino2.control_stack = [
        pink.otm.ControlCommand("go_to",target=(7, 7), never_repeat=True),
        pink.otm.ControlCommand("turn_left", never_repeat=True)]
    $ pink_otm_current_pc.control_stack = [
        pink.otm.ControlCommand("go_to",target=(5, 7), never_repeat=True),
        pink.otm.ControlCommand("turn_up", never_repeat=True)]

    # Define the conditions for the wait to end
    $ pink.otm.add_movement_wait(test_corridor_room14_mino1)
    $ pink.otm.add_movement_wait(test_corridor_room14_mino2)
    $ pink.otm.add_movement_wait(pink_otm_current_pc)

    # Start the wait
    call pink_otm_event_wait

    "Adventurer" """Well, well, well, look what the cat dragged in. If it isn't our old friend, Unnamed Protagonist?

    Trying to find some puzzles? Some adventures? The slightest hint of entertainment?

    Foolish girl! This is merely a tech demo! There is no entertainment to be had!"""
    $ pink.otm.end_dynamic_event()
