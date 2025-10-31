from typing import Dict, Set, Union, Optional
from math import floor, pow, sqrt

from pink_engine.commons import Coord
from pink_engine.orthogonal_tiled_map import OrthogonalTiledMapGameObject
import renpy  # noqa
import renpy.store as rs  # noqa


class PinkChannel:
    def __init__(
            self,
            sound_file: str,
            channel_id: str,
            emitter: Union[Coord, str, OrthogonalTiledMapGameObject],
            listen_pixel: Coord,
            pan: bool,
            scale: bool,
            max_volume_distance: float,
            min_volume_distance: Optional[float],
            min_volume: float,
            max_volume: float,
            max_pan_distance: Optional[float],
            no_pan_distance: float,
            max_pan: float,
            loop: bool,
            mixer: str
    ):
        """
        This class represents a single locational sound being played. It will be automatically destroyed when the
        sound effect is done playing.
        """
        if min_volume_distance is None:
            min_volume_distance: int = renpy.store.pink_otm_default_min_volume_distance
        if max_pan_distance is None:
            max_pan_distance: int = renpy.store.pink_otm_default_max_pan_distance
        self.sound_file = sound_file
        self.mixer = mixer
        self.channel_id = channel_id
        self.emitter = emitter

        self.pan = pan
        self.scale = scale

        self.max_volume_distance = max_volume_distance
        self.min_volume_distance = min_volume_distance
        self.min_volume = min_volume
        self.max_volume = max_volume

        self.max_pan_distance = max_pan_distance
        self.no_pan_distance = no_pan_distance
        self.max_pan = max_pan

        self.loop = loop

        # Sets initial values
        self._volume_ratio = None
        self._pan_ratio = None
        emit_pixel = self._get_emit_pixel()
        if self.scale:
            self._set_volume(emit_pixel, listen_pixel)
        if self.pan:
            self._set_pan(emit_pixel, listen_pixel)

        renpy.exports.music.play(self.sound_file, self.channel_id, loop=loop)

        self.last_st = None

    def _get_emit_pixel(self) -> Optional[Coord]:
        """
        Retrieves the pixel that is considered to be emitting this particular sound effects. All distances
        are calculated from this pixel.
        """
        if type(self.emitter) is str:
            emit_object = getattr(rs, self.emitter)
            if issubclass(type(emit_object), OrthogonalTiledMapGameObject):
                if self.emitter.base_id is not None:
                    emit_pixel = Coord(
                        int(floor((self.emitter.base_x_start + self.emitter.base_x_end) / 2)),
                        int(floor((self.emitter.base_y_start + self.emitter.base_y_end) / 2)))
                else:
                    return None 
            else:
                emit_pixel = Coord(
                    emit_object.x + floor(emit_object.width / 2),
                    emit_object.y + emit_object.arc_y_offset + floor(emit_object.height / 2))
        elif issubclass(type(self.emitter), OrthogonalTiledMapGameObject):
            if self.emitter.base_id is not None:
                emit_pixel = Coord(
                    int(floor((self.emitter.base_x_start + self.emitter.base_x_end) / 2)),
                    int(floor((self.emitter.base_y_start + self.emitter.base_y_end) / 2)))
            else:
                return None
        else:
            emit_pixel = Coord(
                floor((self.emitter.x + 0.5) * rs.pink_otm_current_map.tile_size.x),
                floor((self.emitter.y + 0.5) * rs.pink_otm_current_map.tile_size.y))
        return emit_pixel

    def _set_volume(self, emit_pixel: Coord, listen_pixel: Coord) -> None:
        """
        Recalculates the volume on this channel by recalculating the distance between the emit_pixel and the
        listen_pixel.
        """
        if rs.pink_otm_loading_map is not None:
            this_map = rs.pink_otm_loading_map
        else:
            this_map = rs.pink_otm_current_map

        if listen_pixel is None or this_map is None or this_map.tile_size is None:  # Startups & Transition
            return

        # Distance is total distance in tiles
        distance = sqrt(
            pow(abs(emit_pixel.x - listen_pixel.x) / this_map.tile_size.x, 2) +
            pow(abs(emit_pixel.y - listen_pixel.y) / this_map.tile_size.y, 2))
        if distance > self.min_volume_distance:
            volume_ratio = self.min_volume
        elif distance <= self.max_volume_distance:
            volume_ratio = self.max_volume
        else:
            # distance ratio = what ratio of the total distance from max volume to min volume is this distance at.
            distance_ratio = (
                    (distance - self.max_volume_distance) / (self.min_volume_distance - self.max_volume_distance))
            volume_ratio = 0 + self.max_volume - (self.max_volume * distance_ratio) + (self.min_volume * distance_ratio)
            if volume_ratio < self.min_volume:
                volume_ratio = self.min_volume
        if self._volume_ratio is None or self._volume_ratio != volume_ratio:
            renpy.exports.music.set_volume(volume_ratio, delay=0, channel=self.channel_id)
            self._volume_ratio = volume_ratio

    def _set_pan(self, emit_pixel: Coord, listen_pixel: Coord) -> None:
        """
        Recalculates the pan on this channel by recalculating the horizontal distance between the emit_pixel and the
        listen_pixel.
        """
        if rs.pink_otm_loading_map is not None:
            this_map = rs.pink_otm_loading_map
        else:
            this_map = rs.pink_otm_current_map

        if listen_pixel is None or this_map is None or this_map.tile_size is None:  # Startups & Transition
            return

        # Only horizontal distance matters for panning
        distance = (emit_pixel.x - listen_pixel.x) / this_map.tile_size.x
        if distance > self.max_pan_distance:
            pan_ratio = self.max_pan
        elif distance < -self.max_pan_distance:
            pan_ratio = -self.max_pan
        elif abs(distance) <= self.no_pan_distance:
            pan_ratio = 0.0
        else:
            pan_ratio = (distance / self.max_pan_distance) * self.max_pan

        if self._pan_ratio is None or self._pan_ratio != pan_ratio:
            renpy.exports.music.set_pan(pan_ratio, delay=0, channel=self.channel_id)
            self._pan_ratio = pan_ratio

    def per_frame(self, st: float, listen_pixel: Coord):
        """
        This function is called every frame that the sound is active, adjusting volume and panning, and killing
        the channel if necessary.
        """
        self.last_st = st
        if not renpy.exports.music.is_playing(self.channel_id):
            rs.pink_sound_manager.recycle_channel(self.channel_id)

        emit_pixel = self._get_emit_pixel()

        if emit_pixel is None:  # Object's conditional was removed
            return

        if self.scale:
            self._set_volume(emit_pixel, listen_pixel)
        if self.pan:
            self._set_pan(emit_pixel, listen_pixel)


class PinkSoundManager:
    def __init__(self):
        """
        Manages locational sounds (sounds with scaling and panning based on distance)
        """
        self.last_st = 0.0

        self.active_channels: Dict[str, PinkChannel] = {}

        self.available_sound_channels: Set[str] = renpy.store.pink_channel_ids.copy()
        self.available_music_channels: Set[str] = renpy.store.pink_music_channel_ids.copy()
        self.available_voice_channels: Set[str] = renpy.store.pink_voice_channel_ids.copy()

        self._next_channel_id = 0

    def play_sound(
            self,
            sound_file: str,
            emitter: Union[Coord, str, OrthogonalTiledMapGameObject],
            pan: bool = True,
            scale: bool = True,
            max_volume_distance: float = 1,
            min_volume_distance: Optional[float] = None,
            min_volume: float = 0.0,
            max_volume: float = 1.0,
            max_pan_distance: float = None,
            no_pan_distance: Optional[float] = 0,
            max_pan: float = 1.0,
            loop: bool = False,
            mixer: str = "sfx"
    ) -> Optional[str]:
        """
        Plays the given sound effect.
        """
        if mixer == "sfx":
            if len(self.available_sound_channels) == 0:
                return  # can't play more than a 100 scaled/panned sounds at once
            used_channel_id = self.available_sound_channels.pop()
        elif mixer == "music":
            if len(self.available_music_channels) == 0:
                return  # can't play more than a 100 scaled/panned sounds at once
            used_channel_id = self.available_music_channels.pop()
        elif mixer == "voice":
            if len(self.available_voice_channels) == 0:
                return  # can't play more than a 100 scaled/panned sounds at once
            used_channel_id = self.available_voice_channels.pop()
        else:
            return  # Cannot play scaled/panned sounds on custom mixers.

        new_channel = PinkChannel(
            sound_file=sound_file,
            channel_id=used_channel_id,
            listen_pixel=self._get_listen_pixel(),
            emitter=emitter,
            pan=pan,
            scale=scale,
            max_volume_distance=max_volume_distance,
            min_volume_distance=min_volume_distance,
            min_volume=min_volume,
            max_volume=max_volume,
            max_pan_distance=max_pan_distance,
            no_pan_distance=no_pan_distance,
            max_pan=max_pan,
            loop=loop,
            mixer=mixer)
        self.active_channels[used_channel_id] = new_channel

        return used_channel_id

    def recycle_channel(self, channel_id: str) -> None:
        """
        Recycles the given channel id, adding it back into the list of available channels.
        """
        renpy.exports.music.stop(channel_id)
        self.active_channels.pop(channel_id)
        if channel_id.startswith('pink_sound_'):
            self.available_sound_channels.add(channel_id)
        elif channel_id.startswith('pink_music_'):
            self.available_music_channels.add(channel_id)
        elif channel_id.startswith('pink_voice_'):
            self.available_voice_channels.add(channel_id)

    @staticmethod
    def _get_listen_pixel() -> Optional[Coord]:
        """
        Retrieves the pixel that is considered to be the listener for sound effects on this frame. All distances
        are calculated based on this pixel.
        """
        if rs.pink_otm_current_camera is None:  # transitions
            return

        listen_object = rs.pink_otm_current_camera.camera_target
        listen_pixel = Coord(
            listen_object.x + floor(listen_object.width / 2),
            listen_object.y + listen_object.arc_y_offset + floor(listen_object.height / 2))
        return listen_pixel

    def per_frame(self, st: float) -> None:
        """
        Called every frame, calling the per_frame function of all active channels in turn.
        """
        self.last_st = st

        listen_pixel = self._get_listen_pixel()
        if listen_pixel is None:
            return

        for active_channel in self.active_channels.copy().values():
            active_channel.per_frame(st, listen_pixel)

    def stop_sound(self, channel_id: str):
        """
        Stops the sound on the given channel, and recycles the channel.
        """
        if channel_id in self.active_channels:
            renpy.exports.music.stop(channel_id)
        self.active_channels.pop(channel_id)
        if channel_id.startswith('pink_sound_'):
            self.available_sound_channels.add(channel_id)
        elif channel_id.startswith('pink_music_'):
            self.available_music_channels.add(channel_id)
        elif channel_id.startswith('pink_voice_'):
            self.available_voice_channels.add(channel_id)

    def stop_all_sounds(self):
        """
        Stops the sounds on all channels, recycling them.
        """
        for channel_id in self.active_channels.keys():
            renpy.exports.music.stop(channel_id)
        self.active_channels = {}
        self.available_sound_channels = renpy.store.pink_channel_ids.copy()
        self.available_music_channels = renpy.store.pink_music_channel_ids.copy()
        self.available_voice_channels = renpy.store.pink_voice_channel_ids.copy()

    def pause_all_sounds(self):
        """
        Pauses the sounds on all channels.
        """
        for channel_id in self.active_channels.keys():
            renpy.exports.music.set_pause(True, channel_id)

    def unpause_all_sounds(self):
        """
        Unpauses the sounds on all channels.
        """
        for channel_id in self.active_channels.keys():
            renpy.exports.music.set_pause(False, channel_id)
