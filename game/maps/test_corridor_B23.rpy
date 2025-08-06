default pink_otm_B23_field = False

label test_corridor_B23_sign:
    $ pink.otm.start_continuing_event()
    """
    This room demonstrates how to add and remove a parallel process element through object conditionality.

    When you interact with the computer, it changes the 'pink_otm_B23_field' variable. On this map's invisible
    'interact' layer, there is an area that is conditional on this variable.

    This area has a 'code_on_add' and 'code_on_remove' property, which add and remove a music-playing area to the
    relevant parallel process respectively
    """
    $ pink.otm.end_current_event()

