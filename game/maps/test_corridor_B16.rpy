label test_corridor_B16_sign:
    $ pink.otm.start_continuing_event()
    """This room is all about walking through walls.

    To get here, you had to walk through a wall. This permeable piece of architecture was accomplished by using
    wall tiles in an object layer and overriding the move_to and move_from settings.

    Over on the right, you can see an NPC walking through the wall. Unlike you, he is not using a permeable wall, but
    has instead been given the can_always_move property. He can even walk through you!

    This functionality is intended for cutscenes, to allow characters to move through otherwise impermeable objects."""
    $ pink.otm.end_current_event()

label test_corridor_B16_npc:
    $ pink.otm.start_dynamic_event()
    "Youth" "I'm a ghost!"
    $ pink.otm.end_current_event()
