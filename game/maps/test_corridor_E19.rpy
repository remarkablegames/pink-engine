default test_corridor_E19_weather = 0

label test_corridor_E19_sign:
    $ pink.otm.start_continuing_event()
    """
    This room tests conditional layers. This room has three different conditional layers, each of which gives a
    different coloured overlay. You can switch overlays using the computer outside of the room.

    Note that conditional layers are only evaluated on entry/exit/reloading of a map, unlike conditional objects, which
    are reevaluated every frame.
    """
    $ pink.otm.end_current_event()


label test_corridor_E19_computer:
    $ pink.otm.start_continuing_event()
    menu:
        "Which colour overlay should room E19 have?"

        "None":
            $ test_corridor_E19_weather = 0
        "Green":
            $ test_corridor_E19_weather = 1
        "Blue":
            $ test_corridor_E19_weather = 2
        "Red":
            $ test_corridor_E19_weather = 3
    $ pink.otm.end_current_event()