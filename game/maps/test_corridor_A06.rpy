default test_corridor_A06_pillar = False

label test_corridor_A06_sign:
    $ pink.otm.start_continuing_event()
    """This room exists to test conditional objects. After reading this sign, a computer should appear in the
    middle of the room. You should not be able to walk through it."""
    $ test_corridor_A06_pillar = True
    $ pink.otm.end_current_event()

label test_corridor_A06_pillar:
    $ pink.otm.start_continuing_event()
    menu:
        "Would you like to make this computer unit vanish again?"

        "Yes":
            $ test_corridor_A06_pillar = False
        "No":
            $ test_corridor_A06_pillar = True
    $ pink.otm.end_current_event()
