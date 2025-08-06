label test_corridor_A12_sign_s:
    $ pink.otm.start_static_event()
    """Interacting with this sign starts a static event. During a static event, all moving objects on screen instantly
    freeze, giving the appearance of a gameworld that is wholly paused.
    """
    $ pink.otm.end_current_event()

label test_corridor_A12_sign_c:
    $ pink.otm.start_continuing_event()
    """Interacting with this sign starts a continuing event. During a continuing event, all objects on screen keep
    moving as they normally do, unless the event itself passed on new instructions.
    """
    $ pink.otm.end_current_event()

label test_corridor_A12_sign_d:
    $ pink.otm.start_dynamic_event()
    """Interacting with this sign starts a dynamic event. During a dynamic event, all objects on screen finish their
    current move, and then remain in place unless the event itself passes on new instructions.
    """
    $ pink.otm.end_current_event()

label test_corridor_A12_npc_s:
    $ pink.otm.start_static_event()
    "Youth" """Interacting with me triggers a static event. When a static event is triggered, all moving objects on screen
    instantly freeze in place, and remain frozen until the event ends.

    No instructions can be passed to objects during a static event, as objects will remain frozen no matter what until
    the end of the event.

    Static events are useful for events wherein the world is explicitly paused while the player does something."""
    $ pink.otm.end_current_event()

label test_corridor_A12_npc_c1:
    $ pink.otm.start_continuing_event(interaction_reaction=False)
    "Youth" """Interacting with me triggers a continuing event. During a continuing event, all objects keep moving
    as they were before, unless the event specifically tells them to do something else.

    Unlike my more social companion over at C2, my event does not include a call to my default interaction stack,
    which I'm continuing to walk around in circles even when talking to you.

    Continuing events are useful for events where you don't want the broader game world to be interrupted by what
    the player does."""
    $ pink.otm.end_current_event()

label test_corridor_A12_npc_c2:
    $ pink.otm.start_continuing_event()
    "Youth" """Interacting with me triggers a continuing event. During a continuing event, all objects keep moving
    as they were before, unless the event specifically tells them to do something else.

    Unlike my rude companion over at C1, my event does includes a call to my default interaction stack, which is why
    I stopped and turned to you when you interacted with me.

    Continuing events are useful for events where you don't want the broader game world to be interrupted by what
    the player does."""
    $ pink.otm.end_current_event()

label test_corridor_A12_npc_d1:
    $ pink.otm.start_dynamic_event(interaction_reaction=False)
    "Youth" """Interacting with me triggers a dynamic event. During a dynamic event, all objects finish their current
    movement, but stand still afterwards unless the event specifically tells them to do something else.

    At the end of a dynamic event, all characters automatically return to the location they began it in.

    Unlike my more social companion over at D2, my event does not include a call to my default interaction stack, which
    is why I'm not turning to face you.

    Dynamic events are useful to trigger cutscenes, or to ensure objects don't keep on moving while you interact
    with a particular something."""
    $ pink.otm.end_current_event()

label test_corridor_A12_npc_d2:
    $ pink.otm.start_dynamic_event()
    "Youth" """Interacting with me triggers a dynamic event. During a dynamic event, all objects finish their current
    movement, but stand still afterwards unless the event specifically tells them to do something else.

    At the end of a dynamic event, all characters automatically return to the location they began it in.

    Unlike my rude companion over at D1, my event does includes a call to my default interaction stack, which is why
    I stopped and turned to you when you interacted with me.

    Dynamic events are useful to trigger cutscenes, or to ensure objects don't keep on moving while you interact
    with a particular something."""
    $ pink.otm.end_current_event()
