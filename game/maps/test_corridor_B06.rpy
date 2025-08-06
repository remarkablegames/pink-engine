label test_corridor_B06_sign1:
    $ pink.otm.start_continuing_event()
    """This room tests a parallel process that changes the zoom level as you approach the pink thingies.

    The pink thingies near the top of the map zoom in, with the left zooming in gradually as you approach, and the
    right zooming in a single step.

    The pink thingies near the bottom of the map zoom out, with the right zooming out gradually as you approach, and
    the left zooming in in a single step."""
    $ pink.otm.end_current_event()
