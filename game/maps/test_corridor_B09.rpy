default test_corridor_B09_var = 1

init python:
    def test_corridor_B09_function():
        global test_corridor_B09_var
        test_corridor_B09_var += 1
        if test_corridor_B09_var == 10:
            test_corridor_B09_var = 1

label test_corridor_B09_sign1:
    $ pink.otm.start_continuing_event()
    """This room exists to test objects which run code rather than events, allowing you to update variables without
    interrupting the game.

    The number displayed near the top of the map is equal to the value of variable 'test_corridor_B09_var'. The
    function 'test_corridor_B09_function' updates this variable.

    Walking onto the pink thing to the right runs this function.

    Walking onto the pink thing to the left runs this function, but only if the player moves rightwards.

    Interacting with the computer runs this function, but only if the player faces upwards.
    """
    $ pink.otm.end_current_event()
