import sys, os
path = os.path.dirname(os.path.abspath('../database/database_update.py'))
if path not in sys.path:
    sys.path.append(path)
from datebase_update import get_fortnight_surv, get_many_surv

from datetime import datetime, timedelta
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import torch.optim as optim
import numpy as np


states = [1, 2, 3, 4, 5, 6, 7, 8, 9]

class FluDataset(Dataset):
    def __init__(self, df, window_size=10):
        self.window_size = window_size
        self.states = states
        self.series = []
        
        for state in states:
            start = datetime.strptime("2017-01-01", "%Y-%m-%d")
            for i in range(20 - window_size):
                window_start = start + timedelta(days=(i * 14))
                window_end = window_start + timedelta(days=(window_size*14))
                df = get_many_surv(state, window_start, window_end)[0].tolist()
                self.series.append(df)
        self.series = np.log1p(self.series)
        
        # standardize
        self.mean = self.series.mean()
        self.std = self.series.std()
        series = (series - self.mean) / self.std


    def __len__(self):
        return len(self.series)
    
    def __getitem__(self, idx):
        return torch.tensor(self.series[idx], dtype=torch.float32)

class FluRNN(nn.Module):
    def __init__(self, input_size, hidden_size=128, num_layers=1):
        super().__init__()
        self.gru = nn.GRU(input_size, hidden_size, num_layers, batch_first=True)
        self.linear = nn.Linear(hidden_size, 1)

    def forward(self, x):
        # out = self.rnn(x)
        # final = self.linear(out)
        # return final
        _, h = self.gru(x)
        out = self.linear(h[-1])
        return out

model = FluRNN(input_size=1)
optimizer = optim.Adam(model.parameters(), lr=1e-3)
criterion = nn.MSELoss()
df = []
dataloader = DataLoader(FluDataset(df), batch_size=32, shuffle=True)

for epoch in range(20):
    for x in dataloader:
        y_true = x[:, -1]
        x = x.unsqueeze(-1)
        y_pred = model(x).squeeze()
        loss = criterion(y_pred, y_true)
        break
    print(y_true[:10])
    print(y_pred[:10])
       # optimizer.zero_grad()
       # loss.backward()
       # optimizer.step()
    print(f"Epoch {epoch}: loss = {loss.item():.4f}")

