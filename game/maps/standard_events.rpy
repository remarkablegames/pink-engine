default super_quick_fade = Dissolve(0.025)
default quick_fade = Dissolve(0.1)

default pink_otm_hop_noise = "music/hop.wav"
default pink_otm_terrain_noises = {
    "metal": 'music/steps_metal.wav',
    "sand": 'music/steps_sand.mp3',
    "stone": 'music/steps_stone.ogg'
}

init python:
    # Default pursuit speed.
    pink_otm_def_pursuit_speed = 0.11

    def pink_return_merged_dict(a, b):
        """
        Merges the two given dictionaries and returns the result.
        :param dict a: The first given dictionary.
        :param dict b: The second given dictionary.
        :rtype: dict
        """
        c = a.copy()
        c.update(b)
        return c

    def pink_movement_sound_terrain(moving_npc, x_coord, y_coord, can_move):
        if can_move:
            sound_tag = pink_otm_current_map.base_grid.get_sound_tag(x_coord, y_coord)
            movement_sound = pink_otm_terrain_noises.get(sound_tag)
        else:
            movement_sound = moving_npc.movement_sound_blocked
        if movement_sound is not None:
            pink_sound_manager.play_sound(
                sound_file=movement_sound,
                max_volume=moving_npc.movement_sound_multiplier,
                min_volume_distance=moving_npc.movement_sound_max_distance,
                emitter=moving_npc)

    def pink_movement_sound_static(moving_npc, x_coord, y_coord, can_move):
        if can_move:
            movement_sound = moving_npc.movement_sound
        else:
            movement_sound = moving_npc.movement_sound_blocked
        if movement_sound is not None:
            pink_sound_manager.play_sound(
                sound_file=movement_sound,
                max_volume=moving_npc.movement_sound_multiplier,
                min_volume_distance=moving_npc.movement_sound_max_distance,
                emitter=moving_npc)

    def pink_otm_walk_up_to_character(moving_npc, target_character):
        """
        Makes the given Sprite collection (such as an NPC) move up to the target object.
        :param OrthogonalTiledMapGameObjectSpriteCollection moving_npc: the object that is to move.
        :param str|OrthogonalTiledMapGameObject|tuple target_character: the object that is to be moved up to,
        the ref_name for such an object, or the coordinate to be moved up to.
        """
        target_coord = pink.otm.get_walk_up_target(origin=moving_npc, goal=target_character)
        moving_npc.control_stack = [
            pink.otm.ControlCommand(
                "go_to_smart", target=target_coord, never_repeat=True),
            pink.otm.ControlCommand(
                "turn_to", target=target_character.central_coord, never_repeat=True, movement_time=0.01)]

    def pink_otm_pursuit_script(target_npc, pursuit_speed=pink_otm_def_pursuit_speed):
        """
        Makes the given NPC pursue the PC.
        :param OrthogonalTiledMapGameObjectSpriteCollection moving_npc: the sprite collection object that is to pursue
        the PC
        :param float pursuit_speed: The speed at which the object is to pursue the PC. Speed is the time per movement
        in seconds, so the lower the value, the higher the speed.
        """
        target_npc.interrupt_delay()  # interrupt any delays
        target_npc.set_state('pursuing', 1)
        target_npc.control_stack = [
            pink.otm.ControlCommand(
                "go_to_smart", target='pink_otm_current_pc', ignore_elements=["pink_otm_current_pc"],
                movement_time=pursuit_speed, never_repeat=True)]

    def pink_otm_cease_pursuit_script(target_npc, return_coord):
        """
        Makes the given NPC stop pursuing the PC and return to the given coordinates.
        :param OrthogonalTiledMapGameObjectSpriteCollection target_npc: the sprite collection object that is to stop
        pursuing the PC
        :param tuple return_coord: The given coordinate to return to.
        """
        target_npc.set_state('pursuing', 0)
        target_npc.control_stack = [
            pink.otm.ControlCommand("go_to_smart", target=return_coord, never_repeat=True)]

    def pink_otm_pursuit_and_reset(
            npc, engage_variable, pursuit_speed=pink_otm_def_pursuit_speed
    ):
        """
        Adds a conditional code trigger to the current OTM map that makes the given NPC pursue the PC once the
        given variable is set to True. Once the variable is set to False, the NPC will teleport back to their starting
        point.
        :param OrthogonalTiledMapGameObjectSpriteCollection npc: the sprite collection object that is to pursue
        the PC
        :param str engage_variable: The name of the variable to check for. It should be a variable in the ren'py store.
        :param float pursuit_speed: The speed at which the object is to pursue the PC. Speed is the time per movement
        in seconds, so the lower the value, the higher the speed.
        """
        pink.otm.ConditionalCodeTriggers.add_condition(
            condition="""getattr(renpy.store, '{variable_name}') and not get_map_object({ref_id}).get_state('pursuing')""".format(ref_id=npc.map_id, variable_name=engage_variable),
            event_code="""renpy.store.pink_otm_pursuit_script(get_map_object({ref_id}), {pursuit_speed})""".format(ref_id=npc.map_id, pursuit_speed=pursuit_speed))
        pink.otm.ConditionalCodeTriggers.add_condition(
            condition="""get_map_object({ref_id}).get_state('pursuing') == 1 and not getattr(renpy.store, '{variable_name}')""".format(ref_id=npc.map_id, variable_name=engage_variable),
            event_code="""get_map_object({ref_id}).control_stack = [];get_map_object({ref_id}).set_state('pursuing', 0);get_map_object({ref_id}).set_to_coords({x}, {y})""".format(ref_id=npc.map_id, x=npc.central_coord.x, y=npc.central_coord.y))

    def pink_otm_pursuit_range(
            npc, engage_range, disengage_range=None, pursuit_speed=pink_otm_def_pursuit_speed, in_view=True
    ):
        """
        Adds a conditional code trigger to the current OTM map that makes the given NPC pursue the PC once the PC
        gets within a given range. If a disengage_range is given, adds a second conditional code trigger that makes
        the NPC stop pursuing once the PC gets beyond a certain range.
        :param OrthogonalTiledMapGameObjectSpriteCollection npc: the sprite collection object that is to pursue
        the PC
        :param int engage_range: The range at which to start pursuing the player. Range is measured in difference
        between central coordinates.
        :param int disengage_range: The range at which to stop pursuing the player.
        :param float pursuit_speed: The speed at which the object is to pursue the PC. Speed is the time per movement
        in seconds, so the lower the value, the higher the speed.
        :param bool in_view: If True, will only start pursuing if the PC has unobstructed sight of the PC. When to
        stop pursuing is not affected.
        """
        pink.otm.ConditionalCodeTriggers.add_condition(
            condition="""not get_map_object({ref_id}).get_state('pursuing') and is_in_range(viewer=get_map_object({ref_id}), view_range={engage_range}, in_view={in_view}, include_touched_coords=False)""".format(ref_id=npc.map_id, engage_range=engage_range, in_view=in_view),
            event_code="""renpy.store.pink_otm_pursuit_script(get_map_object({ref_id}), {pursuit_speed})""".format(ref_id=npc.map_id, pursuit_speed=pursuit_speed))
        if disengage_range is not None:
            pink.otm.ConditionalCodeTriggers.add_condition(
                condition="""get_map_object({ref_id}).get_state('pursuing') == 1 and not is_in_range(viewer=get_map_object({ref_id}), view_range={disengage_range}, in_view=False)""".format(ref_id=npc.map_id, disengage_range=disengage_range),
                event_code="""renpy.store.pink_otm_cease_pursuit_script(get_map_object({ref_id}), {central_coord})""".format(ref_id=npc.map_id, central_coord=npc.central_coord))

    def pink_otm_pursuit_cone(
            npc, engage_range, disengage_range=None, pursuit_speed=pink_otm_def_pursuit_speed, in_view=True
    ):
        """
        Adds a conditional code trigger to the current OTM map that makes the given NPC pursue the PC once the PC
        gets within a given cone. If a disengage_range is given, adds a second conditional code trigger that makes
        the NPC stop pursuing once the PC gets beyond a certain range.
        :param OrthogonalTiledMapGameObjectSpriteCollection moving_npc: the sprite collection object that is to pursue
        the PC
        :param int engage_range: The range at which to start pursuing the player. Range is measured in difference
        between central coordinates.
        :param int disengage_range: The range at which to stop pursuing the player. Note that disengagement only looks
        at total distance, not the view cone.
        :param float pursuit_speed: The speed at which the object is to pursue the PC. Speed is the time per movement
        in seconds, so the lower the value, the higher the speed.
        :param bool in_view: If True, will only start pursuing if the PC has unobstructed sight of the PC. When to
        stop pursuing is not affected.
        """
        pink.otm.ConditionalCodeTriggers.add_condition(
            condition="""not get_map_object({ref_id}).get_state('pursuing') and is_in_cone(viewer=get_map_object({ref_id}), view_range={engage_range}, in_view={in_view})""".format(ref_id=npc.map_id, engage_range=engage_range, in_view=in_view),
            event_code="""renpy.store.pink_otm_pursuit_script(get_map_object({ref_id}), {pursuit_speed})""".format(ref_id=npc.map_id, pursuit_speed=pursuit_speed))
        if disengage_range is not None:
            pink.otm.ConditionalCodeTriggers.add_condition(
                condition="""get_map_object({ref_id}).get_state('pursuing') == 1 and not is_in_range(viewer=get_map_object({ref_id}), view_range={disengage_range}, in_view=False)
                """.format(ref_id=npc.map_id, disengage_range=disengage_range),
                event_code="""renpy.store.pink_otm_cease_pursuit_script(get_map_object({ref_id}), {central_coord})""".format(ref_id=npc.map_id, central_coord=npc.central_coord))

    def pink_otm_pursuit_line(
            npc, engage_range, disengage_range=None, pursuit_speed=pink_otm_def_pursuit_speed, in_view=True
    ):
        """
        Adds a conditional code trigger to the current OTM map that makes the given NPC pursue the PC once the PC
        gets within a given line . If a disengage_range is given, adds a second conditional code trigger that makes
        the NPC stop pursuing once the PC gets beyond a certain range.
        :param OrthogonalTiledMapGameObjectSpriteCollection moving_npc: the sprite collection object that is to pursue
        the PC
        :param int engage_range: The range at which to start pursuing the player. Range is measured in difference
        between central coordinates.
        :param int disengage_range: The range at which to stop pursuing the player. Note that disengagement only looks
        at total distance, not the view line.
        :param float pursuit_speed: The speed at which the object is to pursue the PC. Speed is the time per movement
        in seconds, so the lower the value, the higher the speed.
        :param bool in_view: If True, will only start pursuing if the PC has unobstructed sight of the PC. When to
        stop pursuing is not affected.
        """
        pink.otm.ConditionalCodeTriggers.add_condition(
            condition="""not get_map_object({ref_id}).get_state('pursuing') and is_in_line(viewer=get_map_object({ref_id}), view_range={engage_range}, in_view={in_view})""".format(ref_id=npc.map_id, engage_range=engage_range, in_view=in_view),
            event_code="""renpy.store.pink_otm_pursuit_script(get_map_object({ref_id}), {pursuit_speed})""".format(ref_id=npc.map_id, pursuit_speed=pursuit_speed))
        if disengage_range is not None:
            pink.otm.ConditionalCodeTriggers.add_condition(
                condition="""get_map_object({ref_id}).get_state('pursuing') == 1 and not is_in_range(viewer=get_map_object({ref_id}), view_range={disengage_range}, in_view=False)""".format(ref_id=npc.map_id, disengage_range=disengage_range),
                event_code="""renpy.store.pink_otm_cease_pursuit_script(get_map_object({ref_id}), {central_coord})""".format(ref_id=npc.map_id, central_coord=npc.central_coord))

label pink_otm_fade_in(fade_time, color="#000000"):
    $ pink.otm.initiate_event_wait()
    $ fade_overlay = pink_otm_current_map._overlay_manager.add_overlay_solid(color, fade_time)  # TODO direct rather than via _overlay_manager
    $ pink.otm.add_alpha_wait(fade_overlay)
    call pink_otm_event_wait
    return

label pink_otm_fade_out(fade_time):
    $ renpy.pause(0.01)
    $ fade_overlay.set_alpha(0.0, fade_time)
    call pink_otm_overlay_alpha_wait(fade_overlay)
    return

label pink_otm_movement_wait(*objects, max_time=None, completion_wait=0.0):
    python:
        pink.otm.initiate_event_wait(max_time=max_time, completion_wait=completion_wait)
        for wait_object in objects:
            pink.otm.add_movement_wait(wait_object)
    call pink_otm_event_wait
    return

label pink_otm_zoom_wait(max_time=None, completion_wait=0.0):
    python:
        pink.otm.initiate_event_wait(max_time=max_time, completion_wait=completion_wait)
        pink.otm.add_zoom_wait()
    call pink_otm_event_wait
    return

label pink_otm_overlay_alpha_wait(*overlays, max_time=None, completion_wait=0.0):
    python:
        pink.otm.initiate_event_wait(max_time=max_time, completion_wait=completion_wait)
        for overlay in overlays:
            pink.otm.add_alpha_wait(overlay)
    call pink_otm_event_wait
    return

label pink_otm_overlay_movement_wait(*overlays, max_time=None, completion_wait=0.0):
    python:
        pink.otm.initiate_event_wait(max_time=max_time, completion_wait=completion_wait)
        for overlay in overlays:
            pink.otm.add_overlay_movement_wait(overlay)
    call pink_otm_event_wait
    return


label pink_otm_transition(
        target_map='', x_coord=0, y_coord=0, orientation=None,
        transition_out=None, transition_in=None,
        transition_delay=0.0,
        transition_out_delay_sound=None, transition_out_sound=None, transition_in_sound=None
    ):
    # This is a functional label, used to run code to transition between maps. It takes the following arguments:
    # target_map (str): Path of the map to go to.
    # x_coord (int): X coordinate to center the player's base on in the new map.
    # y_coord (int): Y coordinate to center the player's base on in the new map.
    # orientation (str): Which way the player should initially face in the new map (left, right, up, down).
    # transition_out (renpy transition): Which transition effect to play between the transition screen and the new map.
    # transition_in (renpy transition): Which transition effect to play between the old map and the transition screen.
    # transition_delay (float): How long to wait before starting the transition_in. Useful to show animation or
    #   ensure a sound effect has time to play.
    # transition_out_delay_sound (str): Path of the sound effect to start playing on the start of the delay
    # transition_out_sound (str): Path of the sound effect to start playing on the start of the transition_out UNTESTED
    # transition_in_sound (str): Path of the sound effect to start playing on the start of the transition_in

    # Because start_continuing_event will pop all the label-specific variables when it pops the call from the stack,
    # a temporary variable is necessary. This variable is to be shared between all standard events.
    $ _pink_tempvars = {
        'target_map': target_map, 'x_coord': x_coord, 'y_coord': y_coord, 'orientation': orientation,
        'transition_out': transition_out, 'transition_in': transition_in,
        'transition_delay': transition_delay,
        'transition_out_delay_sound': transition_out_delay_sound, 'transition_out_sound': transition_out_sound,
        'transition_in_sound': transition_in_sound}
    $ pink.otm.start_continuing_event()

    # Recenters the camera on the player character
    $ pink_otm_current_camera.recenter_on_player()

    # Plays a sound effect that starts at the same time as the delay
    if _pink_tempvars['transition_out_delay_sound'] is not None:
        $ renpy.play(_pink_tempvars['transition_out_delay_sound'], 'audio')

    # Delays before starting the out transition
    if _pink_tempvars['transition_delay'] != 0.0:
        $ renpy.pause(_pink_tempvars['transition_delay'])

    # Shows the transition screen (a black screen)
    scene black
    show screen pink_otm_map
    with None

    # Plays a sound effect that starts at the same time as the out transition
    if _pink_tempvars['transition_out_sound'] is not None:
        $ renpy.play(_pink_tempvars['transition_out_sound'], 'audio')
    # Performs the out transition
    hide screen pink_otm_map with _pink_tempvars['transition_out']

    # Performs the change in map
    $ pink.otm.go_to_map(
        target_map=_pink_tempvars['target_map'], x_coord=_pink_tempvars['x_coord'], y_coord=_pink_tempvars['y_coord'],
        orientation=_pink_tempvars['orientation'], transition_in=_pink_tempvars['transition_in'],
        transition_in_sound=_pink_tempvars['transition_in_sound'])