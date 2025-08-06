label test_corridor_E16_event:
    $ pink.otm.start_continuing_event()
    call pink_otm_fade_in(0.2)
    $ test_corridor_E16_npc1 = pink.otm.spawn_sprite_collection(
        sprite_collection_path="pink_engine/sprite_collections/sevarihk green blob.json",
        x_coord=5, y_coord=5, orientation="left")
    $ test_corridor_E16_npc2 = pink.otm.spawn_sprite_collection(
        sprite_collection_path="pink_engine/sprite_collections/sevarihk green blob.json",
        x_coord=1, y_coord=5, orientation="right")
    call pink_otm_fade_out(0.2)

    """This room is a copy of the scene from E15, except with minor fade effects as the NPCs appear and disappear."""

    $ test_corridor_E16_npc1.control_stack = [
        pink.otm.ControlCommand("go_to",target=(3, 3), never_repeat=True),
        pink.otm.ControlCommand("turn_down", never_repeat=True)]
    $ test_corridor_E16_npc2.control_stack = [
        pink.otm.ControlCommand("go_to",target=(3, 7), never_repeat=True),
        pink.otm.ControlCommand("turn_up", never_repeat=True)]

    "Note that this is not a ren'py transition effect."
    """As the pink engine does not transition between events outside of map switches, ren'py transitions are hard
    to align with pink engine effects."""
    "Instead, the pink engine has its own set of fade and shake effects for use in cutscenes."
    "More examples of this can be found in room E29"

    $ pink.otm.initiate_event_wait()
    $ pink.otm.add_movement_wait(test_corridor_E16_npc1, x_coord=3, y_coord=3, orientation="down", finished=True)
    $ pink.otm.add_movement_wait(test_corridor_E16_npc2, x_coord=3, y_coord=7, orientation="up", finished=True)
    call pink_otm_event_wait

    call pink_otm_fade_in(0.2)
    $ test_corridor_E16_npc1.hide()
    $ test_corridor_E16_npc2.hide()
    call pink_otm_fade_out(0.2)
    $ pink.otm.end_current_event()
