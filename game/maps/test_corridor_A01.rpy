label test_corridor_A01_sign1:
    $ pink.otm.start_continuing_event()
    """This room exists for the sake of testing basic event functionality. Every time you interact with an
    object that has an event attached (such as this sign, or the door you used to get here), the pink engine jumps to a
    specified ren'py label.

    in the case of this sign, said label consists of a call to start a continuing pink engine event (ensuring that
    the map remains shown as a background, and any moving characters on screen keep moving), this dialogue, and then
    an end of the event.

    The other sign in this room leaves the pink engine in its event, returning to regular ren'py."""
    $ pink.otm.end_current_event()

label test_corridor_A01_sign2:
    $ pink.otm.leave_otm()
    show placeholder
    """This room exists for the sake of testing basic event functionality. Every time you interact with an
    object that has an event attached (such as this sign, or the door you used to get here), the pink engine jumps to a
    specified ren'py label.

    in the case of this sign, said label consists of a call to leave the pink engine, display a very ugly
    background image, show this dialogue, and then return to the pink engine map.

    The other sign in this room remains in the pink engine during its event."""
    $ pink.otm.return_to_otm()
