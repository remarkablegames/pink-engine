label test_corridor_E08_sign:
    $ pink.otm.start_continuing_event()
    """This room tests arbitrary event triggers that have been placed in an invisible interaction layer.

    If you open this map in tiled, you'll see a pink thing placed on an interaction layer (a type of non-visible layer).

    The layer has an arbitrary even trigger attached that should cause an attemp to trigger every time the player tries
    to run."""
    $ pink.otm.end_current_event()

label test_corridor_E08_run:
    $ pink.otm.start_dynamic_event()
    """This very annoying event is triggered whenever you try to run in this room."""
    $ pink.otm.end_dynamic_event()