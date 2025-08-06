label test_corridor_B03a_sign:
    $ pink.otm.start_continuing_event()
    """This room exists to test the background music and ambience map properties.

    If you move to the map to the North, the music should keep playing.

    If you move to the map to the East, the track should change.

    If you move to the hallway to the South, background music should stop playing."""
    $ pink.otm.end_current_event()

label test_corridor_B03b_sign:
    $ pink.otm.start_continuing_event()
    """This room exists to test the background music and ambience map properties. The ambience you are hearing is
    'Crowd Talk Loop' by 'Iwan 'qubodup' Gabovitch' on freesound.org.

    The music you are hearing underneath the ambience is 'still', by Dlay, retrieved from freemusicarchive.org. Links
    to both are in the credits file.

    If you move to the map to the North, the music and ambience should keep playing.

    If you move to the map to the West, the track should change and the ambience should stop.

    If you move to the hallway to the South, background music should stop playing."""
    $ pink.otm.end_current_event()

label test_corridor_B03c_sign:
    $ pink.otm.start_continuing_event()
    """This room exists to test the background music and ambience map properties. The music and ambience in this
    room should be the same as the room you came in from."""
    $ pink.otm.end_current_event()
