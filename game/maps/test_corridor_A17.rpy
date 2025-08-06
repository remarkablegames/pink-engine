label test_corridor_A17_sign:
    $ pink.otm.start_continuing_event()
    """This room exists to test various movement options. The white area near the entrance has two characters
    performing random movement within the grid.

    The characters that flank this white area demonstrate the clockwise turns.

    The character in the walled-off area is set to move towards the player. He will prioritize the y axis over
    the x axis.

    The character in the star-shaped area just below this tablet is also set to move towards the player, except for
    only two steps, before returning to the center of the star.

    The two characters that flank the star-shaped area demonstrate the random turn.

    The characters in the corner always turn towards the player."""
    $ pink.otm.end_current_event()
