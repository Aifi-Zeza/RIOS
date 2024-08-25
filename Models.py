import torch.nn as nn
import torch
import sys,os


class LSTMModelV2(nn.Module):
    def __init__(self, num_classes, mfcc_size, hidden_size, num_layers, dropout, bidirectional, device='cpu'):
        super(LSTMModelV2, self).__init__()

        self.num_layers = num_layers
        self.hidden_size = hidden_size
        self.directions = 2 if bidirectional else 1
        self.device = device

        # LSTM layer
        self.lstm = nn.LSTM(input_size=mfcc_size,
                            hidden_size=hidden_size,
                            num_layers=num_layers,
                            dropout=dropout,
                            bidirectional=bidirectional,
                            batch_first=True)

        # Fully connected layer for classification
        self.classifier = nn.Linear(hidden_size * self.directions, num_classes)

    def forward(self, x):
        # Forward pass through LSTM
        lstm_out, (hn, cn) = self.lstm(x)

        # Extract the last layer's hidden state
        # If bidirectional, hn will have shape [num_layers * directions, batch_size, hidden_size]
        hn = hn[-self.directions:]  # Take the last hidden state for both directions

        # Reshape or concatenate if bidirectional
        if self.directions == 2:
            hn = torch.cat((hn[0], hn[1]), dim=1)  # Combine the last hidden states from both directions

        # Now hn should have the shape [batch_size, hidden_size * directions]
        out = self.classifier(hn)  # Shape [batch_size, num_classes]
        return out


# Пример инициализации модели


