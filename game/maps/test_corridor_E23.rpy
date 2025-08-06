default test_corridor_E23_bridge_over = True

label test_corridor_E23_sign:
    $ pink.otm.start_continuing_event()
    """This room demonstrates how to build a bridge in the pink engine.

    There's actually two distinct versions of every tile that makes up the bridge. One on a layer that is drawn over
    the player, the other on a layer which is drawn under the player. Which version shows up depends on the variable
    'test_corridor_E23_bridge_over'.

    The value of this variable is changed by invisible tiles at the top and bottom of the ladder. These have a
    'code_on_touch' variable, allowing for the value to be changed without triggering an event.

    The bridge tiles in the 'sub' layer have their own movement rules, preventing you from walking off the bridge onto
    the ground.
    """
    $ pink.otm.end_current_event()

