label test_corridor_B10_sign1:
    $ pink.otm.start_continuing_event()
    """This room exists to test repositioning characters as part of an event. When you stand on the pink thing, the
    characters in this room should switch locations."""
    $ pink.otm.end_current_event()

label test_corridor_B10_tele1:
    $ pink.otm.start_dynamic_event()
    $ test_corridor_B10_npc1.set_to_coords(4, 5, orientation="left")
    $ test_corridor_B10_npc2.set_to_coords(4, 6, orientation="left")
    $ renpy.pause(0.5)
    $ test_corridor_B10_npc1.set_to_coords(1, 4, orientation="right")
    $ test_corridor_B10_npc2.set_to_coords(1, 5, orientation="right")
    $ renpy.pause(0.5)
    $ test_corridor_B10_npc1.set_to_coords(3, 7, orientation="up")
    $ test_corridor_B10_npc2.set_to_coords(3, 3, orientation="down")
    $ renpy.pause(0.5)
    $ test_corridor_B10_npc1.set_to_coords(2, 3, orientation="down")
    $ pink.otm.end_dynamic_event()

label test_corridor_B10_npc1_talk:
    $ pink.otm.start_continuing_event()
    "Mark" "Hi, my name is Mark, but you can call me test_corridor_B10_npc1 in your code."
    $ pink.otm.end_current_event()

label test_corridor_B10_npc2_talk:
    $ pink.otm.start_continuing_event()
    "Lucy" "Hi, my name is Lucy, but you can call me test_corridor_B10_npc2 in your code."
    $ pink.otm.end_current_event()
