label test_corridor_A21_sign:
    $ pink.otm.start_continuing_event()
    """This room exists to test conditional events. The event for reading this sign will only trigger if the player
    is facing upwards. The event for the pink floor thing will only trigger if the player is facing downwards."""
    $ pink.otm.end_current_event()

label test_corridor_A21_thing:
    $ pink.otm.start_continuing_event()
    """This event will only trigger if the player is facing downwards."""
    $ pink.otm.end_current_event()
