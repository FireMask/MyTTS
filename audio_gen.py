import torch
import uuid
import os
from TTS.api import TTS
from audio_join import AudioUtil

class MyTTS:
    save_path = "audio_outputs"
    models={
        "spanish_default":"tts_models/es/css10/vits",
        "spanish_trained":"tts_models/es/mai/tacotron2-DDC",
        "multi_advanced":"tts_models/multilingual/multi-dataset/xtts_v2"
    }

    def __init__(self, model, use_audio_sample, language, audio_sample, file_prefix, speed=1, delete_files = True):
        self.use_audio_sample = use_audio_sample
        self.language = language
        self.audio_sample = "audio_samples/" + audio_sample
        self.model_selected = model
        self.speed=speed
        self.delete_audio_files = delete_files
        self.file_prefix = file_prefix

    def init_tts(self):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tts = TTS(self.models[self.model_selected]).to(device)
        print("Running on " + device)

    def available_models(self):
        return self.models
    
    def generate_tts(self, text):
        if not text:
            print("There is no text")
            return "There is no text"
 
        self.init_tts()

        audios = []

        cleaned_text = text.replace("\n", "")
        paragraphs = cleaned_text.split("[SEPARATOR]")
        folder = self.create_folder()
        for index, parag in enumerate(paragraphs):
            if not parag: 
                continue

            file_path = self.get_file_name(index+1, folder)
            self.generate_audio_file(parag, file_path)
            audios.append(file_path)
        
        result_file = self.get_file_name("final", folder, ext="mp3")
        if self.join_audios(audios, result_file):
            if self.delete_audio_files:
                self.delete_audios(audios)

        print("\033[31m" + result_file + "\033[0m")   
    
    def join_audios(self, audios, result_file):
        return AudioUtil.wav_join(audios, result_file)

    def delete_audios(self, audios):
        for audio in audios:
            try:
                os.remove(audio)
                # print(f"File '{audio}' has been deleted.")
            except FileNotFoundError:
                print(f"File '{audio}' does not exist.")
            except PermissionError:
                print(f"Permission denied: '{audio}' could not be deleted.")
            except Exception as e:
                print(f"Error: {e}")

    def create_folder(self):
        folder_name = str(uuid.uuid4().hex)
        os.makedirs(self.save_path+"/"+folder_name, exist_ok=True)
        return folder_name
    
    def get_file_name(self, prefix, save_path, ext="wav"):
        file_name = f"{str(uuid.uuid4().hex)}.{ext}"
        file_path = f"{self.save_path}/{save_path}/{prefix:02}_{self.file_prefix}_{file_name}"
        return file_path

    def generate_audio_file(self, text, file_path):
        if self.use_audio_sample:
            self.tts.tts_to_file(text = text,
                            language = self.language,
                            speaker_wav = self.audio_sample,
                            file_path = file_path,
                            speed=self.speed,
                            split_sentences=False)
        else:
            self.tts.tts_to_file(text = text, file_path = file_path)