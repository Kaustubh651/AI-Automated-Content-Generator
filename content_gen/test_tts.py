from TTS.api import TTS

tts = TTS(model_name="tts_models/en/ljspeech/vits", progress_bar=True, gpu=True)
tts.tts_to_file(text="Hello world, this is Sprint 0 TTS test.", file_path="audio/test.wav")
print("TTS audio saved at audio/test.wav")
