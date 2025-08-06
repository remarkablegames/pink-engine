label test_corridor_E18_event:
    $ pink.otm.start_continuing_event()

    # Uncouples followers
    $ pink.otm.uncouple_followers()

    # Hides all but the first follower with fade effect.
    if len(renpy.store.pink_otm_followers) > 1:
        call pink_otm_fade_in(0.2)
        $ _extra_followers_index = 1
        while _extra_followers_index < len(renpy.store.pink_otm_followers):
            $ renpy.store.pink_otm_followers[_extra_followers_index].hide()
            $ _extra_followers_index += 1
        call pink_otm_fade_out(0.2)

    # Gives the follower movement instructions
    if len(renpy.store.pink_otm_followers) > 0:
        $ renpy.store.pink_otm_followers[0].control_stack = [
            pink.otm.ControlCommand("go_to_smart",target=(3, 5), never_repeat=True),
            pink.otm.ControlCommand("go_to_smart",target=(1, 5), never_repeat=True),
            pink.otm.ControlCommand("turn_right", never_repeat=True)]

    # Wait for movement commands to be carried out
    if len(renpy.store.pink_otm_followers) == 1:
        $ pink.otm.initiate_event_wait()
        $ pink.otm.add_movement_wait(renpy.store.pink_otm_followers[0], x_coord=1, y_coord=5, orientation="right")
        call pink_otm_event_wait

    """This event serves as a sample of how to control followers during an event.

    This event has movement instructions for one follower. Any additional followers are hidden during the
    event and re-revealed afterwards"""

    # Teleports followers to player at end of function
    if len(renpy.store.pink_otm_followers) > 1:
        call pink_otm_fade_in(0.2)
        $ pink.otm.reveal_all_followers()
        $ pink.otm.teleport_followers_to_player()
        call pink_otm_fade_out(0.2)
    $ pink.otm.end_current_event()
