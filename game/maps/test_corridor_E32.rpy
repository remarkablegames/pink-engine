default E32_pursue_var = False

label test_corridor_E32_sign:
    $ pink.otm.start_continuing_event()
    """This room demonstrates a chase functionality that causes a pursuer to start pursuing based on a variable being
    flipped, and causes the pursuer to teleport back to their origin when the variable is set to False.

    Interacting with either screen in the room will flip the value of the variable that causes the minotaur to start
    pursuing.
    """
    $ pink.otm.end_current_event()
