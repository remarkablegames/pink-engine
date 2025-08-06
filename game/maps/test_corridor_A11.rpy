label test_corridor_A11_sign:
    $ pink.otm.start_continuing_event()
    """This room demonstrates a couple of extra options when giving your NPCs commands.

    Bottom left: This character makes a few turns when it is all the way on the right.

    Middle left: This character has the same movement route as the bottom left, but changes its movement speed every
    iteration.

    Top left: This character has a delay in its movement route, causing it to pause for a few seconds when all the way
    on the right.

    Top right: This character plays a brief animation when all the way on the left.

    Middle right: This character plays a much lengthier animation when all the way on the left.

    Bottom right: This character plays the same animation as the middle right character, but at a slower speed."""
    $ pink.otm.end_current_event()
