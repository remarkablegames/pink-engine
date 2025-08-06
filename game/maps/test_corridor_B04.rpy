label test_corridor_B04_sign1:
    $ pink.otm.start_continuing_event()
    """This room exists to test parallel processes. Standing on the white areas in this room should change the music
    being played. Moving to the left or the right of the map should cause the audio panning to shift in that
    direction."""
    $ pink.otm.end_current_event()
