from pydub import AudioSegment

class AudioUtil:
    def __init__(self):
        print("init")

    def wav_join(audios, file_name):
        if not audios:
            print("Error: no audios provided")
            return False
        
        merged = AudioSegment.from_wav(audios[0])

        # Append the remaining files
        for audio in audios[1:]:
            next_audio = AudioSegment.from_wav(audio)
            merged += next_audio  # Concatenate the audio segments

        # Export the merged audio to a new file
        merged.export(file_name, format="mp3")

        return True