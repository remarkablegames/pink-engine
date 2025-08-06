default pink_otm_B24_max_time_1 = 10.0
default pink_otm_B24_max_time_2 = 10.0
default pink_otm_B24_max_time_3 = 10.0
default pink_otm_B24_max_time_4 = 10.0
default pink_otm_B24_max_time_5 = 10.0

label test_corridor_B24_sign:
    $ pink.otm.start_continuing_event()
    """
    During pink engine cutscenes, you'll frequently be assigning movement or camera zoom instructions, and then
    waiting for those instructions to be carried out before moving on to the next ren'py line.

    This consists of assigning a sequence of instructions, assigning a set of conditions that are to be waited for,
    and then starting your wait.

    However, what happens if, thanks to some kind of oversight, the conditions which you're waiting for never actually
    occur? Normally, this would cause the game to hang forever, which is quite a problem for your players.

    However, one thing you can do is define a 'max_time' when initiating a wait during an event. If the wait has
    lasted longer than the max period of time, the wait will not only end, but will also teleport characters to their
    destinations, and finish carrying out zooms.

    Stepping on the pink thing in this room triggers an event that will cause a player to walk to the left side of the
    room, have the camera zoom in, walk to the right side of the room, have the camera zoom out, and then walk back.

    That's a total of five waits. Using the computer, you can change the max_time for each individual wait.
    """
    $ pink.otm.end_current_event()

label test_corridor_B24_event:
    $ pink.otm.start_continuing_event()

    # Wait 1: move left
    $ pink.otm.initiate_event_wait(max_time=pink_otm_B24_max_time_1)
    $ pink.otm.add_movement_wait(pink_otm_current_pc, x_coord=2, y_coord=4)
    $ pink_otm_current_pc.control_stack = [pink.otm.ControlCommand("go_to",target=(2, 4))]
    call pink_otm_event_wait

    # Wait 2: zoom camera in
    $ pink.otm.initiate_event_wait(max_time=pink_otm_B24_max_time_2)
    $ pink.otm.add_zoom_wait(2.0)
    $ pink_otm_current_camera.smooth_zoom(2.0, 2.0)
    call pink_otm_event_wait

    # Wait 3: move right
    $ pink.otm.initiate_event_wait(max_time=pink_otm_B24_max_time_3)
    $ pink.otm.add_movement_wait(pink_otm_current_pc, x_coord=22, y_coord=4)
    $ pink_otm_current_pc.control_stack = [pink.otm.ControlCommand("go_to",target=(22, 4))]
    call pink_otm_event_wait

    # Wait 4: zoom camera out
    $ pink.otm.initiate_event_wait(max_time=pink_otm_B24_max_time_4)
    $ pink.otm.add_zoom_wait(1.0)
    $ pink_otm_current_camera.smooth_zoom(1.0, 2.0)
    call pink_otm_event_wait

    # Wait 5: return
    $ pink.otm.initiate_event_wait(max_time=pink_otm_B24_max_time_5)
    $ pink.otm.add_movement_wait(pink_otm_current_pc, x_coord=14, y_coord=4, orientation="up")
    $ pink_otm_current_pc.control_stack = [
        pink.otm.ControlCommand("go_to",target=(14, 4)),
        pink.otm.ControlCommand("turn_up")]
    call pink_otm_event_wait

    $ pink.otm.end_current_event()


label test_corridor_B24_computer:
    $ pink.otm.start_continuing_event()
    menu:
        "Would you like to alter a max time?"

        "Move left: [pink_otm_B24_max_time_1] seconds":
            menu:
                "What should the maximum time for segment 1 be?"

                "0.5 seconds":
                    $ pink_otm_B24_max_time_1 = 0.5
                "2 seconds":
                    $ pink_otm_B24_max_time_1 = 2.0
                "10 seconds":
                    $ pink_otm_B24_max_time_1 = 10.0
                "30 seconds":
                    $ pink_otm_B24_max_time_1 = 30.0
                "Cancel":
                    pass

        "Zoom in: [pink_otm_B24_max_time_2] seconds":
            menu:
                "What should the maximum time for segment 2 be?"

                "0.5 seconds":
                    $ pink_otm_B24_max_time_2 = 0.5
                "2 seconds":
                    $ pink_otm_B24_max_time_2 = 2.0
                "10 seconds":
                    $ pink_otm_B24_max_time_2 = 10.0
                "30 seconds":
                    $ pink_otm_B24_max_time_2 = 30.0
                "Cancel":
                    pass

        "Move right: [pink_otm_B24_max_time_3] seconds":
            menu:
                "What should the maximum time for segment 3 be?"

                "0.5 seconds":
                    $ pink_otm_B24_max_time_3 = 0.5
                "2 seconds":
                    $ pink_otm_B24_max_time_3 = 2.0
                "10 seconds":
                    $ pink_otm_B24_max_time_3 = 10.0
                "30 seconds":
                    $ pink_otm_B24_max_time_3 = 30.0
                "Cancel":
                    pass

        "Zoom out: [pink_otm_B24_max_time_4] seconds":
            menu:
                "What should the maximum time for segment 1 be?"

                "0.5 seconds":
                    $ pink_otm_B24_max_time_4 = 0.5
                "2 seconds":
                    $ pink_otm_B24_max_time_4 = 2.0
                "10 seconds":
                    $ pink_otm_B24_max_time_4 = 10.0
                "30 seconds":
                    $ pink_otm_B24_max_time_4 = 30.0
                "Cancel":
                    pass

        "Move to start: [pink_otm_B24_max_time_5] seconds":
            menu:
                "What should the maximum time for segment 1 be?"

                "0.5 seconds":
                    $ pink_otm_B24_max_time_5 = 0.5
                "2 seconds":
                    $ pink_otm_B24_max_time_5 = 2.0
                "10 seconds":
                    $ pink_otm_B24_max_time_5 = 10.0
                "30 seconds":
                    $ pink_otm_B24_max_time_5 = 30.0
                "Cancel":
                    pass

        "Change all at once":
            menu:
                "What should the maximum time for segment 1 be?"

                "0.5 seconds":
                    $ pink_otm_B24_max_time_1 = 0.5
                    $ pink_otm_B24_max_time_2 = 0.5
                    $ pink_otm_B24_max_time_3 = 0.5
                    $ pink_otm_B24_max_time_4 = 0.5
                    $ pink_otm_B24_max_time_5 = 0.5
                "2 seconds":
                    $ pink_otm_B24_max_time_1 = 2.0
                    $ pink_otm_B24_max_time_2 = 2.0
                    $ pink_otm_B24_max_time_3 = 2.0
                    $ pink_otm_B24_max_time_4 = 2.0
                    $ pink_otm_B24_max_time_5 = 2.0
                "10 seconds":
                    $ pink_otm_B24_max_time_1 = 10.0
                    $ pink_otm_B24_max_time_2 = 10.0
                    $ pink_otm_B24_max_time_3 = 10.0
                    $ pink_otm_B24_max_time_4 = 10.0
                    $ pink_otm_B24_max_time_5 = 10.0
                "30 seconds":
                    $ pink_otm_B24_max_time_1 = 30.0
                    $ pink_otm_B24_max_time_2 = 30.0
                    $ pink_otm_B24_max_time_3 = 30.0
                    $ pink_otm_B24_max_time_4 = 30.0
                    $ pink_otm_B24_max_time_5 = 30.0
                "Cancel":
                    pass

        "Changing nothing":
            pass
    $ pink.otm.end_current_event()