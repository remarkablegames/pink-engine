label test_corridor_A18_sign:
    $ pink.otm.start_continuing_event()
    """This room exists to test off-grid movement. You should see various characters moving in the white areas.

    With the exception of the top-left character, the characters on this map all use the 'custom_go' command. The
    character in the top left uses 'custom_go_to' instead. """
    $ pink.otm.end_current_event()
