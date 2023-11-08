from cur.adapter.audio_adapter import AudioAdapter


class AudioEditorServer:
    def __init__(self, observer):
        self.audio_data = None
        self.audio_tracks = []
        self.adapter = AudioAdapter()
        self.clipboard = None
        self.current_track = None
        self.observer = observer
        self.track_names = {}
        self.commands = {
            "open": self.open_audio,
            "copy": self.copy_audio,
            "paste": self.paste_audio,
            "cut": self.cut_audio,
            "encode": self.encode_audio,
            "add_track": self.add_audio_track,
            "deform": self.deform_audio,
            "mix": self.mix_audio_tracks,
            "split": self.split_audio_track,
            "move": self.move_audio_track,
            "copy-segment": self.copy_segment,
            "paste-segment": self.copy_segment,
            "cut-segment": self.cut_segment,
            "select_segment": self.select_segment,
            "pitch_shift": self.pitch_shift,
            "sat": self.select_audio_track,
            "rat": self.remove_audio_track_by_name,
            "lat": self.list_audio_tracks,
            "sct": self.save_current_track,
            "duration": self.get_audio_track_duration,
        }

    def list_audio_tracks(self):
        try:
            track_list = list(self.track_names.keys())
            track_list_message = "\n".join(track_list)
            self.observer.notify("list_audio_tracks", track_list_message)
            if track_list:
                return track_list_message
            else:
                return "No active audio tracks"
        except Exception as e:
            return f"Error getting list of audio tracks: {str(e)}"

    def mix_audio_tracks(self, new_track_name, *track_names_or_indices):
        try:
            tracks_to_mix = []
            for name_or_index in track_names_or_indices:
                if name_or_index.isdigit():
                    index = int(name_or_index)
                    if 0 <= index < len(self.audio_tracks):
                        tracks_to_mix.append(self.audio_tracks[index])
                elif name_or_index in self.track_names:
                    index = self.track_names[name_or_index]
                    if 0 <= index < len(self.audio_tracks):
                        tracks_to_mix.append(self.audio_tracks[index])
            if len(tracks_to_mix) >= 2:
                mixed_track = sum(tracks_to_mix)
                self.audio_tracks.append(mixed_track)
                self.track_names[new_track_name] = len(self.audio_tracks) - 1
                self.observer.notify("TracksMixed", new_track_name)
                return ''
            else:
                return "At least two tracks (by name or index) are required for mixing."
        except Exception as e:
            return f"Error mixing tracks: {str(e)}"

    def split_audio_track(self, track_name_or_index, start_time, end_time):
        try:
            if track_name_or_index.isdigit():
                index = int(track_name_or_index)
                if 0 <= index < len(self.audio_tracks):
                    track = self.audio_tracks[index]
                else:
                    return "Invalid audio track index"
            elif track_name_or_index in self.track_names:
                index = self.track_names[track_name_or_index]
                if 0 <= index < len(self.audio_tracks):
                    track = self.audio_tracks[index]
                else:
                    return "Invalid audio track index"
            else:
                return "Track with the specified name or index not found"
            start_time = int(start_time)
            end_time = int(end_time)
            split_tracks = [track[start_time:end_time], track[:start_time] + track[end_time:]]
            del self.audio_tracks[index]
            self.audio_tracks.extend(split_tracks)
            self.observer.notify("split_audio_track")
            return ''
        except Exception as e:
            return f"Error splitting track: {str(e)}"

    def get_audio_track_duration(self, track_name_or_index):
        try:
            if track_name_or_index.isdigit():
                index = int(track_name_or_index)
                if 0 <= index < len(self.audio_tracks):
                    duration = len(self.audio_tracks[index])
                    self.observer.notify("DurationObtained",duration)
                    return ''
                else:
                    return "Invalid audio track index"
            elif track_name_or_index in self.track_names:
                index = self.track_names[track_name_or_index]
                if 0 <= index < len(self.audio_tracks):
                    duration = len(self.audio_tracks[index])
                    self.observer.notify("DurationObtained", duration)
                    return ''
                else:
                    return "Track with the specified name not found"
            else:
                return "Track with the specified name or index not found"
        except Exception as e:
            return f"Error getting audio track duration: {str(e)}"

    def move_audio_track(self, track_name_or_index, time_shift):
        try:
            if track_name_or_index.isdigit():
                index = int(track_name_or_index)
                if 0 <= index < len(self.audio_tracks):
                    track = self.audio_tracks[index]
                else:
                    return "Invalid audio track index"
            elif track_name_or_index in self.track_names:
                index = self.track_names[track_name_or_index]
                if 0 <= index < len(self.audio_tracks):
                    track = self.audio_tracks[index]
                else:
                    return "Invalid audio track index"
            else:
                return "Track with the specified name or index not found"

            time_shift = int(time_shift)
            self.audio_tracks[index] = track.fade_in(time_shift)
            self.observer.notify("move_audio_track")
            return ''
        except Exception as e:
            return f"Error moving track: {str(e)}"

    def copy_segment(self):
        if self.audio_data:
            self.clipboard = self.audio_data
            self.observer.notify("SegmentCopied")
            return ''
        else:
            return "No audio selected for copying"

    def paste_segment(self):
        if self.clipboard:
            self.audio_data += self.clipboard
            self.observer.notify("SegmentPasted")
            return ''
        else:
            return "No data in clipboard to paste"

    def cut_segment(self):
        if self.audio_data:
            self.clipboard = self.audio_data
            self.audio_data = None
            self.observer.notify("SegmentCut")
            return ''
        else:
            return "No audio selected for cutting"

    def select_segment(self, start_time, end_time):
        if self.audio_data:
            try:
                start_time = int(start_time)
                end_time = int(end_time)
                self.audio_data = self.audio_data[start_time:end_time]
                self.observer.notify("SegmentSelected")
                return ''
            except Exception as e:
                return f"Error selecting audio segment: {str(e)}"
        else:
            return "No audio selected for segment selection"

    def add_audio_track(self, file_path, format, track_name):
        try:
            audio_track = self.adapter.load_audio(file_path, format)
            self.audio_tracks.append(audio_track)
            self.track_names[track_name] = len(self.audio_tracks) - 1
            self.observer.notify("AudioTrackAdded")
            return ''
        except Exception as e:
            return f"Error adding audio track: {str(e)}"

    def deform_audio(self, start_time, end_time, effect_type):
        if self.audio_data:
            try:
                start_time = int(start_time)
                end_time = int(end_time)
                if effect_type == "reverse":
                    self.audio_data = self.audio_data[start_time:end_time].reverse()
                elif effect_type == "speedup":
                    self.audio_data = self.audio_data[start_time:end_time].speedup(playback_speed=1.5)
                self.observer.notify("AudioDeformed")
                return ''
            except Exception as e:
                return f"Error deforming audio: {str(e)}"
        else:
            return "No audio selected for deformation"

    def pitch_shift(self, amount):
        if self.current_track:
            try:
                amount = float(amount)
                self.current_track = self.current_track.speedup(playback_speed=amount)
                self.observer.notify("PitchShifted")
                return ''
            except Exception as e:
                return f"Error applying pitch shift effect: {str(e)}"
        else:
            return "No selected audio track to apply the effect"

    def encode_audio(self, output_format):
        if self.audio_data:
            try:
                if output_format in ["ogg", "flac", "mp3"]:
                    output_path = "output." + output_format
                    self.adapter.save_audio(self.audio_data, output_path, output_format)
                    self.observer.notify("AudioEncoded")
                    return ''
                else:
                    return "Invalid format for encoding"
            except Exception as e:
                return f"Error encoding audio: {str(e)}"
        else:
            return "No data to encode"

    def save_current_track(self, output_path, output_format):
        try:
            if self.current_track:
                self.adapter.save_audio(self.current_track, output_path, output_format)
                self.observer.notify("AudioSaved")
                return ''
            else:
                return "No data to save. Select an audio track and apply pitch_shift effect first."
        except Exception as e:
            return f"Error saving audio: {str(e)}"

    def select_audio_track(self, track_name_or_index):
        try:
            if track_name_or_index.isdigit():
                index = int(track_name_or_index)
                if 0 <= index < len(self.audio_tracks):
                    self.current_track = self.audio_tracks[index]
                    self.observer.notify("AudioTrackSelected")
                    return ''
                else:
                    return "Invalid audio track index"
            elif track_name_or_index in self.track_names:
                index = self.track_names[track_name_or_index]
                if 0 <= index < len(self.audio_tracks):
                    self.current_track = self.audio_tracks[index]
                    self.observer.notify("AudioTrackSelected")
                    return ''
                else:
                    return "Track with the specified name not found"
            else:
                return "Track with the specified name or index not found"
        except Exception as e:
            return f"Error selecting audio track: {str(e)}"

    def remove_audio_track_by_name(self, track_name):
        try:
            if track_name in self.track_names:
                track_index = self.track_names[track_name]
                del self.track_names[track_name]
                if 0 <= track_index < len(self.audio_tracks):
                    del self.audio_tracks[track_index]
                    self.observer.notify("AudioTrackRemoved")
                    return ''
                else:
                    return "Invalid audio track index"
            else:
                return "Audio track with the specified name not found"
        except Exception as e:
            return f"Error removing audio track: {str(e)}"

    def open_audio(self, file_path, format):
        try:
            self.audio_data = self.adapter.load_audio(file_path, format)
            self.observer.notify("AudioOpened")
            return ''
        except Exception as e:
            return f"Error loading audio: {str(e)}"
    def copy_audio(self):
        if self.audio_data:
            self.clipboard = self.audio_data
            self.observer.notify("AudioCopied")
            return ''
        else:
            return "No audio selected for copying"
    def paste_audio(self):
        if self.clipboard:
            self.audio_data = self.clipboard
            self.observer.notify("AudioPasted")
            return ''
        else:
            return "No data in clipboard to paste"

    def cut_audio(self):
        if self.audio_data:
            self.audio_data = None
            self.observer.notify("AudioCut")
            return ''
        else:
            return "No audio selected for cutting"

    def handle_command(self, command):
        parts = command.split(" ")
        if parts[0] in self.commands:
            if len(parts) > 1:
                return self.commands[parts[0]](*parts[1:])
            else:
                return self.commands[parts[0]]()
        else:
            return "Invalid command"