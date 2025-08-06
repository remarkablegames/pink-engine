label test_corridor_A09_sign:
    $ pink.otm.start_continuing_event()
    """This room exists to test basic movement-capable NPCs. You should be seeing a lot of movement on your screen right
    now.

    The character in the bottom left should start in the same position she was in when you left the room. The rest
    should change back to their starting position."""
    $ pink.otm.end_current_event()

label test_corridor_A09_hero:
    $ pink.otm.start_continuing_event()
    "Adventurer" "Ho there, fellow explorer!"
    $ pink.otm.end_current_event()
