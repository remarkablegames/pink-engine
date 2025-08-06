label test_corridor_A16_sign:
    $ pink.otm.start_continuing_event()
    """
    This room tests various camera functions. Stepping on a pink thing will trigger a camera function.

    The leftmost pink thing spawns a camera drone and assigns it vertical movements.

    The central pink thing spawns a camera drone and assigns it horizontal movements.

    The rightmost pink thing spawns a camera drone and makes it move around the room using both vertical and
    horizontal movements.

    The topmost pink thing makes the camera zoom in.

    The bottom-most pink thing makes the camera zoom out
    """
    $ pink.otm.end_current_event()

label test_corridor_A16_camera_test1:
    $ pink.otm.start_dynamic_event()

    $ pink_otm_current_camera.spawn_camera_drone()

    # Up
    $ pink.otm.initiate_event_wait(completion_wait=0.5)
    $ pink_otm_current_camera.camera_target.control_stack = [pink.otm.ControlCommand("go_to",target=(4, 4))]
    $ pink.otm.add_movement_wait('pink_otm_camera_drone')
    call pink_otm_event_wait

    # Down
    $ pink.otm.initiate_event_wait(completion_wait=0.5)
    $ pink_otm_current_camera.camera_target.control_stack = [pink.otm.ControlCommand("go_to",target=(4, 14))]
    $ pink.otm.add_movement_wait('pink_otm_camera_drone')
    call pink_otm_event_wait

    # Return to starting position
    $ pink.otm.initiate_event_wait()
    $ pink_otm_current_camera.camera_target.control_stack = [pink.otm.ControlCommand("go_to",target=(4, 8))]
    $ pink.otm.add_movement_wait('pink_otm_camera_drone')
    call pink_otm_event_wait

    # Restore player camera
    $ pink_otm_current_camera.recenter_on_player()

    $ pink.otm.end_current_event()

label test_corridor_A16_camera_test2:
    $ pink.otm.start_dynamic_event()

    $ pink_otm_current_camera.spawn_camera_drone()

    # Left
    $ pink.otm.initiate_event_wait(completion_wait=0.5)
    $ pink_otm_current_camera.camera_target.control_stack = [pink.otm.ControlCommand("go_to",target=(8, 8))]
    $ pink.otm.add_movement_wait('pink_otm_camera_drone')
    call pink_otm_event_wait

    # Right
    $ pink.otm.initiate_event_wait(completion_wait=0.5)
    $ pink_otm_current_camera.camera_target.control_stack = [pink.otm.ControlCommand("go_to",target=(18, 8))]
    $ pink.otm.add_movement_wait('pink_otm_camera_drone')
    call pink_otm_event_wait

    # Return to starting position
    $ pink.otm.initiate_event_wait()
    $ pink_otm_current_camera.camera_target.control_stack = [pink.otm.ControlCommand("go_to",target=(13, 8))]
    $ pink.otm.add_movement_wait('pink_otm_camera_drone')
    call pink_otm_event_wait

    # Restore player camera
    $ pink_otm_current_camera.recenter_on_player()

    $ pink.otm.end_current_event()

label test_corridor_A16_camera_test3:
    $ pink.otm.start_dynamic_event()

    $ pink_otm_current_camera.spawn_camera_drone()

    # Top-right
    $ pink.otm.initiate_event_wait(completion_wait=0.5)
    $ pink_otm_current_camera.camera_target.control_stack = [pink.otm.ControlCommand("go_to",target=(22, 4))]
    $ pink.otm.add_movement_wait('pink_otm_camera_drone')
    call pink_otm_event_wait

    # Top-left
    $ pink.otm.initiate_event_wait(completion_wait=0.5)
    $ pink_otm_current_camera.camera_target.control_stack = [pink.otm.ControlCommand("go_to",target=(4, 4))]
    $ pink.otm.add_movement_wait('pink_otm_camera_drone')
    call pink_otm_event_wait

    # Bottom-left
    $ pink.otm.initiate_event_wait(completion_wait=0.5)
    $ pink_otm_current_camera.camera_target.control_stack = [pink.otm.ControlCommand("go_to",target=(4, 14))]
    $ pink.otm.add_movement_wait('pink_otm_camera_drone')
    call pink_otm_event_wait

    # Bottom-right
    $ pink.otm.initiate_event_wait(completion_wait=0.5)
    $ pink_otm_current_camera.camera_target.control_stack = [pink.otm.ControlCommand("go_to",target=(22, 14))]
    $ pink.otm.add_movement_wait('pink_otm_camera_drone')
    call pink_otm_event_wait

    # Return to starting position
    $ pink.otm.initiate_event_wait()
    $ pink_otm_current_camera.camera_target.control_stack = [pink.otm.ControlCommand("go_to",target=(22, 8))]
    $ pink.otm.add_movement_wait('pink_otm_camera_drone')
    call pink_otm_event_wait

    # Restore player camera
    $ pink_otm_current_camera.recenter_on_player()

    $ pink.otm.end_current_event()

label test_corridor_A16_camera_test4:
    $ pink.otm.start_dynamic_event()

    # Zoom out
    $ pink.otm.initiate_event_wait(completion_wait=0.5)
    $ pink_otm_current_camera.smooth_zoom(0.5, 2.0)
    $ pink.otm.add_zoom_wait()
    call pink_otm_event_wait

    # Zoom in
    $ pink.otm.initiate_event_wait(completion_wait=0.5)
    $ pink_otm_current_camera.smooth_zoom(1.0, 2.0)
    $ pink.otm.add_zoom_wait()
    call pink_otm_event_wait

    $ pink.otm.end_current_event()

label test_corridor_A16_camera_test5:
    $ pink.otm.start_dynamic_event()

    # Zoom in
    $ pink.otm.initiate_event_wait(completion_wait=0.5)
    $ pink_otm_current_camera.smooth_zoom(2.0, 2.0)
    $ pink.otm.add_zoom_wait()
    call pink_otm_event_wait

    # Zoom out
    $ pink.otm.initiate_event_wait(completion_wait=0.5)
    $ pink_otm_current_camera.smooth_zoom(1.0, 2.0)
    $ pink.otm.add_zoom_wait()
    call pink_otm_event_wait

    $ pink.otm.end_current_event()
