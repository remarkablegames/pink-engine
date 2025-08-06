default test_variable_01 = False

label test_corridor_A19_sign:
    $ pink.otm.start_continuing_event()
    $ test_variable_01 = True
    """This room exists to test rendering capacity. If all goes well, you should experience no significant slow-down
    in this room"""
    $ pink.otm.end_current_event()
