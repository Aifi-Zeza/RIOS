import numpy as np
import torch
import librosa
import sounddevice as sd
import threading
import sys
import os
import time

from Models import LSTMModelV2

from transformers import DistilBertTokenizer, DistilBertModel

from vosk import Model,KaldiRecognizer,SetLogLevel
import queue



class WakeWordProgramm:
    # Параметры
    SAMPLE_RATE = 22050
    N_MFCC = 13  # Изменено с 10 на 13, как указано в оригинальной модели
    MODEL_PATH = './files/audio/wake_model/lstm_model.pth'  # Путь к сохраненной модели
    RECORD_DURATION = 2  # Длительность записи в секундах
    fixed_mfcc_length = 50

    def __init__(self,function):
        self.listenning = False
        self.function = function
        self.model = self.load_model(self.MODEL_PATH)
    # Извлечение MFCC из аудио
    def extract_mfcc(self, audio):
        mfccs = librosa.feature.mfcc(y=audio, sr=self.SAMPLE_RATE, n_mfcc=self.N_MFCC)
        return np.mean(mfccs.T, axis=0).reshape(1, -1)  # Вернем в форме [1, N_MFCC]

    # Функция для загрузки модели
    def load_model(self, model_path):
        model = LSTMModelV2(num_classes=2, 
                            mfcc_size=self.N_MFCC, 
                            hidden_size=64,  # Изменено с 32 на 64
                            num_layers=2, 
                            dropout=0.5, 
                            bidirectional=True)  # Используем двунаправленный LSTM
        model.load_state_dict(torch.load(model_path))
        model.eval()
        return model

    def record_audio(self, duration):
        audio = sd.rec(int(duration * self.SAMPLE_RATE), samplerate=self.SAMPLE_RATE, channels=1, dtype='float32')
        sd.wait()  # Ждем завершения записи
        return audio.flatten()  # Превращаем в одномерный массив

    def predict(self, model, audio,):
        n_fft = min(2048, len(audio))  # Устанавливаем n_fft в зависимости от длины сигнала
        mfcc = librosa.feature.mfcc(y=audio, sr=self.SAMPLE_RATE, n_fft=n_fft,n_mfcc=13)
        mfcc = mfcc.T
        if mfcc.shape[0] > self.fixed_mfcc_length:
            mfcc = mfcc[:self.fixed_mfcc_length, :]  # Обрезаем
        elif mfcc.shape[0] < self.fixed_mfcc_length:
            padding = np.zeros((self.fixed_mfcc_length - mfcc.shape[0], self.num_mfcc))
            mfcc = np.vstack((mfcc, padding))
        input_tensor = torch.tensor(mfcc, dtype=torch.float32).unsqueeze(0)  # Преобразуйте в тензор и добавьте размерность для батча
        input_tensor = input_tensor.to(model.device)  # Перемещаем тензор на нужное устройство
        with torch.no_grad():
            output = model(input_tensor)
            probabilities = torch.sigmoid(output)
        return probabilities.numpy()[0][1]  # Вернуть предсказанный класс

    def load_audio_from_file(self, file_path):
        audio, sr = librosa.load(file_path, sr=self.SAMPLE_RATE)  # Загружаем аудио с заданной частотой
        return audio, sr

    def start(self):
        self.listenning = True
        self.recording_thread = threading.Thread(target=self.startlisten)
        self.recording_thread.start()

    def startlisten(self):
        try:
            threshhold = 0.81
        
            while self.listenning:
                # Запись звука с микрофона
                audio_data = self.record_audio(self.RECORD_DURATION)
                #audio_data = self.load_audio_from_file('dataset/wake/0e41dc6d-cd08-4571-91b6-fb78cb4e6468 — копия.mp3')
                # Предсказание
                result = self.predict(self.model, audio_data)
                #print(f'trying:{result}')
                if result > threshhold:
                    self.stop()
                    self.function()
                else:
                    print('rythm')
                


                #time.sleep(0.5)  # Небольшая пауза перед следующей записью
        except KeyboardInterrupt:
            print('exiting')

    def stop(self):
        self.listenning = False

class BERTPrediction:
    def __init__(self):
        # Проверка наличия доступного устройства
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Используемое устройство BERT: {self.device}")
        # Загрузка токенизатора и модели DistilRuBERT для разговорного языка
        self.tokenizer = DistilBertTokenizer.from_pretrained('DeepPavlov/distilrubert-base-cased-conversational')
        self.model = DistilBertModel.from_pretrained('DeepPavlov/distilrubert-base-cased-conversational').to(self.device)
        self.vectorBase = None

    def basesentece(self,baseSentece):
        self.vectorBase = self.get_sentence_vector(baseSentece)

    # Функция для получения векторного представления предложения
    def get_sentence_vector(self,sentence):
        inputs = self.tokenizer(sentence, return_tensors='pt', padding=True, truncation=True).to(self.device)
        outputs = self.model(**inputs)
        return outputs.last_hidden_state[0][0].detach().cpu().numpy()  # Возврат на CPU

   


    # Функция для вычисления косинусного сходства
    def get_cosine_similarity(self, GettedSentence):
        GettedVector = self.get_sentence_vector(GettedSentence) 
        predictedData = np.dot(self.vectorBase, GettedVector) / (np.linalg.norm(self.vectorBase) * np.linalg.norm(GettedVector))
        if predictedData >= 92:
            return True
        else:
            return False

class voskRecognition:
    def __init__(self,runmethod):
        
        self.method = runmethod
        self.unresult = None
        SetLogLevel(0)
        if not os.path.exists("./files/audio/model"):
            print("Голосовая модель не найдена")
            exit(1)


        _deviceInf = sd.query_devices(sd.default.device[0],'input')
        self._samlprate = int(_deviceInf['default_samplerate'])
        print(sd.default.device[0],_deviceInf)
        self._queue = queue.Queue()

        self._model = Model('./files/audio/model')
        self._recognizer = KaldiRecognizer(self._model,self._samlprate)
        self._recognizer.SetWords(False)


    def _recCallbk(self,indata,frames,time,status):
        if status:
            print(status,file=sys.stderr)
        self._queue.put(bytes(indata))

    def record(self):
        self.recording_thread = threading.Thread(target=self.thRecord)
        self.recording_thread.start()

    def thRecord(self):
        try: 
            record = True
            with sd.RawInputStream(dtype='int16',channels=1,callback=self._recCallbk):
                while record:
                    _data = self._queue.get()
                    if self._recognizer.AcceptWaveform(_data):
                        _recognizerRes = self._recognizer.Result()
                        result = _recognizerRes.split('"')
                        if len(result[3]) >= 4:
                            self.method(result[3])
                            record = False
                        else:
                            self.unresult()
                            print('промах')
                            record = False
                        
                
                
        except Exception as e:
            print(str(e))






