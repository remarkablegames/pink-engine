label test_corridor_B25_sign:
    $ pink.otm.start_continuing_event()
    """
    Because movement waits by default wait for a control stack to be fully consumed, they can be used in events even
    if the end conditions match the starting positions.

    The most common case of this is spawning a camera somewhere on the map during an event, and then having that camera
    move back to the player's position.
    """
    $ pink.otm.end_current_event()

label test_corridor_B25_event:
    $ pink.otm.start_dynamic_event()

    $ pink_otm_current_camera.spawn_camera_drone()

    $ pink_otm_current_camera.camera_target.set_to_coords(12, 4)
    $ pink_otm_current_camera.camera_target.control_stack = [pink.otm.ControlCommand("go_to",target=(32, 4))]
    $ pink.otm.initiate_event_wait(completion_wait=0.5)
    $ pink.otm.add_movement_wait('pink_otm_camera_drone', x_coord=32, y_coord=4)
    call pink_otm_event_wait
    $ pink_otm_current_camera.recenter_on_player()

    $ pink.otm.end_current_event()