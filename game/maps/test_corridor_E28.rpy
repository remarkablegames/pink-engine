
label test_corridor_E28_sign:
    $ pink.otm.start_continuing_event()
    """In addition to locational sounds, the 0.17 update for the pink engine also includes movement sounds. The sand,
    metal plate and rock tiles in this room all have the 'sound_tag' property.

    This property maps to a sound file as defined in the standard_events.rpy file.

    Whenever you step on one of the tiles, the specified sound effect plays. You can extend and alter the dictionary
    in standard_events.rpy as you see fit, giving your game your own unique soundscape.

    The pink engine also supports playing bumping sounds when you bump into an object. You can enable or disable
    this sound by interacting with the computer in this room.

    Note that followers will also trigger sounds on these tiles, albeit somewhat softer.

    You can adjust the volume at which follower movement sounds play by altering the value of
    `pink_otm_default_follower_movement_sound_multiplier` in the pink config file.
    """
    $ pink.otm.end_current_event()


label test_corridor_E28_computer:
    $ pink.otm.start_continuing_event()
    menu:
        "Wall bumping noise:"

        "Enable":
            $ pink_otm_current_pc.movement_sound_blocked = 'music/bump.wav'
        "Disable":
            $ pink_otm_current_pc.movement_sound_blocked = None
        "Return":
            pass
    $ pink.otm.end_current_event()