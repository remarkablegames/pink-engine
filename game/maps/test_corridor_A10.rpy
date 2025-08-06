label test_corridor_A10_sign:
    $ pink.otm.start_continuing_event()
    """These six characters are all walking the same route, but with different options set, causing slightly different
    behavior.

    Middle Left: Uses all the default options.

    Top Left: This character has turn_and_move set to False, meaning that he turns and moves as separate commands.

    Top Right: This character has animate_invalid_move set to False for its entire route. As a result, when you block
    his movement, he switches from his walk animation to his stand animation.

    Middle Right: This character has pop_invalid_move set to True for its entire route. This means that, when a
    move is invalid, the character will not try to repeat it, instead moving on to the next command. When you block
    his movement, his route will change.

    Bottom Right: This character has a movement route that consists only of two 'go_to' commands, for the top left
    and bottom right coordinates of its route.

    Bottom Left: This character has a movement route that consists only of two 'go_to_smart' commands, causing it to
    engage in pathfinding when its path is blocked"""
    $ pink.otm.end_current_event()

label test_corridor_A10b_sign:
    $ pink.otm.start_continuing_event()
    """This is a copy of the last room, except the NPCs movements have an 'arc_height' attached to them, causing them
    to hop, hop, hop to their destinations."""
    $ pink.otm.end_current_event()
