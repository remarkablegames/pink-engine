label test_corridor_B11_sign1:
    $ pink.otm.start_continuing_event()
    """This room exists to test a parallel process that adds control commands to objects depending on the player's
    position. This particular room uses that process to automatically open doors.

    The door on the left should open when approached from either side.

    The door in the middle should only open when approached from the bottom of the map.

    The door on the right should only open when approached from the top of the map."""
    $ pink.otm.end_current_event()
