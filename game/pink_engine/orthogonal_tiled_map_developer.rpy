label pink_otm_developer_start:
    $ pink.otm.leave_otm()
    call screen pink_developer

label pink_otm_developer_stop:
    $ pink.otm.return_to_otm()

screen pink_developer():
    vbox:
        text "Press shift+O again to enter the regular console." size pink_console_text_size
        textbutton "Orthogonal Tiled Maps settings" text_size pink_console_text_size action [Hide("pink_developer"), Show("pink_otm_developer")]
        textbutton "Orthogonal Tiled Maps" text_size pink_console_text_size action [Hide("pink_developer"), Show("pink_otm_developer_maps")]
        textbutton "Tilesets" text_size pink_console_text_size action [Hide("pink_developer"), Show("pink_developer_tilesets")]
        textbutton "Sprite Collections" text_size pink_console_text_size action [Hide("pink_developer"), Show("pink_developer_sprites")]
        textbutton "Return" text_size pink_console_text_size action Jump("pink_otm_developer_stop")

    key "game_menu" action Jump("pink_otm_developer_stop")


screen pink_otm_developer():
    frame:
        xfill True
        yfill True
        background "#000000"

        hbox:
            frame:
                has vpgrid:
                    cols 1
                    yfill True
                    mousewheel True
                    scrollbars 'vertical'
                    spacing 1

                vbox:
                    xsize 200
                    textbutton "back" text_size pink_console_text_size action [Hide("pink_otm_developer"), Show("pink_developer")]

            frame:
                has vpgrid:
                    cols 1
                    xfill True
                    yfill True
                    mousewheel True
                    scrollbars 'vertical'
                    spacing 1

                vbox:
                    hbox:
                        $ walk_speed_string = '{:5.2f}'.format(pink_otm_current_walk_speed)
                        text "Player walk speed: [walk_speed_string] " size pink_console_text_size
                        textbutton "+" text_size pink_console_text_size xpadding 0 ypadding 0 action SetVariable('pink_otm_current_walk_speed', pink_otm_current_walk_speed + 0.01)
                        textbutton "-" text_size pink_console_text_size xpadding 0 ypadding 0 action SetVariable('pink_otm_current_walk_speed', max(pink_otm_current_walk_speed - 0.01, 0.01))
                    hbox:
                        $ run_speed_string = '{:5.2f}'.format(pink_otm_current_run_speed)
                        text "Player run speed: [run_speed_string] " size pink_console_text_size
                        textbutton "+" text_size pink_console_text_size xpadding 0 ypadding 0 action SetVariable('pink_otm_current_run_speed', pink_otm_current_run_speed + 0.01)
                        textbutton "-" text_size pink_console_text_size xpadding 0 ypadding 0 action SetVariable('pink_otm_current_run_speed', max(pink_otm_current_run_speed - 0.01, 0.01))
                    hbox:
                        $ xzoom_string = '{:5.2f}'.format(pink_otm_camera_current_xzoom)
                        text "X Zoom: [xzoom_string] " size pink_console_text_size
                        textbutton "++ " text_size pink_console_text_size xpadding 0 ypadding 0 action SetVariable('pink_otm_camera_current_xzoom', pink_otm_camera_current_xzoom + 0.10)
                        textbutton "+ " text_size pink_console_text_size xpadding 0 ypadding 0 action SetVariable('pink_otm_camera_current_xzoom', pink_otm_camera_current_xzoom + 0.01)
                        textbutton "- " text_size pink_console_text_size xpadding 0 ypadding 0 action SetVariable('pink_otm_camera_current_xzoom', max(pink_otm_camera_current_xzoom - 0.01, 0.01))
                        textbutton "--" text_size pink_console_text_size xpadding 0 ypadding 0 action SetVariable('pink_otm_camera_current_xzoom', max(pink_otm_camera_current_xzoom - 0.10, 0.01))
                    hbox:
                        $ yzoom_string = '{:5.2f}'.format(pink_otm_camera_current_yzoom)
                        text "Y Zoom: [yzoom_string] " size pink_console_text_size
                        textbutton "++ " text_size pink_console_text_size xpadding 0 ypadding 0 action SetVariable('pink_otm_camera_current_yzoom', pink_otm_camera_current_yzoom + 0.10)
                        textbutton "+ " text_size pink_console_text_size xpadding 0 ypadding 0 action SetVariable('pink_otm_camera_current_yzoom', pink_otm_camera_current_yzoom + 0.01)
                        textbutton "- " text_size pink_console_text_size xpadding 0 ypadding 0 action SetVariable('pink_otm_camera_current_yzoom', max(pink_otm_camera_current_yzoom - 0.01, 0.01))
                        textbutton "--" text_size pink_console_text_size xpadding 0 ypadding 0 action SetVariable('pink_otm_camera_current_yzoom', max(pink_otm_camera_current_yzoom - 0.10, 0.01))
                    hbox:
                        text "Autocenter sprites: [pink_otm_autocenter_sprites]" size pink_console_text_size
                        if pink_otm_autocenter_sprites:
                            textbutton " Disable." text_size pink_console_text_size xpadding 0 ypadding 0 action SetVariable('pink_otm_autocenter_sprites', False)
                        else:
                            textbutton " Enable." text_size pink_console_text_size xpadding 0 ypadding 0 action SetVariable('pink_otm_autocenter_sprites', True)
                    hbox:
                        text "Force run: [pink_otm_force_run]" size pink_console_text_size
                        if pink_otm_force_run:
                            textbutton " Turn off" text_size pink_console_text_size xpadding 0 ypadding 0 action SetVariable('pink_otm_force_run', False)
                        else:
                            textbutton " Turn on" text_size pink_console_text_size xpadding 0 ypadding 0 action SetVariable('pink_otm_force_run', True)
                    hbox:
                        text "Disable run: [pink_otm_forbid_run]" size pink_console_text_size
                        if pink_otm_forbid_run:
                            textbutton " Turn off" text_size pink_console_text_size xpadding 0 ypadding 0 action SetVariable('pink_otm_forbid_run', False)
                        else:
                            textbutton " Turn on" text_size pink_console_text_size xpadding 0 ypadding 0 action SetVariable('pink_otm_forbid_run', True)
                    hbox:
                        $ follower_count = len(pink_otm_followers)
                        text "Current nr. of Followers: [follower_count]" size pink_console_text_size
                        if follower_count > 0:
                            textbutton " Remove all followers" text_size pink_console_text_size xpadding 0 ypadding 0 action Function(pink.otm.remove_all_followers)


screen pink_otm_developer_maps():
    # This screen takes as arguments:
    #
    # sel_filename
    #    Which map to initially select
    default filenames = pink.otm.get_all_map_filenames()
    default sel_filename = filenames[0]
    default tele_x = 0
    default tele_y = 0

    frame:
        xfill True
        yfill True
        background "#000000"

        hbox:
            frame:
                has vpgrid:
                    cols 1
                    yfill True
                    mousewheel True
                    scrollbars 'both'
                    spacing 1

                vbox:
                    xsize 200
                    for filename in filenames:
                        if filename == sel_filename:
                            textbutton "[filename]" text_size pink_console_text_size text_color '#ffff00' action SetScreenVariable("sel_filename", filename)
                        else:
                            textbutton "[filename]" text_size pink_console_text_size action SetScreenVariable("sel_filename", filename)
                    textbutton "back" text_size pink_console_text_size action [Hide("pink_otm_developer_maps"), Show("pink_developer")]

            frame:
                has vpgrid:
                    cols 1
                    xfill True
                    yfill True
                    mousewheel True
                    scrollbars 'vertical'
                    spacing 1

                $ grid_size, tile_size, image_size, layer_count, tiled_version, properties, tilesets = pink.otm.get_map_data(sel_filename)

                vbox:
                    text "Filename: [sel_filename]" size pink_console_text_size color '#ffff00'
                    text "Tile size (in pixels): [tile_size]" size pink_console_text_size
                    text "Map size (in tiles): [grid_size]" size pink_console_text_size
                    text "Map size (in pixels): [image_size]" size pink_console_text_size
                    text "Nr. of layers: [layer_count]" size pink_console_text_size
                    text "Created in tiled version: [tiled_version]" size pink_console_text_size
                    text "Tilesets:" size pink_console_text_size
                    for tileset_name in tilesets:
                        button:
                            xpadding 0
                            ypadding 0
                            action [Hide("pink_otm_developer_maps"),
                                    Show("pink_developer_tilesets", sel_filename=tileset_name)]
                            text "   [tileset_name]" size pink_console_text_size
                    text "Map-level properties:" size pink_console_text_size
                    for property_str in properties:
                        text "   [property_str]" size pink_console_text_size
                    text "" size pink_console_text_size

                    hbox:
                        textbutton "Teleport to coordinates: " text_size pink_console_text_size xpadding 0 ypadding 0 action [Hide("pink_otm_developer_maps"), Function(pink.otm.go_to_map, target_map=sel_filename, x_coord=tele_x, y_coord=tele_y)]
                        text "X: [tele_x] " size pink_console_text_size
                        textbutton "+" text_size pink_console_text_size xpadding 0 ypadding 0 action SetScreenVariable('tele_x', min(tele_x + 1, int(grid_size.split('x')[0]) - 1))
                        textbutton "-" text_size pink_console_text_size xpadding 0 ypadding 0 action SetScreenVariable('tele_x', max(tele_x - 1, 0))
                        text "Y: [tele_y] " size pink_console_text_size
                        textbutton "+" text_size pink_console_text_size xpadding 0 ypadding 0 action SetScreenVariable('tele_y', min(tele_y + 1, int(grid_size.split('x')[1]) - 1))
                        textbutton "-" text_size pink_console_text_size xpadding 0 ypadding 0 action SetScreenVariable('tele_y', max(tele_y - 1, 0))

screen pink_developer_tilesets():
    # This screen takes as arguments:
    #
    # sel_filename
    #    Which tileset to initially select
    default filenames = pink.otm.get_all_tileset_filenames()
    default sel_filename = filenames[0]

    frame:
        xfill True
        yfill True
        background "#000000"

        hbox:
            frame:
                has vpgrid:
                    cols 1
                    yfill True
                    mousewheel True
                    scrollbars 'both'
                    spacing 1

                vbox:
                    xsize 200
                    for filename in filenames:
                        if filename == sel_filename:
                            textbutton "[filename]" text_size pink_console_text_size text_color '#ffff00' action SetScreenVariable("sel_filename", filename)
                        else:
                            textbutton "[filename]" text_size pink_console_text_size action SetScreenVariable("sel_filename", filename)
                    textbutton "back" text_size pink_console_text_size action [Hide("pink_developer_tilesets"), Show("pink_developer")]

            frame:
                has vpgrid:
                    xfill True
                    yfill True
                    cols 1
                    mousewheel True
                    scrollbars 'vertical'
                    spacing 1

                $ tile_count, tiled_version = pink.otm.get_tileset_data(sel_filename)

                vbox:
                    text "Filename: [sel_filename]" size pink_console_text_size color '#ffff00'
                    text "Nr. of tiles: [tile_count]" size pink_console_text_size
                    text "Created in tiled version: [tiled_version]" size pink_console_text_size

screen pink_developer_sprites():
    # This screen takes as arguments:
    #
    # sel_filename
    #    Which sprite collection to initially select
    default filenames = pink.otm.get_all_sprite_filenames()
    default sel_filename = filenames[0]

    frame:
        xfill True
        yfill True
        background "#000000"

        hbox:
            frame:
                has vpgrid:
                    cols 1
                    yfill True
                    mousewheel True
                    scrollbars 'both'
                    spacing 1

                vbox:
                    xsize 200
                    for filename in filenames:
                        if filename == sel_filename:
                            textbutton "[filename]" text_size pink_console_text_size text_color '#ffff00' action SetScreenVariable("sel_filename", filename)
                        else:
                            textbutton "[filename]" text_size pink_console_text_size action SetScreenVariable("sel_filename", filename)
                    textbutton "back" text_size pink_console_text_size action [Hide("pink_developer_sprites"), Show("pink_developer")]

            frame:
                has vpgrid:
                    cols 1
                    xfill True
                    yfill True
                    mousewheel True
                    scrollbars 'vertical'
                    spacing 1

                $ animations, pc_sprite = pink.otm.get_sprite_data(sel_filename)

                vbox:
                    text "Filename: [sel_filename]" size pink_console_text_size color '#ffff00'
                    text "Animations:" size pink_console_text_size
                    for animation in sorted(animations):
                        text "   [animation]" size pink_console_text_size
                    text "Suitable for PC: [pc_sprite]" size pink_console_text_size
                    text ""
                    if pc_sprite:
                        textbutton "Use Sprite" text_size pink_console_text_size action [Hide("pink_developer_sprites"), Function(pink_otm_current_pc.switch_sprite_collection, sel_filename), Jump("pink_otm_developer_stop")]
                        textbutton "Add Follower" text_size pink_console_text_size action [FunctionNoReturn(pink.otm.add_player_follower, "pink_engine/sprite_collections/" + sel_filename)]


init python:
    class FunctionNoReturn(Function):
        def __call__(self):
            rv = self.callable(*self.args, **self.kwargs)

            if self.update_screens:
                renpy.restart_interaction()
