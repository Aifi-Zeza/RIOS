import numpy as np
import torch
import torch.nn as nn
import librosa
import sounddevice as sd

# Параметры
SAMPLE_RATE = 22050
N_MFCC = 13  # Количество MFCC
MODEL_PATH = 'audio/wake_model/wake_word_classifier.pth'  # Путь к сохраненной модели

# Запись звука с микрофона
def record_audio(duration):
    print("Начинаем запись...")
    audio = sd.rec(int(duration * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype='float32')
    sd.wait()  # Ждущй завершения записи
    print("Запись завершена.")
    return audio.flatten()  # Превращаем в одномерный массив

# Извлечение MFCC из записанного аудио
def extract_mfcc(audio):
    mfccs = librosa.feature.mfcc(y=audio, sr=SAMPLE_RATE, n_mfcc=N_MFCC)
    return np.mean(mfccs.T, axis=0).reshape(1, -1)  # Вернем в форме [1, N_MFCC]

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

# Функция для загрузки модели
def load_model(model_path):
    model = LSTMModel(input_size=N_MFCC, hidden_size=128, output_size=2)  # 2 класса
    model.load_state_dict(torch.load(model_path))
    model.eval()
    return model

# Функция для предсказания
def predict(model, audio):
    mfccs = extract_mfcc(audio)  # Извлеките MFCC
    input_tensor = torch.tensor(mfccs, dtype=torch.float32)  # Преобразуйте в тензор
    with torch.no_grad():
        output = model(input_tensor)
        _, predicted = torch.max(output.data, 1)
    return predicted.numpy()[0]  # Вернуть предсказанный класс

# Основная функция
if __name__ == '__main__':
    model = load_model(MODEL_PATH)

    # Запись звука с микрофона
    duration = 2  # Длительность записи в секундах
    audio_data = record_audio(duration)

    # Предсказание
    result = predict(model, audio_data)
    if result == 1:
        print("Предсказано: Wake")
    else:
        print("Предсказано: Not Wake")