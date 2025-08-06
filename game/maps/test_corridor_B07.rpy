default test_corridor_B07_var = 5

label test_corridor_B07_sign1:
    $ pink.otm.start_continuing_event()
    """This room exists to test parallel processes. As you move horizontally across this level, it should update
    the variable 'test_corridor_B07_var'.

    The number objects at the top of the map each have a conditional statement that cause them to appear only when
    'test_corridor_B07_var' matches the number."""
    $ pink.otm.end_current_event()
