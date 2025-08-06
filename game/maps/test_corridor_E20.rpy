label test_corridor_E20_event:
    $ pink.otm.start_continuing_event()
    "If you have a green blob follower, he will jump in place now."
    $ follower_blob = pink.otm.get_follower("pink_engine/sprite_collections/sevarihk green blob.json")
    if follower_blob is not None:
        $ follower_blob.control_stack = [
            pink.otm.ControlCommand(
                "special_move", move_by_x=0, move_by_y=0, movement_time=0.3, arc_height=64,
                never_repeat=True, path=renpy.store.pink_otm_hop_noise)]
        $ renpy.pause(0.5)
    $ pink.otm.end_current_event()


label test_corridor_E20_computer:
    $ pink.otm.start_continuing_event()
    menu:
        "Which action would you like to take?"

        "Remove all followers":
            $ pink.otm.remove_all_followers()
        "Do nothing":
            $ pass
    $ pink.otm.end_current_event()
