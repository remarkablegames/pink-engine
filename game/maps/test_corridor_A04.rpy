label test_corridor_A04_sign:
    $ pink.otm.start_continuing_event()
    """This room exists to test more complex occultation. Each shelf actually consists of two distinct objects (the
    shelf itself, and the books/drawers), drawn at different z orders.

    Moving behind or in front of them should cause both to be drawn in front of/behind the player without changing
    their own relative order.

    To switch between different player sprites, use the left-most computer in the main hall. The big punk sprite
    is two squares tall, so will be drawn in front of the objects when standing before them."""
    $ pink.otm.end_current_event()
