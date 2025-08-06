label test_corridor_A23_mino_catch:
    $ pink.otm.leave_otm()
    """This room exists to test two features:
    1) Events triggered by contact with an NPC.
    2) Pathfinding targeting a moving target

    Being caught by either of the minotaurs in this room will result in you being removed from the room.
    """
    $ pink.otm.go_to_map(
        target_map='test_corridor_A.json', x_coord=73, y_coord=3, orientation="down")