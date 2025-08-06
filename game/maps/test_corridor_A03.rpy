label test_corridor_A03_sign:
    $ pink.otm.start_continuing_event()
    """This room exists to test collision and occultation (the process that determines the draw order of objects). In
    this room, you can see ten pillars.

    Moving behind the pillars should cause them to be drawn in front of the player. To switch between different player
    sprites, use the left-most computer in the main hall.

    The big punk sprite is two squares tall, so will be drawn in front of the objects when standing before them.

    The first pair of pillars, on the left, consists of a single object in Tiled each, and have been placed so that
    their 'bases' (the part of the object that actually counts for collision and event interaction) only intersect a
    single tile.

    The second pair of pillars are part of a tile layer in Tiled, rather than an object layer. They again consist
    of only a single tile per image.

    The third pair of pillars is again drawn on an object layer in Tiled, but has now been placed so that its bases
    intersect with multiple map coordinates.

    The fourth pair of pillars does not consist of a single image per pillar.

    Rather, it is modular, making use of the occultates_as_y property to ensure all components are placed in the render
    order as if they were placed on the lowest y coordinate, ensuring visual consistency.

    The fifth pair of pillars is the same as the fourth pair, but placed so that its bases intersect multiple
    coordinates. """
    $ pink.otm.end_current_event()
