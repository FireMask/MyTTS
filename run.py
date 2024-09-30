from audio_gen import MyTTS

texto = ''
with open('text.txt', 'r') as file:
    texto = file.read()

tts = MyTTS(
    model="multi_advanced",
    use_audio_sample=True,
    language="es",
    audio_sample="tavo_garay.wav",
    speed=1,
    delete_files=False,
    file_prefix="tavo"
)

tts.generate_tts(texto)

# [SEPARATOR]