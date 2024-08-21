import os
import numpy as np
import librosa
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader


# Параметры
SAMPLE_RATE = 22050
SEGMENT_DURATION = 1.25  # Длительность сегмента звука для анализа (в секундах)
SEGMENT_SAMPLES = SAMPLE_RATE * SEGMENT_DURATION
SEGMENT_SAMPLES = int(SEGMENT_SAMPLES)
N_MFCC = 10  # Количество MFCC
BATCH_SIZE = 32
EPOCHS = 30
LEARNING_RATE = 0.001

# Функция для деления аудио на сегменты и извлечения MFCC
def extract_mfcc_from_segments(file_path):
    audio, _ = librosa.load(file_path, sr=SAMPLE_RATE)
    num_samples = len(audio)

    segments = []
    for start in range(0, num_samples, SEGMENT_SAMPLES):
        end = min(start + SEGMENT_SAMPLES, num_samples)
        segment = audio[start:end]

        if len(segment) < SEGMENT_SAMPLES:
            silence = np.zeros(SEGMENT_SAMPLES - len(segment))
            segment = np.concatenate((segment, silence))

        mfccs = librosa.feature.mfcc(y=segment, sr=SAMPLE_RATE, n_mfcc=N_MFCC)
        segments.append(np.mean(mfccs.T, axis=0))

    return segments

# Класс Dataset для PyTorch
class AudioDataset(Dataset):
    def __init__(self, data_dir):
        self.X = []
        self.y = []
        loaded_files = 0
        for label in ["wake", "not_wake"]:
            folder = os.path.join(data_dir, label)
            for filename in os.listdir(folder):
                print('загрузка файла под номером' + " " + str(loaded_files))
                loaded_files += 1
                if filename.endswith('.mp3'):
                    file_path = os.path.join(folder, filename)
                    mfccs_list = extract_mfcc_from_segments(file_path)
                    self.X.extend(mfccs_list)
                    self.y.extend([1 if label == "wake" else 0] * len(mfccs_list))
                    
        self.X = np.array(self.X)
        self.y = np.array(self.y)
    
    def __len__(self):
        return len(self.X)
    
    def __getitem__(self, idx):
        return torch.tensor(self.X[idx], dtype=torch.float32), torch.tensor(self.y[idx], dtype=torch.long)

# Создание модели LSTM
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

# Основная функция для обучения модели
def train_classifier(data_dir):
    print("Загрузка данных...")
    dataset = AudioDataset(data_dir)
    train_size = int(0.8 * len(dataset))
    test_size = len(dataset) - train_size
    train_dataset, test_dataset = torch.utils.data.random_split(dataset, [train_size, test_size])

    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False)

    model = LSTMModel(input_size=N_MFCC, hidden_size=128, output_size=2)  # 2 класса
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)

    print("Обучение модели...")
    for epoch in range(EPOCHS):
        model.train()
        for inputs, labels in train_loader:
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

    # Оценка модели
    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for inputs, labels in test_loader:
            outputs = model(inputs) 
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    accuracy = correct / total
    print(f"\nРезультаты обучения модели:\n{'-'*30}")
    print(f"Точность: {accuracy:.2f}")

    # Сохранение модели
    torch.save(model.state_dict(), classifier_directory+'wake_word_classifier.pth')
    print(f"Модель сохранена в {classifier_directory}\n{'-'*30}")

# Запуск
if __name__ == "__main__":
    data_directory = 'dataset'  # Укажите путь к вашим данным
    classifier_directory = 'audio/wake_model/'
    train_classifier(data_directory)