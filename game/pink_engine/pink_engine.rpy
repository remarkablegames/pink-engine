default pink_render_enabled = True

init python:
    import pink_engine.exports as pink
    import pygame

    # Creates the channels for locational sound effects that use the sound slider.
    pink_channels_spawned = 100
    pink_channel_ids = set()
    for x in range(pink_channels_spawned):
        new_channel_id = f"pink_sound_{x}"
        renpy.exports.music.register_channel(new_channel_id, "sfx")
        pink_channel_ids.add(new_channel_id)

    # Creates the channels for locational sound effects that use the music slider.
    pink_music_channels_spawned = 100
    pink_music_channel_ids = set()
    for x in range(pink_music_channels_spawned):
        new_channel_id = f"pink_music_{x}"
        renpy.exports.music.register_channel(new_channel_id, "music")
        pink_music_channel_ids.add(new_channel_id)

    # Creates the channels for locational sound effects that use the voice slider.
    pink_voice_channels_spawned = 100
    pink_voice_channel_ids = set()
    for x in range(pink_voice_channels_spawned):
        new_channel_id = f"pink_voice_{x}"
        renpy.exports.music.register_channel(new_channel_id, "voice")
        pink_voice_channel_ids.add(new_channel_id)
