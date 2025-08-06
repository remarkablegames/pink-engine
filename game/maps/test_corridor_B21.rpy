label test_corridor_B21_sign:
    $ pink.otm.start_continuing_event()
    """
    This room exists to tests the relation between parallel processes and events.

    This room has a parallel process, changing the soundtrack based on the area the player is standing in. The white
    areas of the room have their own soundtrack, separate from the rest.

    Interacting with the computers on the right side of the room will start an event in which the player walks
    across the room, crossing the white areas.

    During the event for the upper computer, the parallel process is not paused, meaning the soundtrack switches as
    the player walks through.

    During the event for the lower computer, the parallel process is paused, meaning the soundtrack stays constant.

    Parallel processes are automatically unpaused at the end of any event.
    """
    $ pink.otm.end_current_event()

label test_corridor_B21_computer_01:
    $ pink.otm.start_dynamic_event()

    $ pink.otm.initiate_event_wait()
    $ pink_otm_current_pc.control_stack = [pink.otm.ControlCommand("go_to",target=(1, 6), never_repeat=True)]
    $ pink.otm.add_movement_wait(pink_otm_current_pc, x_coord=1, y_coord=6, finished=True)
    call pink_otm_event_wait

    $ pink.otm.end_current_event()

label test_corridor_B21_computer_02:
    $ pink.otm.start_dynamic_event()
    $ pink_otm_current_map.pause_parallel_processes("sound_play_areas")

    $ pink.otm.initiate_event_wait()
    $ pink_otm_current_pc.control_stack = [pink.otm.ControlCommand("go_to",target=(1, 9), never_repeat=True)]
    $ pink.otm.add_movement_wait(pink_otm_current_pc, x_coord=1, y_coord=9, finished=True)
    call pink_otm_event_wait

    $ pink.otm.end_current_event()