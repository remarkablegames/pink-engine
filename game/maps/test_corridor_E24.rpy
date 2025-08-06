label test_corridor_E24_sign:
    $ pink.otm.start_continuing_event()
    """As of version 0.17, the pink engine supports locational sounds. That is, sounds that scale and pan based on
    the player's location compared to the emitting object.

    In this room, it is the computer object that is the sound emitted, constantly repeating a single sound through the
    'emits_sound' property, which causes an object to emit a constantly looping sound.

    You can interact with this object to alter all properties related to emanating sounds, allowing you to experiment
    with the settings.

    You can enable and disable locational panning and scaling. You can adjust the maximum and minimum volume, the
    distance at which the maximum and minimum volume are reached, the maximum pan and the range for full panning and no
    panning.
    """
    $ pink.otm.end_current_event()

label test_corridor_E24_computer:
    $ pink.otm.start_continuing_event()
    call test_corridor_E24_main_menu
    $ pink.otm.go_to_map(target_map='test_corridor_E24.json', x_coord=16, y_coord=17, orientation="up")

label test_corridor_E24_main_menu:
    menu:
        "Alter variables"

        "Return (refreshes map)":
            return
        "Enable sound scaling (currently [E24_computer.emits_sound_scale])":
            jump test_corridor_E24_menu_scale_volume
        "Minimum Volume (currently [E24_computer.emits_sound_min_volume])" if E24_computer.emits_sound_scale:
            jump test_corridor_E24_menu_min_volume
        "Maximum Volume (currently [E24_computer.emits_sound_max_volume])" if E24_computer.emits_sound_scale:
            jump test_corridor_E24_menu_max_volume
        "Range for min volume (currently [E24_computer.emits_sound_min_volume_distance])" if E24_computer.emits_sound_scale:
            jump test_corridor_E24_menu_range_for_no_volume
        "Range for max volume (currently [E24_computer.emits_sound_max_volume_distance])" if E24_computer.emits_sound_scale:
            jump test_corridor_E24_menu_range_for_full_volume
        "Enable sound panning (currently [E24_computer.emits_sound_pan])":
            jump test_corridor_E24_menu_pan_sound
        "Max Pan (currently [E24_computer.emits_sound_max_pan])" if E24_computer.emits_sound_pan:
            jump test_corridor_E24_menu_max_pan
        "Range for full pan (currently [E24_computer.emits_sound_max_pan_distance])" if E24_computer.emits_sound_pan:
            jump test_corridor_E24_menu_range_for_full_pan
        "Range for no pan (currently [E24_computer.emits_sound_no_pan_distance])" if E24_computer.emits_sound_pan:
            jump test_corridor_E24_menu_range_for_no_pan

label test_corridor_E24_menu_scale_volume:
    menu:
        "What should the value be?"

        "True (default)":
            $ E24_computer.properties['emits_sound_scale'] = True
        "False":
            $ E24_computer.properties['emits_sound_scale'] = False

    jump test_corridor_E24_main_menu

label test_corridor_E24_menu_min_volume:
    menu:
        "What should the value be?"

        "0.0 (default)":
            $ E24_computer.properties['emits_sound_min_volume'] = 0.0
        "0.1" if E24_computer.emits_sound_max_volume > 0.1:
            $ E24_computer.properties['emits_sound_min_volume'] = 0.1
        "0.25" if E24_computer.emits_sound_max_volume > 0.25:
            $ E24_computer.properties['emits_sound_min_volume'] = 0.25
        "0.5" if E24_computer.emits_sound_max_volume > 0.5:
            $ E24_computer.properties['emits_sound_min_volume'] = 0.5
        "0.75" if E24_computer.emits_sound_max_volume > 0.75:
            $ E24_computer.properties['emits_sound_min_volume'] = 0.75
        "0.9" if E24_computer.emits_sound_max_volume > 0.9:
            $ E24_computer.properties['emits_sound_min_volume'] = 0.9

    jump test_corridor_E24_main_menu

label test_corridor_E24_menu_max_volume:
    menu:
        "What should the value be?"

        "0.1" if E24_computer.emits_sound_min_volume < 0.1:
            $ E24_computer.properties['emits_sound_max_volume'] = 0.1
        "0.25" if E24_computer.emits_sound_min_volume < 0.25:
            $ E24_computer.properties['emits_sound_max_volume'] = 0.25
        "0.5" if E24_computer.emits_sound_min_volume < 0.5:
            $ E24_computer.properties['emits_sound_max_volume'] = 0.5
        "0.75" if E24_computer.emits_sound_min_volume < 0.75:
            $ E24_computer.properties['emits_sound_max_volume'] = 0.75
        "0.9" if E24_computer.emits_sound_min_volume < 0.9:
            $ E24_computer.properties['emits_sound_max_volume'] = 0.9
        "1.0 (default)":
            $ E24_computer.properties['emits_sound_max_volume'] = 1.0

    jump test_corridor_E24_main_menu

label test_corridor_E24_menu_range_for_no_volume:
    menu:
        "What should the value be?"

        "3" if E24_computer.emits_sound_max_volume_distance < 3:
            $ E24_computer.properties['emits_sound_min_volume_distance'] = 3
        "10" if E24_computer.emits_sound_max_volume_distance < 10:
            $ E24_computer.properties['emits_sound_min_volume_distance'] = 10
        "15" if E24_computer.emits_sound_max_volume_distance < 15:
            $ E24_computer.properties['emits_sound_max_volume_distance'] = 15
        "20" if E24_computer.emits_sound_max_volume_distance < 20:
            $ E24_computer.properties['emits_sound_min_volume_distance'] = 20
        "25" if E24_computer.emits_sound_max_volume_distance < 25:
            $ E24_computer.properties['emits_sound_min_volume_distance'] = 25
        "[pink_otm_default_min_volume_distance] (default)":
            $ E24_computer.properties['emits_sound_min_volume_distance'] = pink_otm_default_min_volume_distance

    jump test_corridor_E24_main_menu

label test_corridor_E24_menu_range_for_full_volume:
    menu:
        "What should the value be?"

        "1 (default)":
            $ E24_computer.properties['emits_sound_max_volume_distance'] = 1
        "3" if E24_computer.emits_sound_min_volume_distance > 3:
            $ E24_computer.properties['emits_sound_max_volume_distance'] = 3
        "10" if E24_computer.emits_sound_min_volume_distance > 10:
            $ E24_computer.properties['emits_sound_max_volume_distance'] = 10
        "15" if E24_computer.emits_sound_min_volume_distance > 15:
            $ E24_computer.properties['emits_sound_max_volume_distance'] = 15
        "20" if E24_computer.emits_sound_min_volume_distance > 20:
            $ E24_computer.properties['emits_sound_max_volume_distance'] = 20
        "25" if E24_computer.emits_sound_min_volume_distance > 25:
            $ E24_computer.properties['emits_sound_max_volume_distance'] = 25

    jump test_corridor_E24_main_menu

label test_corridor_E24_menu_pan_sound:
    menu:
        "What should the value be?"

        "True (default)":
            $ E24_computer.properties['emits_sound_pan'] = True
        "False":
            $ E24_computer.properties['emits_sound_pan'] = False

    jump test_corridor_E24_main_menu

label test_corridor_E24_menu_max_pan:
    menu:
        "What should the value be?"

        "0.1":
            $ E24_computer.properties['emits_sound_max_pan'] = 0.1
        "0.25":
            $ E24_computer.properties['emits_sound_max_pan'] = 0.25
        "0.5":
            $ E24_computer.properties['emits_sound_max_pan'] = 0.5
        "0.75":
            $ E24_computer.properties['emits_sound_max_pan'] = 0.75
        "0.9":
            $ E24_computer.properties['emits_sound_max_pan'] = 0.9
        "1.0 (default)":
            $ E24_computer.properties['emits_sound_max_pan'] = 1.0

    jump test_corridor_E24_main_menu

label test_corridor_E24_menu_range_for_full_pan:
    menu:
        "What should the value be?"

        "3" if E24_computer.emits_sound_no_pan_distance < 3:
            $ E24_computer.properties['emits_sound_max_pan_distance'] = 3
        "10" if E24_computer.emits_sound_no_pan_distance < 10:
            $ E24_computer.properties['emits_sound_max_pan_distance'] = 10
        "15" if E24_computer.emits_sound_no_pan_distance < 15:
            $ E24_computer.properties['emits_sound_max_pan_distance'] = 15
        "[pink_otm_default_max_pan_distance] (default)":
            $ E24_computer.properties['emits_sound_max_pan_distance'] = pink_otm_default_max_pan_distance

    jump test_corridor_E24_main_menu

label test_corridor_E24_menu_range_for_no_pan:
    menu:
        "What should the value be?"

        "0 (default)":
            $ E24_computer.properties['emits_sound_no_pan_distance'] = 0
        "3" if E24_computer.emits_sound_max_pan_distance > 3:
            $ E24_computer.properties['emits_sound_no_pan_distance'] = 3
        "10" if E24_computer.emits_sound_max_pan_distance > 10:
            $ E24_computer.properties['emits_sound_no_pan_distance'] = 10
        "15" if E24_computer.emits_sound_max_pan_distance > 15:
            $ E24_computer.properties['emits_sound_no_pan_distance'] = 15

    jump test_corridor_E24_main_menu

