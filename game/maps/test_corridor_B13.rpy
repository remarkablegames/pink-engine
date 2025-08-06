default test_corridor_B13_var1 = 1
default test_corridor_B13_var2 = 1

init python:
    def test_corridor_B13_var_reset():
         renpy.store.test_corridor_B13_var1 = 1
         renpy.store.test_corridor_B13_var2 = 1

label test_corridor_B13_sign1:
    $ pink.otm.start_continuing_event()
    """This room has a time-based parallel process running, affecting two variables. The value of the
    variable is displayed on the screens at the top of the map.

    The top row is a simple sequence that sets the value to 1 higher every second, before resetting at the end.

    The bottom row is a more complex sequence, using adding and subtraction in its sequence rather than always just
    setting the value. It also uses less monotonous timing. Like the top sequence, the bottom sequence resets at the
    end.

    While interacting with this sign, the parallel process will continue. The sign to the left pauses the parallel
    process explicitly. The sign to the right starts a static event that pauses all parallel processes.

    Opening your menu should pause the timer."""
    $ pink.otm.end_current_event()

label test_corridor_B13_sign2:
    $ pink.otm.start_continuing_event()
    $ pink_otm_current_map.pause_parallel_processes("var_times")
    """While you interact with this sign, the parallel process changing the variables is paused. """
    $ pink.otm.end_current_event()

label test_corridor_B13_sign3:
    $ pink.otm.start_static_event()
    """Interacting with this sign starts a static event. During a static event, all parallel processes are halted."""
    $ pink.otm.end_current_event()
