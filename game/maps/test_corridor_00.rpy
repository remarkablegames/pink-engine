default test_lab_door_visible_settings = {
    'transition_out_delay_sound': 'music/metal_door_01.wav',
    'transition_out': renpy.store.super_quick_fade,
    'transition_in': renpy.store.quick_fade,
    'transition_delay': 0.25}
default test_lab_door_invisible_settings = {
    'transition_in': renpy.store.quick_fade}


label test_corridor_computer1:
    $ pink.otm.start_continuing_event()
    menu:
        "What sprite would you like the player to use?"

        "Punk (default)":
            $ pink_otm_current_pc.switch_sprite_collection("test_player_sprite_collection.json")
        "Star":
            $ pink_otm_current_pc.switch_sprite_collection("test_player_sprite_collection_star.json")
        "Square":
            $ pink_otm_current_pc.switch_sprite_collection("test_player_sprite_collection_square.json")
        "Big Punk":
            $ pink_otm_current_pc.switch_sprite_collection("test_player_sprite_collection_big.json")
    $ pink.otm.end_current_event()

label test_corridor_computer2:
    $ pink.otm.start_continuing_event()
    menu:
        "What would you like your movement speed to be?"

        "0.075":
            $ pink_otm_current_map.change_walk_speed(0.075)
            $ pink_otm_current_map.change_run_speed(0.0375)
        "0.10":
            $ pink_otm_current_map.change_walk_speed(0.10)
            $ pink_otm_current_map.change_run_speed(0.05)
        "0.14 (default)":
            $ pink_otm_current_map.change_walk_speed(0.14)
            $ pink_otm_current_map.change_run_speed(0.07)
        "0.20":
            $ pink_otm_current_map.change_walk_speed(0.20)
            $ pink_otm_current_map.change_run_speed(0.10)
        "0.40":
            $ pink_otm_current_map.change_walk_speed(0.40)
            $ pink_otm_current_map.change_run_speed(0.20)
    $ pink.otm.end_current_event()


label test_corridor_computer3:
    $ pink.otm.start_continuing_event()
    menu:
        "Run Options"

        "Force running" if not pink_otm_force_run:
            $ pink_otm_force_run = True
        "Stop forcing running" if pink_otm_force_run:
            $ pink_otm_force_run = False
        "Disable running" if not pink_otm_forbid_run:
            $ pink_otm_forbid_run = True
        "Enable running" if pink_otm_forbid_run:
            $ pink_otm_forbid_run = False
        "Cancel":
            pass
    $ pink.otm.end_current_event()


label test_corridor_computer4:
    $ pink.otm.start_continuing_event()
    menu:
        "Set map zoom"

        "0.10":
            $ pink_otm_current_camera.set_zoom(0.1)
        "0.5":
            $ pink_otm_current_camera.set_zoom(0.5)
        "1.5 (x), 0.5 (y)":
            $ pink_otm_current_camera.set_y_zoom(0.5)
            $ pink_otm_current_camera.set_x_zoom(1.5)
        "0.9":
            $ pink_otm_current_camera.set_zoom(0.9)
        "1.0 (default)":
            $ pink_otm_current_camera.set_zoom(1.0)
        "1.1":
            $ pink_otm_current_camera.set_zoom(1.1)
        "1.5":
            $ pink_otm_current_camera.set_zoom(1.5)
        "0.5 (x), 1.5 (y)":
            $ pink_otm_current_camera.set_y_zoom(1.5)
            $ pink_otm_current_camera.set_x_zoom(0.5)
        "2.0":
            $ pink_otm_current_camera.set_zoom(2.0)
    $ pink.otm.end_current_event()


label test_corridor_computer5:
    $ pink.otm.start_continuing_event()
    menu:
        "Set movement keys"

        "Arrow keys only":
            $ pink_otm_movement_keys = {
                pygame.K_DOWN: 'down',
                pygame.K_UP: 'up',
                pygame.K_LEFT: 'left',
                pygame.K_RIGHT: 'right'}
            $ pink_otm_current_map.reload_keys()
        "Wasd keys only":
            $ pink_otm_movement_keys = {
                pygame.K_s: 'down',
                pygame.K_w: 'up',
                pygame.K_a: 'left',
                pygame.K_d: 'right'}
            $ pink_otm_current_map.reload_keys()
        "Both":
            $ pink_otm_movement_keys = {
                pygame.K_DOWN: 'down', pygame.K_s: 'down',
                pygame.K_UP: 'up', pygame.K_w: 'up',
                pygame.K_LEFT: 'left', pygame.K_a: 'left',
                pygame.K_RIGHT: 'right', pygame.K_d: 'right'}
            $ pink_otm_current_map.reload_keys()

    $ pink.otm.end_current_event()


label test_corridor_computer6:
    $ pink.otm.start_continuing_event()
    menu:
        "Set interaction key"

        "No mouse":
            $ pink_otm_key_down_functions = {
                pygame.K_SPACE: pink.otm.OrthogonalTiledMap.player_interaction,
                pygame.K_RETURN: pink.otm.OrthogonalTiledMap.player_interaction,
                pygame.K_RSHIFT: pink.otm.OrthogonalTiledMap.run_key_down,
                pygame.K_LSHIFT: pink.otm.OrthogonalTiledMap.run_key_down}
            $ pink_otm_mouse_button_down_functions = {}
            $ pink_otm_current_map.reload_keys()
        "Mouse only":
            $ pink_otm_key_down_functions = {
                pygame.K_RSHIFT: pink.otm.OrthogonalTiledMap.run_key_down,
                pygame.K_LSHIFT: pink.otm.OrthogonalTiledMap.run_key_down}
            $ pink_otm_mouse_button_down_functions = {
                1: pink.otm.OrthogonalTiledMap.player_interaction}
            $ pink_otm_current_map.reload_keys()
        "Both":
            $ pink_otm_key_down_functions = {
                pygame.K_SPACE: pink.otm.OrthogonalTiledMap.player_interaction,
                pygame.K_RETURN: pink.otm.OrthogonalTiledMap.player_interaction,
                pygame.K_RSHIFT: pink.otm.OrthogonalTiledMap.run_key_down,
                pygame.K_LSHIFT: pink.otm.OrthogonalTiledMap.run_key_down}
            $ pink_otm_mouse_button_down_functions = {
                1: pink.otm.OrthogonalTiledMap.player_interaction}
            $ pink_otm_current_map.reload_keys()
    $ pink.otm.end_current_event()


label test_corridor_computer7:
    $ pink.otm.start_continuing_event()
    menu:
        "Autocenter sprites"

        "Disable" if pink_otm_autocenter_sprites:
            $ pink_otm_autocenter_sprites = False
        "Enable" if not pink_otm_autocenter_sprites:
            $ pink_otm_autocenter_sprites = True
        "Cancel":
            $ pass
    $ pink.otm.end_current_event()


label test_corridor_computer8:
    $ pink.otm.start_continuing_event()
    menu:
        "Viewport"

        "Default":
            $ pink_otm_default_viewport_x_offset = 0
            $ pink_otm_default_viewport_y_offset = 0
            $ pink_otm_default_viewport_width = config.screen_width
            $ pink_otm_default_viewport_height = config.screen_height
            $ pink_otm_current_camera.center_on_target()
            $ renpy.restart_interaction()
        "100, 100, 600, 600":
            $ pink_otm_default_viewport_x_offset = 100
            $ pink_otm_default_viewport_y_offset = 100
            $ pink_otm_default_viewport_width = 600
            $ pink_otm_default_viewport_height = 600
            $ pink_otm_current_camera.center_on_target()
            $ renpy.restart_interaction()
        "Cancel":
            $ pass
    $ pink.otm.end_current_event()


label test_corridor_elevator:
    $ pink.otm.start_continuing_event()
    $ renpy.play(test_lab_door_visible_settings['transition_out_delay_sound'], 'audio')
    menu:
        "Select floor"

        "Floor A":
            $ pink.otm.force_instant_transition_on_event_end()
            $ pink.otm.go_to_map(target_map='test_corridor_A.json', x_coord=2, y_coord=3, orientation="down")
        "Floor B":
            $ pink.otm.force_instant_transition_on_event_end()
            $ pink.otm.go_to_map(target_map='test_corridor_B.json', x_coord=2, y_coord=3, orientation="down")
        "Floor C":
            $ pink.otm.force_instant_transition_on_event_end()
            $ pink.otm.go_to_map(target_map='test_corridor_C.json', x_coord=2, y_coord=3, orientation="down")
        "Floor E":
            $ pink.otm.force_instant_transition_on_event_end()
            $ pink.otm.go_to_map(target_map='test_corridor_E.json', x_coord=2, y_coord=3, orientation="down")
        "Artist Gallery":
            $ pink.otm.force_instant_transition_on_event_end()
            $ pink.otm.go_to_map(target_map='artist_corridor_main.json', x_coord=2, y_coord=3, orientation="down")

