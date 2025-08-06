default test_corridor_E22_sprite_path = "pink_engine/sprite_collections/sevarihk blue blob.json"

label test_corridor_E22_follower:
    $ pink.otm.start_continuing_event()
    $ pink.otm.add_player_follower(test_corridor_E22_sprite_path)
    $ pink.otm.end_current_event()


label test_corridor_E22_computer:
    $ pink.otm.start_continuing_event()
    menu:
        "Which action would you like to take?"

        "Remove all followers":
            $ pink.otm.remove_all_followers()

            $ pink.otm.force_instant_transition_on_event_end()
            $ pink.otm.go_to_map(target_map='test_corridor_E22.json', x_coord=1, y_coord=4, orientation="up")
        "Switch blob color":
            $ follower_blob = pink.otm.get_follower(test_corridor_E22_sprite_path)

            if test_corridor_E22_sprite_path == "pink_engine/sprite_collections/sevarihk blue blob.json":
                $ test_corridor_E22_sprite_path = "pink_engine/sprite_collections/sevarihk red blob.json"
            else:
                $ test_corridor_E22_sprite_path = "pink_engine/sprite_collections/sevarihk blue blob.json"

            if follower_blob is not None:
                $ follower_blob.switch_sprite_collection(test_corridor_E22_sprite_path)
            else:
                $ test_corridor_E22_follower_NPC.switch_sprite_collection(test_corridor_E22_sprite_path)

        "Do nothing":
            $ pass
    $ pink.otm.end_current_event()
