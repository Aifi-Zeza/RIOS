import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import time
import random
import os

# Параметры записи
sample_rate = 44100  # Частота дискретизации
max_duration = 480  # Максимальная длина записи в секундах
min_duration = 120   # Минимальная длина записи в секундах
output_dir = 'audio_records'  # Директория для сохранения файлов

# Создание директории для аудиозаписей, если её нет
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def record_audio(duration):
    print(f"Запись аудио в течение {duration} секунд...")
    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float64')
    sd.wait()  # ожидание завершения записи
    return audio

def save_audio(audio, filename):
    wav.write(filename, sample_rate, audio)
    print(f"Сохранено {filename}")

if __name__ == "__main__":
    try:
        while True:
            duration = random.uniform(min_duration, max_duration)  # случайная длина записи
            audio_data = record_audio(duration)  # запись аудио
            filename = os.path.join(output_dir, f"recording_{time.time()}.wav")  # имя файла
            save_audio(audio_data, filename)  # сохранение файла
            time.sleep(1)  # небольшая пауза перед следующей записью
    except KeyboardInterrupt:
        print("Запись остановлена.")