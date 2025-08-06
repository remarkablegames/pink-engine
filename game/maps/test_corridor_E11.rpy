label test_corridor_E11_sign:
    $ pink.otm.start_continuing_event()
    """
    As of version 0.15.0, the pink engine allows you to set conditional events that trigger upon entering the map
    through code.

    Using the code_on_enter property on a map, or the code_on_add property on a map object, you can cause an event to
    trigger when a player enters the map in any way.

    This map uses the following code_on_enter segment set on the map itself:
        StartMapEvents.add_event(event='test_corridor_E11_event')
    wherein test_corridor_E10_event is the name of the event.

    It is also possible, like in previous versions, to trigger an event on entering the map through a touch event
    (an event triggered by touching an object). This technique is used in test room B17.

    However, the old method requires an object for every route of entrance, and causes the event to trigger after
    the first frame of the map has been rendered, rather than before. It is generally advised to use this new system.
    """
    $ pink.otm.end_current_event()

label test_corridor_E11_event:
    $ pink.otm.start_continuing_event()
    """This event triggers upon entering the room."""
    $ pink.otm.end_current_event()
