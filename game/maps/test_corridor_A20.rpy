label test_corridor_A20_sign:
    $ pink.otm.start_continuing_event()
    """This room exists to test movement rules and complex autotiles created by the autotile generator.

    The area on the left is an autotile whose boundaries are marked as impassible. You should not be able to cross
    any hazard line.

    The area in the middle is an animated autotile. It's just there to look pretty, with no additional movement
    functionality.

    The area on the right is an autotile set to only allow movement on boundary-less cells. You should not be able to
    enter any coordinate that includes red squares."""
    $ pink.otm.end_current_event()
