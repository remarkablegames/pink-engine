init python:
    config.per_frame_screens.append('pink_otm_map')

# pink_otm_standard_parallel_processes lists parallel process classes that are automatically initiated for every map.
default pink_otm_standard_parallel_processes = [
    pink.otm.SmoothZoomController]

# pink_otm_parallel_pause specifies which parallel processes should automatically be paused at the start of dynamic and
#  continous events and unpaused at the end. During static events, all parallel processes are paused by default.
default pink_otm_parallel_pause = ["conditional_event_triggers"]

# pink_otm_force_run forces the player to run at all times. pink_otm_forbid_run prevents the player from running at any
#  time.
default pink_otm_force_run = False
default pink_otm_forbid_run = False

# Sets the nearest value on pink otm map. Useful to set to True if you've got very zoomed in maps, to prevent some
# degree of blur, but causes some lack of fidelity at standard zoom levels.
default pink_otm_nearest = False

##### These variables determine the pink engine's reaction to key presses. #####
# pink_otm_gamepad_functions identifies the gamepad buttons that correspond to functions to be executed when the button
#  is either pressed or released.
default pink_otm_gamepad_functions = {
    'pad_a_press': pink.otm.OrthogonalTiledMap.player_interaction,
    'pad_righttrigger_pos': pink.otm.OrthogonalTiledMap.player_interaction,
    'pad_b_press': pink.otm.OrthogonalTiledMap.run_key_down,
    'pad_b_release': pink.otm.OrthogonalTiledMap.run_key_up,

    'pad_leftx_neg': pink.otm.OrthogonalTiledMap._left_movement_key_down_gamepad,
    'pad_leftx_zero': pink.otm.OrthogonalTiledMap._left_right_movement_key_up_gamepad,
    'pad_leftx_pos': pink.otm.OrthogonalTiledMap._right_movement_key_down_gamepad,
    'pad_lefty_neg': pink.otm.OrthogonalTiledMap._up_movement_key_down_gamepad,
    'pad_lefty_zero': pink.otm.OrthogonalTiledMap._up_down_movement_key_up_gamepad,
    'pad_lefty_pos': pink.otm.OrthogonalTiledMap._down_movement_key_down_gamepad,

    'pad_rightx_neg': pink.otm.OrthogonalTiledMap._left_turn_gamepad,
    'pad_rightx_pos': pink.otm.OrthogonalTiledMap._right_turn_gamepad,
    'pad_righty_neg': pink.otm.OrthogonalTiledMap._up_turn_gamepad,
    'pad_righty_pos': pink.otm.OrthogonalTiledMap._down_turn_gamepad}

# pink_otm_gamepad_turning_axis identifies the gamepad axes that correspond to movement.
default pink_otm_gamepad_movement_axis = {
    'leftx': 'horizontal', 'lefty': 'vertical'}

# pink_otm_gamepad_turning_axis identifies the gamepad axes that correspond to turning in place.
default pink_otm_gamepad_turning_axis = {
    'rightx': 'horizontal', 'righty': 'vertical'}

# pink_otm_gamepad_held_keys identifies the gamepad buttons that correspond to functions to be executed when
#  those buttons are held
default pink_otm_gamepad_held_keys = {
    'b': pink.otm.OrthogonalTiledMap.start_running}

# pink_otm_mouse_button_down_functions identifies the mouse buttons that correspond to functions to be executed when
#  those buttons are pressed
default pink_otm_mouse_button_down_functions = {
#     1: pink.otm.OrthogonalTiledMap.player_interaction
    1: pink.otm.OrthogonalTiledMap.click_on_map
    }

# pink_otm_mouse_button_up_functions identifies the mouse buttons that correspond to functions to be executed when
#  those buttons are released
default pink_otm_mouse_button_up_functions = {
    1: pink.otm.OrthogonalTiledMap.unclick_on_map}

# pink_otm_key_down_functions identifies the keyboard keys that correspond to functions to be executed when those keys
#  are pressed.
default pink_otm_key_down_functions = {
    pygame.K_SPACE: pink.otm.OrthogonalTiledMap.player_interaction,
    pygame.K_RETURN: pink.otm.OrthogonalTiledMap.player_interaction,
    pygame.K_RSHIFT: pink.otm.OrthogonalTiledMap.run_key_down,
    pygame.K_LSHIFT: pink.otm.OrthogonalTiledMap.run_key_down,
    pygame.K_o: pink.otm.OrthogonalTiledMap.console_key_down}

# pink_otm_key_up_functions identifies the keyboard keys that correspond to functions to be executed when those keys
#  are released.
default pink_otm_key_up_functions = {
    pygame.K_RSHIFT: pink.otm.OrthogonalTiledMap.run_key_up,
    pygame.K_LSHIFT: pink.otm.OrthogonalTiledMap.run_key_up}

# pink_otm_key_held_functions identifies the keyboard keys that correspond to functions to be executed while those keys
# are held.
default pink_otm_key_held_functions = {
    pygame.K_RSHIFT: pink.otm.OrthogonalTiledMap.start_running,
    pygame.K_LSHIFT: pink.otm.OrthogonalTiledMap.start_running}

# pink_otm_movement_keys identifies the keyboard keys that correspond to movement directions.
default pink_otm_movement_keys = {
    pygame.K_DOWN: 'down', pygame.K_s: 'down',
    pygame.K_UP: 'up', pygame.K_w: 'up',
    pygame.K_LEFT: 'left', pygame.K_a: 'left',
    pygame.K_RIGHT: 'right', pygame.K_d: 'right'}

# pink_otm_event_type_functions identifies the functions to be called when ren'py events are generated that correspond
#  to key presses on various hardware devices (mouse, keyboard, gamepad) are pressed. The keys are the events, whereas
#  the values are the corresponding functions
default pink_otm_event_type_functions = {
    pygame.KEYDOWN: pink.otm.OrthogonalTiledMap.event_key_down,
    pygame.KEYUP: pink.otm.OrthogonalTiledMap.event_key_up,
    pygame.MOUSEBUTTONDOWN: pink.otm.OrthogonalTiledMap.event_mouse_button_down,
    pygame.MOUSEBUTTONUP: pink.otm.OrthogonalTiledMap.event_mouse_button_up,
    pygame.MOUSEMOTION: pink.otm.OrthogonalTiledMap.event_mouse_move,
    renpy.display.core.EVENTNAME: pink.otm.OrthogonalTiledMap.event_gamepad}

# If pink_otm_alt_turning_enabled is enabled, the player character will turn in place if alt is held while movement
#  keys are pressed.
default pink_otm_alt_turning_enabled = True

#### These variables are used to initiate objects ####
# pink_otm_pc_init_dict is the Tiled-like dictionary used to initiate the Player Character.
default pink_otm_pc_init_dict = {
    "properties": [
        {"name": "sprite_collection_path", "type": "string", "value": pink_otm_default_sprite},
        {"name": "repeat_commands", "type": "bool", "value": False},
        {"name": "movement_speed", "type": "float", "value": pink_otm_default_pc_walk_speed},
        {"name": "quick_movement_animation", "type": "str", "value": "run"},
        {"name": "default_movement_animation", "type": "str", "value": "walk"},
        {"name": "ref_name", "type": "str", "value": "pink_otm_current_pc"},
        {"name": "movement_sound_function", "type": "str", "value": pink_player_default_movement_sound_function},
        {"name": "movement_sound", "type": "str", "value": pink_player_default_movement_sound},
        {"name": "movement_sound_blocked", "type": "str", "value": pink_player_default_movement_sound_blocked},
        {"name": "movement_sound_multiplier", "type": "float", "value": 1.0}]}

# pink_otm_camera_drone_init_dict is the Tiled-like dictionary used to initiate the Camera Drone
default pink_otm_camera_drone_init_dict = {
    "properties": [
        {"name": "sprite_collection_path", "type": "string",
         "value": "pink_engine/sprite_collections/empty_sprite_collection.json"},
        {"name": "can_always_move", "type": "bool", "value": True},
        {"name": "repeat_commands", "type": "bool", "value": False},
        {"name": "stand_animation", "type": "string", "value": "exist"},
        {"name": "move_animation", "type": "string", "value": "exist"},
        {"name": "ref_name", "type": "str", "value": "pink_otm_camera_drone"},
        {"name": "ignores_special_movement", "type": "bool", "value": True}]}

# Keeps track of game time.
default otm_timer = pink.tm.GameTimer()

########################################################################################################################
## THE VARIABLES BELOW THIS LINE ARE ALL AUTOMATICALLY SET BY VARIOUS PINK ENGINE PROCESSES, AND SHOULD NOT BE        ##
## MANUALLY EDITED. DOING SO CAN RESULT IN UNEXPECTED BEHAVIOR AND CRASHES.                                           ##
########################################################################################################################

###### These variables are automatically set during the loading of the map #######
# pink_otm_current_map always points to the current OTM map, and can be used to target that map in ren'py and python
# scripts. If no map is currently displayed, this variable is set to None.
default pink_otm_current_map = None

# pink_otm_current_camera always points to the current camera object, and can be used to target that camera in ren'py
# and python scripts.
default pink_otm_current_camera = None

# pink_otm_loading_map points to whatever OTM map is currently being loaded, and can be used to target that map.
# If no OTM map is currently being loaded, this variable is set to None.
default pink_otm_loading_map = None

##### These variables are used to cache ren'py settings that are overridden for one reason or another. #####
# pink_otm_rollback_restore is the cache for the rollback_enabled ren'py config setting. Rollback is always disabled
# while an OTM map is active, as keeping a memory of previous OTM states would significantly slow down the engine.
# Rollback is restored to prior settings once the player enters an event (Note: This can cause issues with dynamic and
# continuous events, and should be kept in mind when designing those).
default pink_otm_rollback_restore = None

# pink_otm_window_hide_cache is the cache for the window_hide_transition ren'py config setting. This setting is
# overridden by the force_instant_transition_on_event_end function, with this cache variable used to restore it after
# the end of the next event.
default pink_otm_window_hide_cache = None

# pink_otm_autosave_on_choice_cache is the cache for the autosave_on_choice ren'py config setting. This setting is
# overriden while an OTM map is active, as saving an OTM map takes significantly more time than most ren'py screens,
# causing significant bursts of slowdown while using menus in OTM events. autosave_on_choice is restored to prior
# settings if OTM mode is left.
default pink_otm_autosave_on_choice_cache = None

###### These variables are automatically set by the smooth zoom controller #####
# Current zoom controller. Used to address the zoom controller during events.
default pink_otm_zoom_controller = None

# These two variables are used to carry over the current zoom level between maps.
default pink_otm_camera_current_xzoom = pink_otm_camera_default_zoom
default pink_otm_camera_current_yzoom = pink_otm_camera_default_zoom

##### These variables are automatically set by the event-triggering functions. #####
# pink_otm_event_trigger always points to whatever object triggered the current event, and can be used to target
# that object during the event. If no event is active, this variable defaults to None.
default pink_otm_event_trigger = None

# pink_otm_event_button always points to the button used to initialize the current event. It can be used to implement
# different behavior depending on the button used to interact with a target. If no event is active, this variable
# defaults to None
default pink_otm_event_button = None

# If a ren'py event is called through OTM maps, that event's label is assigned to the pink_otm_current_event_name
# variable. If no event is active, this variable defaults to None.
default pink_otm_current_event_name = None

# pink_otm_current_event_type contains the type of the currently active Pink OTM event. This can be either 'static',
# 'dynamic' or 'continuous'. If no event is active, this variable defaults to None.
default pink_otm_current_event_type = None

# pink_otm_event_interaction_reaction is a boolean that is set at the start of the event, indicating whether an
# automated reaction was given (such as an NPC turning to the player) to start off the event. This is used to roll back
# that reaction when the event is ended.
default pink_otm_event_interaction_reaction = None

##### These variable are automatically set by the go_to_map function #####
# pink_map_transition_in points at the transition to use during the next transition to an OTM map.
default pink_map_transition_in = None

# pink_map_transition_in_sound points at the sound file to play during the next transition to an OTM map.
default pink_map_transition_in_sound = None

##### These variables are automatically filled in by the leave_otm function ####
# otm_return_map_path contains the map the PC should be placed when the function return_to_otm is called.
default otm_return_map_path = None

# otm_return_coords contains the coordinates the PC should be placed when the function return_to_otm is called.
default otm_return_coords = None

# otm_return_orientation contains the orientation the PC should have when the function return_to_otm is called.
default otm_return_orientation = None

##### These variables are automatically filled in by standard events #####
# _pink_tempvars is a workaround to use in standard events to contain label variables after the call to the standard
# event label is popped off the call stack (which normally pop all label variables)
default _pink_tempvars = {}

##### Followers ####
# pink_otm_followers contains a list of all the player character's current follower objects.
default pink_otm_followers = []

#### Movement ####
# pink_otm_current_walk_speed is used to keep track of the player walk speed, so it can be restored when they stop
#  running.
default pink_otm_current_walk_speed = pink_otm_default_pc_walk_speed

# pink_otm_current_run_speed is used to keep track of the player run speed, so it can be restored when they stop
#  walking.
default pink_otm_current_run_speed = pink_otm_default_pc_run_speed

#### Sound ####
default pink_sound_manager = pink.PinkSoundManager()

label pink_otm_event_wait:
    $ pink.otm.start_event_wait()
    while pink_otm_current_map.current_event_wait is not None:
        $ ui.pausebehavior(0.03)
        $ ui.interact()
    $ renpy.restart_interaction()