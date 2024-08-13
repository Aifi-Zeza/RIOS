import numpy as np
import sounddevice as sd
import librosa
import tensorflow as tf

# Параметры
SAMPLE_RATE = 22050
DURATION = 1  # Длительность звука для анализа (в секундах)
NUM_SAMPLES = SAMPLE_RATE * DURATION

# Загрузка модели
model = tf.keras.models.load_model('wake_word_model.h5')

# Функция для предсказания
def predict_wake_word(audio):
    # Обработка аудио
    audio = audio.flatten()  # Убедимся, что это одномерный массив
    if len(audio) < NUM_SAMPLES:
        audio = np.pad(audio, (0, NUM_SAMPLES - len(audio)), 'constant')  # Добавление нулей до 1 секунды
    audio = audio[:NUM_SAMPLES]  # Чтобы гарантировать, что длина 1 секунда
    audio = audio.reshape((1, NUM_SAMPLES, 1))  # Формат для нейросети

    # Предсказание
    prediction = model.predict(audio)
    return prediction[0][0]

# Функция для записи и предсказания
def listen_for_wake_word():
    print("Начинаю прослушивание... (Скажите 'wake' для активации)")
    while True:
        # Запись аудио
        audio = sd.rec(int(NUM_SAMPLES), samplerate=SAMPLE_RATE, channels=1, dtype='float32')
        sd.wait()  # Ждем окончания записи

        # Предсказание
        confidence = predict_wake_word(audio)
        print(f"Предсказание: {confidence:.4f}")

        # Проверка предсказания
        if confidence > 0.5:  # Порог для "wake"
            print("Слово 'wake' распознано!")
            # Здесь вы можете добавить код для активации вашего приложения

# Запуск
listen_for_wake_word()