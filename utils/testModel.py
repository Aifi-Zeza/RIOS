import numpy as np
import torch
import torch.nn as nn
import librosa
import sounddevice as sd
import threading


class WakeWordProgramm:
    # Параметры
    SAMPLE_RATE = 22050
    N_MFCC = 10  # Количество MFCC
    MODEL_PATH = 'audio/wake_model/wake_word_classifier.pth'  # Путь к сохраненной модели
    RECORD_DURATION = 2  # Длительность записи в секундах

    def __init__(self,function):
        self.function = function
# Извлечение MFCC из аудио
    def extract_mfcc(self,audio):
        mfccs = librosa.feature.mfcc(y=audio, sr=self.SAMPLE_RATE, n_mfcc=self.N_MFCC)
        return np.mean(mfccs.T, axis=0).reshape(1, -1)  # Вернем в форме [1, N_MFCC]

# Функция для загрузки модели
    def load_model(self,model_path):
        model = LSTMModel(input_size=self.N_MFCC, hidden_size=128, output_size=2)  # 2 класса
        model.load_state_dict(torch.load(model_path))
        model.eval()
        return model
    def record_audio(self,duration):
        audio = sd.rec(int(duration * self.SAMPLE_RATE), samplerate=self.SAMPLE_RATE, channels=1, dtype='float32')
        sd.wait()  # Ждем завершения записи
        return audio.flatten()  # Превращаем в одномерный массив
    

    def predict(self,model, audio):
        mfccs = self.extract_mfcc(audio)  # Извлеките MFCC
        input_tensor = torch.tensor(mfccs, dtype=torch.float32)  # Преобразуйте в тензор
        with torch.no_grad():
            output = model(input_tensor)
            _, predicted = torch.max(output.data, 1)
        return predicted.numpy()[0]  # Вернуть предсказанный клас
    def start(self):
        self.recording_thread = threading.Thread(target=self.startlisten)
        self.recording_thread.start()
    def startlisten(self):
        model = self.load_model(self.MODEL_PATH)
        self.listenning = True
        
        while self.listenning:
            # Запись звука с микрофона
            audio_data = self.record_audio(self.RECORD_DURATION)

            # Предсказание
            result = self.predict(model, audio_data)
            if result == 1:
                self.function()

            #time.sleep(0.5)  # Небольшая пауза перед следующей записью
    
    def stop(self):
        self.listenning = False
# Загрузка модели
class LSTMModel(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(LSTMModel, self).__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = x.unsqueeze(1)  # Добавление размерности для последовательности
        out, _ = self.lstm(x)
        out = out[:, -1, :]  # Используем выход последнего временного шага
        out = self.fc(out)
        return out






    