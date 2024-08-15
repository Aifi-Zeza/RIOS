import os
import numpy as np
import librosa
from tensorflow.python.keras import layers, models

# Параметры
SAMPLE_RATE = 22050
DURATION = 1  # Длительность аудиофайла в секундах
NUM_SAMPLES = SAMPLE_RATE * DURATION

def load_data(data_dir):
    labels = []
    features = []

    # Загрузка файлов для "wake" слова
    for filename in os.listdir(os.path.join(data_dir, 'wake')):
        file_path = os.path.join(data_dir, 'wake', filename)
        try:
            signal, sr = librosa.load(file_path, sr=SAMPLE_RATE)
            # Делим сигнал на фрагменты
            for start in range(0, len(signal), NUM_SAMPLES):
                end = start + NUM_SAMPLES
                if end <= len(signal):
                    features.append(signal[start:end])
                    labels.append(1)  # "wake" соответствует 1
        except Exception as e:
            print(f"Ошибка загрузки {file_path}: {e}")

    # Загрузка файлов для "not wake"
    for filename in os.listdir(os.path.join(data_dir, 'not_wake')):
        file_path = os.path.join(data_dir, 'not_wake', filename)
        try:
            signal, sr = librosa.load(file_path, sr=SAMPLE_RATE)
            # Делим сигнал на фрагменты
            for start in range(0, len(signal), NUM_SAMPLES):
                end = start + NUM_SAMPLES
                if end <= len(signal):
                    features.append(signal[start:end])
                    labels.append(0)  # "not wake" соответствует 0
        except Exception as e:
            print(f"Ошибка загрузки {file_path}: {e}")

    return np.array(features), np.array(labels)

# Подготовка данных
data_dir = 'dataset'
X, y = load_data(data_dir)
X = X.reshape((-1, NUM_SAMPLES, 1))  # Формат для CNN

# Создание модели
model = models.Sequential([
    layers.Conv1D(16, 5, activation='relu', input_shape=(NUM_SAMPLES, 1)),
    layers.MaxPooling1D(pool_size=2),
    layers.Conv1D(32, 5, activation='relu'),
    layers.MaxPooling1D(pool_size=2),
    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dense(1, activation='sigmoid')  # Бинарная классификация
])

# Компиляция модели
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Обучение модели
model.fit(X, y, epochs=10, batch_size=32, validation_split=0.2)

# Сохранение модели
model.save('wake_word_model.h5')

print("Модель обучена и сохранена.")