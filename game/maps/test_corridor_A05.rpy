default pink_otm_teleporting_noise = 'music/pop.wav'

label test_corridor_A05_sign:
    $ pink.otm.start_continuing_event()
    """This room exists to test touch-based events. You should only have been able to get here through use of the
    pink teleportation thingies."""
    $ pink.otm.end_current_event()

label test_corridor_A05_tele5:
    $ pink.otm.start_continuing_event()
    """This is a test to ensure that no infinite loops occur. If your program is not frozen, hurray!"""
    $ pink.otm.end_current_event()
