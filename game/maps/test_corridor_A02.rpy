label test_corridor_A02_sign:
    $ pink.otm.start_continuing_event()
    """This room exists to test collision interaction. In it, you can find three ugly rock-like things.

    The rock on the left is a Tiled object, placed so that it fills a single grid square. The rock in the middle is
    placed on a tile layer in Tiled rather than an object layer. The final rock, on the right, is an object again, but
    placed so that it occupies multiple coordinates.

    The player should not be able to enter any map coordinate that contains an ugly rock."""
    $ pink.otm.end_current_event()
