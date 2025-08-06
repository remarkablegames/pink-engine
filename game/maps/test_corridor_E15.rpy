label test_corridor_E15_event:
    $ pink.otm.start_continuing_event()
    $ test_corridor_E15_npc1 = pink.otm.spawn_sprite_collection(
        sprite_collection_path="pink_engine/sprite_collections/sevarihk green blob.json",
        x_coord=5, y_coord=5, orientation="left")
    $ test_corridor_E15_npc2 = pink.otm.spawn_sprite_collection(
        sprite_collection_path="pink_engine/sprite_collections/sevarihk green blob.json",
        x_coord=1, y_coord=5, orientation="right")

    """Two NPCs are spawned as part of this event. They are not conditional map objects, but are created through
    a function called in the event itself."""

    $ test_corridor_E15_npc1.control_stack = [
        pink.otm.ControlCommand("go_to",target=(3, 3), never_repeat=True),
        pink.otm.ControlCommand("turn_down", never_repeat=True)]
    $ test_corridor_E15_npc2.control_stack = [
        pink.otm.ControlCommand("go_to",target=(3, 7), never_repeat=True),
        pink.otm.ControlCommand("turn_up", never_repeat=True)]

    """These NPCs can be given movement instructions like any other NPC."""

    $ pink.otm.initiate_event_wait()
    $ pink.otm.add_movement_wait(test_corridor_E15_npc1, x_coord=3, y_coord=3, orientation="down", finished=True)
    $ pink.otm.add_movement_wait(test_corridor_E15_npc2, x_coord=3, y_coord=7, orientation="up", finished=True)
    call pink_otm_event_wait

    """This functionality is only intended for use in cutscenes, and any NPC created in this manner should be hidden
    away at the end of the cutscene using the hide() function."""

    $ test_corridor_E15_npc1.hide()
    $ test_corridor_E15_npc2.hide()
    $ pink.otm.end_current_event()
