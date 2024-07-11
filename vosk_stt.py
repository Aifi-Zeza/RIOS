from vosk import Model,KaldiRecognizer,SetLogLevel
from pydub import AudioSegment
import json
import os

SetLogLevel(0)
if not os.path.exists("sdata/model"):
    print("Голосовая модель не найдена")
    exit(1)

_framerate = 1600
_chanels = 1

_model = Model("sdata/model")
_rec = KaldiRecognizer(_model,_framerate)
_rec.SetWords(True)

_mp3 = AudioSegment.from_mp3('Song.mp3')
_mp3 = _mp3.set_chanels(_chanels)
_mp3 = _mp3.set_frame_rate(_framerate)

_rec.AcceptWaveform(_mp3.raw_data)
_result = _rec.Result()
_text = json.loads(_result)["text"]
with open('data.txt','w') as f:
    json.dump(_text,f,ensure_ascii=False,indent=4)