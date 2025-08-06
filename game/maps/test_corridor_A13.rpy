label test_corridor_A13_sign:
    $ pink.otm.start_continuing_event()
    """This room exists to test movement routes that include animation changes.

    The character on the left switches its movement animation between walk and stand every time it completes its route.

    The character on the right changes its stand animation every six seconds.
    """
    $ pink.otm.end_current_event()
