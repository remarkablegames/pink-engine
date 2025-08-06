label test_corridor_C_sign_C01:
    $ pink.otm.start_continuing_event()
    "Room C-01: Map Display - Isometric."
    $ pink.otm.end_current_event()

label test_corridor_C_door_C01:
    $ pink.otm.leave_otm()
    $ renpy.play(test_lab_door_visible_settings['transition_out_delay_sound'], 'audio')
    $ pink.tmd.go_to_map(
        target_map='test_corridor_C01.json', button_text="Return", func=pink.uni.go_to_map, map_type="otm",
        uni_target_map='test_corridor_C.json', x_coord=7, y_coord=3, orientation="down")

label test_corridor_C_sign_C02:
    $ pink.otm.start_continuing_event()
    "Room C-02: Map Display - Staggered."
    $ pink.otm.end_current_event()

label test_corridor_C_door_C02:
    $ pink.otm.leave_otm()
    $ renpy.play(test_lab_door_visible_settings['transition_out_delay_sound'], 'audio')
    $ pink.tmd.go_to_map(
        target_map='test_corridor_C02.json', button_text="Return", func=pink.uni.go_to_map, map_type="otm",
        uni_target_map='test_corridor_C.json', x_coord=10, y_coord=3, orientation="down")

label test_corridor_C_sign_C03:
    $ pink.otm.start_continuing_event()
    "Rooms C-03: Map Display - Hexagonal."
    $ pink.otm.end_current_event()

label test_corridor_C_door_C03:
    $ pink.otm.leave_otm()
    $ renpy.play(test_lab_door_visible_settings['transition_out_delay_sound'], 'audio')
    $ pink.tmd.go_to_map(
        target_map='test_corridor_C03.json', button_text="Return", func=pink.uni.go_to_map, map_type="otm",
        uni_target_map='test_corridor_C.json', x_coord=13, y_coord=3, orientation="down")
