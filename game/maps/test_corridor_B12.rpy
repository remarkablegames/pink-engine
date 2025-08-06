label test_corridor_B12_sign1:
    $ pink.otm.start_continuing_event()
    $ from datetime import datetime
    $ today = datetime.now().strftime('%Y-%m-%d %H:%M:%S %Z')
    """Bug report [today]: User has proven able to enter forbidden room by altering his movement speed."""
    """User has now been classified as a Iota-level threat."""
    $ pink.otm.end_current_event()

label test_corridor_B12_npc1:
    $ pink.otm.start_dynamic_event()
    "Woman" """Oy! This room's sign is for authorized guests only! This map has a parallel process that makes me
    move to block your pitiful attempts at an entrance."""
    $ pink.otm.end_current_event()
