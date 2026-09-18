import sys, os
path = os.path.dirname(os.path.abspath('../database/database_update.py'))
if path not in sys.path:
    sys.path.append(path)
from datebase_update import get_fortnight_surv, get_many_surv, get_all_surv
from sklearn.metrics import mean_squared_error, mean_absolute_error, root_mean_squared_error

from datetime import datetime, timedelta
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import torch.optim as optim
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class FluDataset(Dataset):
    def __init__(self, data, split, split_size, window_size=30):
        self.window_size = window_size
        self.series = []
        self.state_to_idx = {state: i for i, state in enumerate(sorted(data["StateID"].unique()))}
        self.state_list = []
        data["CaseNum"] = np.log1p(data["CaseNum"])
        self.mean = data["CaseNum"].mean()
        self.std = data["CaseNum"].std()

        for state, group in data.groupby("StateID"):
            group["CaseNum"] = ((group["CaseNum"] - self.mean) / self.std)
            sid = self.state_to_idx[state]
        
            values = group["CaseNum"].to_numpy()

            # We split based on if we are creating a training dataset or testing dataset
            if split == "train":
                values = values[:(int(len(values)*split_size))]
            else:
                values = values[(int(len(values)*split_size)):]

            # Now we split the data into window size chuncks
            for i in range(len(values) - window_size):
                seq = values[i:i+window_size]
                label = values[i+window_size]
                self.series.append((seq, label, sid))
                self.state_list.append(state)
                
    def __len__(self):
        return len(self.series)
    
    def __getitem__(self, idx):
        seq, label, state_id = self.series[idx]
        return (torch.tensor(seq, dtype=torch.float32),torch.tensor(label, dtype=torch.float32), torch.tensor(state_id, dtype=torch.long),)

class FluRNN(nn.Module):
    def __init__(self, input_size=1, rnn_type="GRU", hidden_size=64, num_layers=2, num_states=60, embed_dim=8, bidirectional=True, dropout=0.2):
        super().__init__()

        self.embedding = nn.Embedding(num_states, embed_dim)
        self.hidden_size = hidden_size
        self.rnn_type = rnn_type
        self.num_direct = 2
        
        if self.rnn_type == "GRU":
            self.rnn = nn.GRU(input_size + embed_dim, hidden_size, num_layers, batch_first=True, bidirectional=bidirectional, dropout=dropout)
        elif self.rnn_type == "LSTM":
            self.rnn = nn.LSTM(input_size + embed_dim, hidden_size, num_layers, batch_first=True, bidirectional=bidirectional, dropout=dropout)
        else:
            self.rnn = nn.RNN(input_size + embed_dim, hidden_size, num_layers, batch_first=True, bidirectional=bidirectional, dropout=dropout, nonlinearity="tanh")
            
        self.fc = nn.Sequential(nn.Linear(hidden_size * self.num_direct, hidden_size // 2),
                                nn.ReLU(),
                                nn.Dropout(dropout),
                                nn.Linear(hidden_size // 2, 1))

    def forward(self, x, state_id, return_embedding=False):
        batch_size, seq_len = x.size()

        embeds = self.embedding(state_id)
        embeds = embeds.unsqueeze(1).repeat(1, seq_len, 1)
        
        x = x.unsqueeze(-1)
        rnn_input = torch.cat((x, embeds), dim=2)
        output, _ = self.rnn(rnn_input)
        last = output[:, -1, :]
        pred = self.fc(last)

        if return_embedding:
            return pred.squeeze(1), last
        else:
            return pred.squeeze(1)

class FluRNNEncoder(nn.Module):
    def __init__(self, checkpoint_path, input_size=1, hidden_size=64, num_layers=2, num_states=60, embed_dim=8, bidirectional=True, dropout=0.2):
        super().__init__()
        self.encoder = FluRNN(input_size, "GRU", hidden_size, num_layers, num_states, embed_dim, bidirectional, dropout)
        checkpoint = torch.load(checkpoint_path, weights_only=False)
        self.encoder.load_state_dict(checkpoint["model_state_dict"])
        self.encoder.eval()
        
    @torch.no_grad()
    def encode(self, x,state_id):
        embedding = self.encoder(x, state_id, return_embedding=True)
        return embedding
        
def state_index(dataset):
    state_index = {}
    for i, state in enumerate(dataset.state_list):
        if state not in state_index:
            index_list = []
            index_list.append(i)
            state_index[state] = index_list
        else:
            state_index[state].append(i)
    return state_index
    
def state_loaders(dataset, batch_size=32, shuffle=True):
    indices = state_index(dataset)
    dataloaders = {}
    for state, index in indices.items():
        subset = torch.utils.data.Subset(dataset, index)
        loader = DataLoader(subset, batch_size=batch_size, shuffle=shuffle)
        dataloaders[state] = loader
    return dataloaders
    
#model_rnn = FluRNN(rnn_type="RNN")
#model_gru = FluRNN(rnn_type="GRU")
#model = FluRNN(rnn_type="GRU")
#models = [model_lstm]


#df = get_all_surv()
#train_size = 0.9

#train_dataset = FluDataset(df, "train", train_size)
#test_dataset = FluDataset(df, "test", train_size)

#dataloaders = state_loaders(train_dataset)
#dataloader = DataLoader(train_dataset, batch_size=32, shuffle=True)
def asymmetric_mse_loss(y_pred, y_true, underweight=1.4):
    diff = y_pred - y_true
    weights = torch.where(diff < 0, underweight, 1.0)
    return torch.mean(weights * diff**2)


def reverse_norm(value, state_id, dataset):
    state_id = state_id.cpu().detach().numpy()
    mean = dataset.mean
    std = dataset.std
    np_pred = value.cpu().detach().numpy()
    np_pred = np.expm1(np_pred * std + mean)
   
    return np_pred

#optimizer = optim.Adam(model.parameters(), lr=1e-4, weight_decay=1e-5)
#criterion = asymmetric_mse_loss
#for epoch in range(26):
 #   model.train()
 #   total_loss = 0
 #   num_batches = 0
 #   for state_id, loader in dataloaders.items():
  #      for x, y_true, state_id in loader:
  #          optimizer.zero_grad()
  #          y_pred = model(x, state_id)
  #          loss = criterion(y_pred, y_true)
  #          loss.backward()
  #          torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
  #          optimizer.step()
  #          total_loss += loss.item()
  #          num_batches += 1
  #  avg_loss = total_loss / num_batches
  #  print(f"Epoch {epoch}: loss = {avg_loss:.4f}")
#torch.save({
 #   "model_state_dict": model.state_dict(),
 #   "state_to_idx": train_dataset.state_to_idx,
 #   "data_mean": train_dataset.mean,
 #   "data_std": train_dataset.std,
 #    }, "/srv/scratch/z5397970/v2_rnn/flu_rnn_model.pt")

def evaluate(pred, true):
    print("Mean square error " + str(mean_squared_error(true, pred)))
    print("Mean absolute error " + str(mean_absolute_error(true, pred)))
    print("Root mean sqare error " + str(root_mean_squared_error(true, pred)))

#model.eval()
#testloader = DataLoader(test_dataset, batch_size=100, shuffle=False)
#with torch.no_grad():
#for state_id, loader in testloader.items():
   # x, y_true, state_id = next(iter(testloader))
   # y_pred_rnn = model_rnn(x, state_id)
   # y_pred_gru = model_gru(x, state_id)
    #y_pred_lstm = model(x, state_id)

   # y_lstm_real = reverse_norm(y_pred_lstm, state_id, train_dataset)
   # y_true_real = reverse_norm(y_true, state_id, train_dataset)
  #  y_rnn_real = reverse_norm(y_pred_rnn, state_id, train_dataset)
   # y_gru_real = reverse_norm(y_pred_gru, state_id, train_dataset)
    

   # print("RNN")
   # evaluate(y_true_real, y_rnn_real)
  #  print("GRU")
   # evaluate(y_true_real, y_gru_real)
  #  print("LSTM")
  #  evaluate(y_true_real, y_lstm_real)

   # plt.figure(figsize=(10, 6))
   # plt.plot(y_true_real, label="true", color="red", marker='o')
   # plt.plot(y_rnn_real, label="Vanilla RNN", color="deepskyblue", marker='x')
  #  plt.plot(y_gru_real, label="GRU", color="green", marker='x')
   # plt.plot(y_lstm_real, label="LSTM", color="purple", marker='x')
   # plt.legend()
   # plt.savefig("lstm.png")
