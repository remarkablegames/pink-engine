label test_corridor_B18_sign:
    $ pink.otm.start_continuing_event()
    """This room exists to test followers. Interact with the NPCs to add them as followers. Interact with the machine to
    remove or hide followers."""
    $ pink.otm.end_current_event()

label test_corridor_B18_follower_1:
    $ pink.otm.start_continuing_event()
    $ pink.otm.add_player_follower("pink_engine/sprite_collections/test_player_proper_hero.json")
    $ pink.otm.end_current_event()

label test_corridor_B18_follower_2:
    $ pink.otm.start_continuing_event()
    $ pink.otm.add_player_follower("pink_engine/sprite_collections/test_player_sprite_collection_big.json")
    $ pink.otm.end_current_event()

label test_corridor_B18_follower_3:
    $ pink.otm.start_continuing_event()
    $ pink.otm.add_player_follower("pink_engine/sprite_collections/sevarihk green blob.json")
    $ pink.otm.end_current_event()

label test_corridor_B18_machine_1:
    $ pink.otm.start_continuing_event()
    menu:
        "Which action would you like to take?"

        "Remove all followers":
            $ pink.otm.remove_all_followers()
        "Remove 1st follower":
            $ pink.otm.remove_follower_by_index(0)
        "Remove 1st follower who is a green blob":
            $ pink.otm.remove_follower_by_path("pink_engine/sprite_collections/sevarihk green blob.json")
        "Remove all green blob followers":
            $ pink.otm.remove_follower_by_path(
                "pink_engine/sprite_collections/sevarihk green blob.json", remove_all=True)
        "Do nothing":
            $ pass
    $ pink.otm.end_current_event()
