
label test_corridor_E27_sign:
    $ pink.otm.start_continuing_event()
    """Whereas the previous three rooms demonstrated the emits_sound property, this room demonstrates directional sounds
    that are played through control commands. Whenever the NPC in this room reaches one of the pink floor things on
    his route, you'll hear him emit one of two alternating noises.

    While the NPC in this room uses the play_sound control command to make noises, any control command that creates
    a sound can be made directional by including the 'pan_sound=True, scale_sound=True' properties.
    """
    $ pink.otm.end_current_event()

