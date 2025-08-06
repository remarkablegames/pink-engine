label test_corridor_B20_sign:
    $ pink.otm.start_continuing_event()
    """This room exists to test 'special movement' tiles. These are map objects with properties that override 'go_left',
    'go_right', etc. commands.

    Multiple examples of special movements are demonstrated on this map, including stairs, ladders, and hopping over
    areas.

    Four of the characters are using very specific go_to loops, moving along the exact same route every time. One of
    these characters is instead using a go_to_smart command to move between the four pink squares, and will change
    his route when blocked.

    If you open this map in Tiled, you'll see that the map objects that implement the special movements are placed
    on a 'move_sub' layer, indicating that they override the movement of sub layers (for this particular map, those
    are the background tiles)."""
    $ pink.otm.end_current_event()