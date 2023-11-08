class AudioEditorObserver:
    def __init__(self):
        self.subscribers = []

    def subscribe(self, subscriber):
        self.subscribers.append(subscriber)

    def unsubscribe(self, subscriber):
        self.subscribers.remove(subscriber)

    def notify(self, event, *args):
        for subscriber in self.subscribers:
            self.update(event, subscriber, *args)

    def update(self, event, subscriber, *args):
        if event == "AudioOpened": message = "Audio data successfully loaded"
        elif event == "AudioPasted": message = "Audio pasted from clipboard"
        elif event == "TracksMixed":
            if args: message = f"Tracks successfully mixed and added as a new track: {args[0]}"
            else: message = "Tracks not mixed"
        elif event == "split_audio_track": message = "Track successfully split into two"
        elif event == "move_audio_track": message = "Track successfully moved"
        elif event == "SegmentCopied": message = "Audio segment copied to clipboard"
        elif event == "SegmentPasted": message = "Audio segment successfully pasted"
        elif event == "SegmentCut": message = "Audio segment successfully cut"
        elif event == "SegmentSelected": message = "Audio segment successfully selected"
        elif event == "AudioTrackAdded": message = "Audio track successfully added"
        elif event == "AudioDeformed": message = "Audio successfully deformed"
        elif event == "PitchShifted": message = "Pitch shift effect applied successfully"
        elif event == "AudioEncoded": message = "Audio successfully encoded"
        elif event == "AudioTrackSelected": message = "Audio track selected"
        elif event == "AudioTrackRemoved": message = "Audio track removed"
        elif event == "AudioCopied": message = "Audio copied to clipboard"
        elif event == "AudioCut": message = "Audio cut successfully"
        elif event == "list_audio_tracks":
            if args: message = f"List of audio tracks: {args[0]}"
            else: message = "List of audio tracks"
        elif event == "AudioSaved": message = 'Audio track saved'
        elif event == "DurationObtained":
            if args: message = f"Duration of audio track: {args[0]}"
            else: message = "Duration of audio track"
        else: return ''
        try:
            subscriber.sendall(message.encode())
        except Exception as e:
            print(f"Error sending message to client: {str(e)}")