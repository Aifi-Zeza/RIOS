from vosk import Model,KaldiRecognizer,SetLogLevel
import queue
import json
import sounddevice as sd
import sys
import os

SetLogLevel(0)
if not os.path.exists("audio/model"):
    print("Голосовая модель не найдена")
    exit(1)


_deviceInf = sd.query_devices(sd.default.device[0],'input')
_samlprate = int(_deviceInf['default_samplerate'])
print(sd.default.device[0],_deviceInf)
_queue = queue.Queue()


def _recCallbk(indata,frames,time,status):
    if status:
        print(status,file=sys.stderr)
    _queue.put(bytes(indata))

_model = Model('audio/model')
_recognizer = KaldiRecognizer(_model,_samlprate)
_recognizer.SetWords(False)

try: 
    with sd.RawInputStream(dtype='int16',channels=1,callback=_recCallbk):
        while True:
            _data = _queue.get()
            if _recognizer.AcceptWaveform(_data):
                _recognizerRes = _recognizer.Result()

                _resultDict = json.loads(_recognizerRes)
                if not _resultDict.get('text','') == "":
                    print(_recognizerRes)
                else:
                    print('no input snd') 
except KeyboardInterrupt:
    print('====> Record Finish') 
except Exception as e:
    print(str(e))
                           
                           
                           
                           