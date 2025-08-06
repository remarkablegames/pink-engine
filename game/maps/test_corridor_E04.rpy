default test_corridor_E04_npc_01_triggered = False
default test_corridor_E04_npc_02_triggered = False
default test_corridor_E04_npc_03_triggered = False
default test_corridor_E04_npc_04_triggered = False
default test_corridor_E04_npc_05_triggered = False
default test_corridor_E04_npc_06_triggered = False

label test_corridor_E04_npc_01:
    $ pink.otm.start_continuing_event()

    # Wait for player to complete move
    $ pink.otm.initiate_event_wait()
    $ pink.otm.add_movement_wait(pink_otm_current_pc, finished=True)
    call pink_otm_event_wait

    $ pink_otm_walk_up_to_character(test_corridor_E04_npc01, pink_otm_current_pc)
    $ pink.otm.initiate_event_wait()
    $ pink.otm.add_movement_wait(test_corridor_E04_npc01, finished=True)
    call pink_otm_event_wait

    if not test_corridor_E04_npc_01_triggered:
        "Trainer" "Hey! Let's get out our miniaturized pets and have them fight for our entertainment!"
        "Trainer" "You don't have any?"
        "Trainer" "Aw man..."
    else:
        "Trainer" "Look, you already told me you don't have miniaturizable battle pets."
        "Trainer" "Come back once you're with the times."
    $ test_corridor_E04_npc_01_triggered = True
    $ pink.otm.end_current_event()

label test_corridor_E04_npc_02:
    $ pink.otm.start_continuing_event()

    # Wait for player to complete move
    $ pink.otm.initiate_event_wait()
    $ pink.otm.add_movement_wait(pink_otm_current_pc, finished=True)
    call pink_otm_event_wait

    $ pink_otm_walk_up_to_character(test_corridor_E04_npc02, pink_otm_current_pc)
    $ pink.otm.initiate_event_wait()
    $ pink.otm.add_movement_wait(test_corridor_E04_npc02, finished=True)
    call pink_otm_event_wait

    if not test_corridor_E04_npc_02_triggered:
        "Trainer" "Finally, someone to challenge!"
        "Trainer" "You don't have any battle pets?"
        "Trainer" "Where else am I gonna find someone to challenge?"
    else:
        "Trainer" "Where else am I gonna find someone to challenge?"
    $ test_corridor_E04_npc_02_triggered = True
    $ pink.otm.end_current_event()

label test_corridor_E04_npc_03:
    $ pink.otm.start_continuing_event()

    # Wait for player to complete move
    $ pink.otm.initiate_event_wait()
    $ pink.otm.add_movement_wait(pink_otm_current_pc, finished=True)
    call pink_otm_event_wait

    $ pink_otm_walk_up_to_character(test_corridor_E04_npc03, pink_otm_current_pc)
    $ pink.otm.initiate_event_wait()
    $ pink.otm.add_movement_wait(test_corridor_E04_npc03, finished=True)
    call pink_otm_event_wait

    if not test_corridor_E04_npc_03_triggered:
        "Trainer" "I see you have overcome my compatriots!"
        "Trainer" "You will find me a much more challenging enemy!"
        "Trainer" "Oh."
    else:
        "Trainer" "What kind of person doesn't carry his own private squadron of magical beasts?"
    $ test_corridor_E04_npc_03_triggered = True
    $ pink.otm.end_current_event()

label test_corridor_E04_npc_04:
    $ pink.otm.start_continuing_event()

    # Wait for player to complete move
    $ pink.otm.initiate_event_wait()
    $ pink.otm.add_movement_wait(pink_otm_current_pc, finished=True)
    call pink_otm_event_wait

    $ pink_otm_walk_up_to_character(test_corridor_E04_npc04, pink_otm_current_pc)
    $ pink.otm.initiate_event_wait()
    $ pink.otm.add_movement_wait(test_corridor_E04_npc04, finished=True)
    call pink_otm_event_wait

    if not test_corridor_E04_npc_04_triggered:
        "Minotaur" "Oh hey there, fellow monster! Would you like to have our miniaturizable battle humans fight?"
        "Minotaur" "Oh, you are a human? Well, never mind then, I guess."
    else:
        "Minotaur" "I think I need glasses..."
    $ test_corridor_E04_npc_04_triggered = True
    $ pink.otm.end_current_event()

label test_corridor_E04_npc_05:
    $ pink.otm.start_continuing_event()

    # Wait for player to complete move
    $ pink.otm.initiate_event_wait()
    $ pink.otm.add_movement_wait(pink_otm_current_pc, finished=True)
    call pink_otm_event_wait

    $ pink_otm_walk_up_to_character(test_corridor_E04_npc05, pink_otm_current_pc)
    $ pink.otm.initiate_event_wait()
    $ pink.otm.add_movement_wait(test_corridor_E04_npc05, finished=True)
    call pink_otm_event_wait

    if not test_corridor_E04_npc_05_triggered:
        "Trainer" "You will never get the badge!"
        "Trainer" "Get out your team, and I will show you your place!"
        "Trainer" "..."
        "Trainer" "Well? I'm waiting."
    else:
        "Trainer" "Man, what is it with teens today? Don't even have battle monster teams."
    $ test_corridor_E04_npc_05_triggered = True
    $ pink.otm.end_current_event()

label test_corridor_E04_npc_06:
    $ pink.otm.start_continuing_event()

    # Wait for player to complete move
    $ pink.otm.initiate_event_wait()
    $ pink.otm.add_movement_wait(pink_otm_current_pc, finished=True)
    call pink_otm_event_wait

    $ pink_otm_walk_up_to_character(test_corridor_E04_npc06, pink_otm_current_pc)
    $ pink.otm.initiate_event_wait()
    $ pink.otm.add_movement_wait(test_corridor_E04_npc06, finished=True)
    call pink_otm_event_wait

    if not test_corridor_E04_npc_06_triggered:
        "Trainer" "Look, I saw you don't actually have a team."
        "Trainer" "But it's still policy to walk up to you like this, acting all challenging."
    else:
        "Trainer" "I don't write the rules, I just follow 'em."
    $ test_corridor_E04_npc_06_triggered = True
    $ pink.otm.end_current_event()

label test_corridor_E04_sign_01:
    $ pink.otm.start_continuing_event()
    """This room tests arbitrary code triggers that are used to detect when an NPC has you in his sights.

    Each of the minotaurs in this room can see ten squares ahead in a straight line. Unlike the previous rooms, these
    minotaurs care not for line of sight, and can see through pillars."""
    $ pink.otm.end_current_event()

label test_corridor_E04_sign_02:
    $ pink.otm.start_continuing_event()
    """Congratulations, you have earned the testing room badge!

    With this badge, miniaturizable battle humans up to level 6 will listen to your orders in battle."""
    $ pink.otm.end_current_event()