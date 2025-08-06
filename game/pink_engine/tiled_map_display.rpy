init python:
    config.per_frame_screens.append('pink_tmd_map')

label pink_tmd_call_map(func, *args, **kwargs):
    scene black

    python:
        # Blocks rollback while on a pink engine map.
        if config.rollback_enabled:
            pink_otm_rollback_restore = True
        else:
            pink_otm_rollback_restore = False

        config.rollback_enabled = False
        # if pink_tmd_current_camera is None:
        pink_tmd_current_map.game_tick(0)

    call screen pink_tmd_map(func, *args, **kwargs)

transform pink_tmd_size_offset(screen_width, screen_height, xzoom, yzoom):
    # Centers small screens
    xoffset max(int((screen_width - (pink_tmd_current_map.image_size.x * xzoom)) / 2), 0)
    yoffset max(int((screen_height - (pink_tmd_current_map.image_size.y * yzoom)) / 2), 0)

screen pink_tmd_map(button_func, *args, button_text="Continue", **kwargs):
    layer "master"

    $ map_camera = pink_tmd_current_map.camera
    $ displayable = pink_tmd_current_map.get_displayable()

    viewport:
        xadjustment map_camera.x
        yadjustment map_camera.y
        draggable True

        at pink_tmd_size_offset(config.screen_width, config.screen_height, map_camera.xzoom, map_camera.yzoom)
        id "map_viewport"
        area (0, 0, config.screen_width, config.screen_height)

        fixed:
            xsize pink_tmd_current_map.image_size.x
            ysize pink_tmd_current_map.image_size.y
            at pink_otm_map_zoom(map_camera.xzoom, map_camera.yzoom)
            add displayable

    add pink_tmd_current_map

    textbutton button_text action [Hide('pink_tmd_map'), Function(button_func, *args, **kwargs)]
