from vosk import Model,KaldiRecognizer,SetLogLevel
import json
import wave
import sys
import os

SetLogLevel(0)
if not os.path.exists("sdata/model"):
    print("Голосовая модель не найдена")
    exit(1)


wf = wave.open("Song.wav", "rb")
if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
    print("Audio file must be WAV format mono PCM.")
    sys.exit(1)

_model = Model("sdata/model")
_rec = KaldiRecognizer(_model,wf.getframerate())
_rec.SetWords(True)
_rec.SetPartialWords(True)

while True:
    data = wf.readframes(4000)
    if len(data) == 0:
        break
    if _rec.AcceptWaveform(data):
        print(_rec.Result())

print(_rec.FinalResult())