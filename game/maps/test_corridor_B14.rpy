label test_corridor_B14_sign1:
    $ pink.otm.start_continuing_event()
    """This room exists to test auto-centering of NPCs."""
    $ pink.otm.end_current_event()

label test_corridor_B14_npc1a_talk:
    $ pink.otm.start_continuing_event()
    "Youth" """Hello! I have been automatically centered on this particular tile, as I was placed on a map along
    grid lines."""
    $ pink.otm.end_current_event()

label test_corridor_B14_npc1b_talk:
    $ pink.otm.start_continuing_event()
    "Youth" """Hello! I have not been automatically centered, because that setting has been disabled."""
    $ pink.otm.end_current_event()

label test_corridor_B14_npc2_talk:
    $ pink.otm.start_continuing_event()
    "Youth" """Hello! I am not automatically centered on this tile, as I have the 'forbid_autocenter' property."""
    $ pink.otm.end_current_event()

label test_corridor_B14_npc3_talk:
    $ pink.otm.start_continuing_event()
    "Youth" """Hello! I am not automatically centered on this tile, as I was placed off-grid."""
    $ pink.otm.end_current_event()
