## ================================================= GENERAL SETTINGS =================================================
## This variable defines screen tag/layer combinations which should freeze pink engine screens when they're up.
define pink_freeze_game_screens = [('menu', 'screens'), ('confirm', 'screens')]

## How large should the text in the pink console be?
define pink_console_text_size = 12

## =================================================== OTM SETTINGS ===================================================

## Default sprite for the pc on orthogonal tiled maps (otm). Should be a path relative to the game folder.
define pink_otm_default_sprite = "pink_engine/sprite_collections/test_player_sprite_collection.json"

## Whether a single tap of the movement key in a direction you are not facing causes your character to move in that
## direction (if True), or only change direction (if False)
define pink_otm_turn_and_move = True

## Whether a character still displays a movement animation when moving in a barred direction
define pink_otm_animate_invalid_move = True

## Movement speed
define pink_otm_default_npc_move_speed = 0.14
define pink_otm_default_pc_walk_speed = 0.14
define pink_otm_default_pc_run_speed = 0.08

## Disables running globally
define pink_otm_disable_run = False

## Default zoom level
define pink_otm_camera_default_zoom = 1.0
define pink_tmd_camera_default_zoom = 1.0

## Viewport settings
define pink_otm_default_viewport_x_offset = 0
define pink_otm_default_viewport_y_offset = 0
define pink_otm_default_viewport_width = config.screen_width
define pink_otm_default_viewport_height = config.screen_height

## Whether to automatically center sprites on tiles if they have been placed along grid lines. Individual sprites can
##  be exempted from autocentering through use of the 'forbid_autocenter' property.
define pink_otm_autocenter_sprites = True

## The animation name used for player movement
define pink_otm_default_walk_animation_name = "walk"
define pink_otm_default_run_animation_name = "run"

## Saving the game while a larger pink engine map is visible takes a fair amount of time, as the entire map needs to
## be put into the save file. This can cause significant lag spikes when gameplay is not paused during saving, such
## as when autosaving during a dialogue choice. As such, config.autosave_on_choice is overridden when a pink engine
## map is visible, preventing autosaves during events. The original config.autosave_on_choice is restored on using
## pink.otm.leave_otm()
define pink_otm_autosave_on_choice = False

## Makes never_repeat True by default during events. This means you won't have to specify on every single control
## command that you don't want them to repeat.
define default_never_repeat_during_event = True

## Default sound drop-off. The tile difference after which a distance-scaled sound is at its minimum volume.
define pink_otm_default_min_volume_distance = 30

## Default panning dropoff. The tile difference after which a distance-panned sound has reached its maximum panning.
define pink_otm_default_max_pan_distance = 20

## Default movement sound function for the player. You can pick between 'pink_movement_sound_terrain'
## and 'pink_movement_sound_static', with the former being terrain-sensitive (utilizing the pink_otm_terrain_noises
## dictionary from standard_events.rpy), and the latter being static (always playing the
## pink_player_default_movement_sound if the player can move, or pink_player_movement_default_sound_blocked if not).
define pink_player_default_movement_sound_function = 'pink_movement_sound_terrain'
define pink_follower_default_movement_sound_function = 'pink_movement_sound_terrain'

## if pink_player_movement_sound_function is set to 'pink_movement_sound_static', this sound will play with every
## movement
define pink_player_default_movement_sound = None
define pink_follower_default_movement_sound = None

## The sound effect to play if the player character can't carry out a movement.
define pink_player_default_movement_sound_blocked = None

## The movement sound multiplier for NPCs and followers
define pink_otm_default_npc_movement_sound_multiplier = 0.5
define pink_otm_default_no_movement_volume_distance = 10
define pink_otm_default_follower_movement_sound_multiplier = 0.3

## Whether to pause the timer during certain types of events
define pink_otm_pause_timer_on_static_event = True
define pink_otm_pause_timer_on_dynamic_event = False
define pink_otm_pause_timer_on_continuing_event = False

## Mouse movement settings
define pink_otm_mouse_click_move = True
define pink_otm_mouse_held_move = True
define pink_otm_hold_delay = 0.3

## ================================================= DEFAULT SETTINGS =================================================
## Enables the model-based renderer. This helps offload more of the rendering calculations to the GPU, so should improve
## performance.
define config.gl2 = True
