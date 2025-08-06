init python:

    # To restore to default ren'py keymapping, comment out the line.
    # Keyboard
    config.keymap['screenshot'] = [ 'alt_shift_K_s' ]
    config.keymap['inspector'] = [ 'alt_K_i' ]
    config.keymap['developer'] = [ 'alt_shift_K_d' ]
    config.keymap['director'] = [ 'alt_ctrl_K_d' ]
    config.keymap['accessibility'] = [ 'alt_shift_K_a' ]
    config.keymap['focus_left'] = [ 'alt_K_LEFT', 'repeat_alt_K_LEFT' ]
    config.keymap['focus_right'] = [ 'alt_K_RIGHT', 'repeat_alt_K_RIGHT' ]
    config.keymap['focus_up'] = [ 'alt_K_UP', 'repeat_alt_K_UP' ]
    config.keymap['focus_down'] = [ 'alt_K_DOWN', 'repeat_alt_K_DOWN' ]

    # Gamepad
    config.pad_bindings['pad_leftx_neg'] = [ "bar_left", "viewport_leftarrow" ]
    config.pad_bindings['repeat_pad_leftx_neg'] = [ "bar_left", "viewport_leftarrow" ]
    config.pad_bindings['pad_rightx_neg'] = [ "bar_left", "viewport_leftarrow" ]
    config.pad_bindings['repeat_pad_rightx_neg'] = [ "bar_left", "viewport_leftarrow" ]

    config.pad_bindings['pad_leftx_pos'] = [ "bar_right", "viewport_rightarrow" ]
    config.pad_bindings['repeat_pad_leftx_pos'] = [ "bar_right", "viewport_rightarrow" ]
    config.pad_bindings['pad_rightx_pos'] = [ "bar_right", "viewport_rightarrow" ]
    config.pad_bindings['repeat_pad_rightx_pos'] = [ "bar_right", "viewport_rightarrow" ]

    config.pad_bindings['pad_lefty_neg'] = [ "bar_up", "viewport_uparrow" ]
    config.pad_bindings['repeat_pad_lefty_neg'] = [ "bar_up", "viewport_uparrow" ]
    config.pad_bindings['pad_righty_neg'] = [ "bar_up", "viewport_uparrow" ]
    config.pad_bindings['repeat_pad_righty_neg'] = [ "bar_up", "viewport_uparrow" ]

    config.pad_bindings['pad_lefty_pos'] = [ "bar_down", "viewport_downarrow" ]
    config.pad_bindings['repeat_pad_lefty_pos'] = [ "bar_down", "viewport_downarrow" ]
    config.pad_bindings['pad_righty_pos'] = [ "bar_down", "viewport_downarrow" ]
    config.pad_bindings['repeat_pad_righty_pos'] = [ "bar_down", "viewport_downarrow" ]
