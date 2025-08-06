label test_corridor_A22_sign_1:
    $ pink.otm.start_continuing_event()
    """This room exists to test pathfinding. The NPC in section A demonstrates the default pathwalking functionality.
    He is set to use the 'go_to_smart' control command to reach all four corners of his path.

    He finds this path by making use of an A* pathfinding algorithm with a preference for straight lines that calculates
    up to 10 movements at once.
    """
    $ pink.otm.end_current_event()

label test_corridor_A22_sign_2:
    $ pink.otm.start_continuing_event()
    """The amount of movements that are calculated at once is customizable. You may want to reduce the number if
    the route needs to be recalculated often (for example, when you have multiple NPCs chasing the PC at once).

    You may also want to increase the number if you want NPCs to navigate very tricky areas.

    The NPCs in section B and C are both given the exact same route to find a path through. The NPC in section B
    has the default max_path_length value of 10, and thus cannot find a route.

    However, the NPC in section C has a max_path_length of 20 for the first leg of his journey, and can find the route.
    """
    $ pink.otm.end_current_event()
