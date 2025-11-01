transform pink_otm_size_offset(screen_width, screen_height, image_size_x, image_size_y, xzoom, yzoom, screen_x_offset, screen_y_offset, shake_x, shake_y):
    # Centers small screens
    xoffset max(int((screen_width - (image_size_x * xzoom)) / 2), screen_x_offset) + shake_x
    yoffset max(int((screen_height - (image_size_y * yzoom)) / 2), screen_y_offset) + shake_y

transform pink_otm_map_zoom(xzoom, yzoom):
    xzoom xzoom
    yzoom yzoom

label pink_otm_call_map:
    scene black

    python:
        # Blocks rollback while on a pink engine map.
        if config.rollback_enabled:
            pink_otm_rollback_restore = True
        else:
            pink_otm_rollback_restore = False

        # Restores config.window_hide_transition to cached value if set.
        if pink_otm_window_hide_cache is not None:
            config.window_hide_transition = pink_otm_window_hide_cache
            pink_otm_window_hide_cache = None

        # Sets config.autosave_on_choice to pink_otm value, caches the original (original is restored on leave_otm)
        if pink_otm_autosave_on_choice_cache is None:
            pink_otm_autosave_on_choice_cache = config.autosave_on_choice
            config.autosave_on_choice = pink_otm_autosave_on_choice

        pink_otm_current_camera = pink_otm_current_map.camera
        pink_otm_current_camera.camera_map_refresh()

        if pink_otm_current_map.x_zoom is not None and pink_otm_current_map.x_zoom != pink_otm_camera_current_xzoom:
            pink_otm_current_camera.set_x_zoom(pink_otm_current_map.x_zoom)

        if pink_otm_current_map.y_zoom is not None and pink_otm_current_map.y_zoom  != pink_otm_camera_current_yzoom:
            pink_otm_current_camera.set_y_zoom(pink_otm_current_map.y_zoom)

        config.rollback_enabled = False

        _temp_sound = pink_map_transition_in_sound
        _temp_transition = pink_map_transition_in
        pink_map_transition_in_sound = None
        pink_map_transition_in = None
        if _temp_sound is not None:
            renpy.play(_temp_sound)

    call screen pink_otm_map with _temp_transition

screen pink_otm_map():
    layer "master"

    $ map_camera = pink_otm_current_map.camera
    $ displayable = pink_otm_current_map.get_displayable()
    $ overlay_manager = pink_otm_current_map.get_overlay_manager()
    if pink_otm_current_event_type is None:
        $ pink_otm_current_map.check_held_keys()

    viewport:
        xadjustment map_camera.x
        yadjustment map_camera.y

        at pink_otm_size_offset(
            config.screen_width, config.screen_height, pink_otm_current_map.image_size.x,
            pink_otm_current_map.image_size.y, map_camera.xzoom, map_camera.yzoom, map_camera.viewport_x_offset,
            map_camera.viewport_y_offset, overlay_manager.shake_x, overlay_manager.shake_y)
        id "map_viewport"
        area (0, 0, map_camera.viewport_width, map_camera.viewport_height)

        fixed:
            xsize pink_otm_current_map.image_size.x
            ysize pink_otm_current_map.image_size.y
            at pink_otm_map_zoom(map_camera.xzoom, map_camera.yzoom)
            add displayable nearest pink_otm_nearest

    add overlay_manager
    add pink_otm_current_map
