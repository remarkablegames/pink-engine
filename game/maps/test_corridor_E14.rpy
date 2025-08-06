label test_corridor_E14_sign:
    $ pink.otm.start_continuing_event()
    """
    This room further builds on the StartMapEvents functionality demonstrated in room E11-E13

    As of version 0.15.0, sprite collection objects in the pink engine, such as NPCs and the player character, have the
    hide() and reveal() functions available.

    Use hide() to hide a character during a cutscene. It will have neither an image or movement rules while hidden.

    Use reveal() to undo the hiding.

    Combining StartMapEvents with the hide() function on the player allows you to start an event at map initialization
    without the player being visible.
    """
    $ pink.otm.end_current_event()

label test_corridor_E14_event:
    $ pink.otm.start_continuing_event()
    $ pink_otm_current_pc.hide()
    """The player character should not be visible during this event."""
    $ pink_otm_current_pc.reveal()
    $ pink.otm.end_current_event()
