from pydub import AudioSegment

class AudioAdapter:
    def load_audio(self, file_path, format):
        audio = AudioSegment.from_file(file_path, format)
        return audio

    def save_audio(self, audio, output_path, format):
        audio.export(output_path, format)
