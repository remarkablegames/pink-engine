label test_corridor_A24_sign:
    $ pink.otm.start_continuing_event()
    """This room exists to test events that behave differently depending on the button you pressed to start those
    events. The NPC in this room will tell you which button you pressed to trigger the event."""
    $ pink.otm.end_current_event()

label test_corridor_A24_youth:
    $ pink.otm.start_continuing_event()
    if pink_otm_event_button == ('keyboard', pygame.K_SPACE):
        "Youth" "You started this interaction by pressing the space button on your keyboard."
    elif pink_otm_event_button == ('keyboard', pygame.K_RETURN):
        "Youth" "You started this interaction by pressing the enter button on your keyboard."
    elif pink_otm_event_button == ('mouse', 1):
        "Youth" "You started this interaction by pressing the left button on your mouse."
    elif pink_otm_event_button == ('controller', 'pad_a_press'):
        "Youth" "You started this interaction by pressing the 'a' key on your gamepad."
    elif pink_otm_event_button == ('controller', 'pad_righttrigger_pos'):
        "Youth" "You started this interaction by pressing the right trigger key on your gamepad."
    else:
        "Youth" "You added new keys to trigger this event, because I have no idea what key this is."
    $ pink.otm.end_current_event()
