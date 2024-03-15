# """C:\Users\sxb23\.cache\whisper"""

import whisper_timestamped as whisper

audio = whisper.load_audio("AUDIO.wav")

model = whisper.load_model("C:/Users/sxb23/.cache/whisper/small.pt", device="gpu")

result = whisper.transcribe(model, audio, language="fr")

import json

print(json.dumps(result, indent=2, ensure_ascii=False))
