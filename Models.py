import torch.nn as nn

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