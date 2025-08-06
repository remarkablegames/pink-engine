label test_corridor_E17_event:
    $ pink.otm.start_continuing_event()

    if len(renpy.store.pink_otm_followers) > 1:
        call pink_otm_fade_in(0.2)
        $ pink.otm.hide_all_followers()
        call pink_otm_fade_out(0.2)

    """This event serves as a sample of how to hide followers during an event."""

    # Teleports followers to player at end of function
    if len(renpy.store.pink_otm_followers) > 1:
        call pink_otm_fade_in(0.2)
        $ pink.otm.reveal_all_followers()
        $ pink.otm.teleport_followers_to_player()
        call pink_otm_fade_out(0.2)
    $ pink.otm.end_current_event()
