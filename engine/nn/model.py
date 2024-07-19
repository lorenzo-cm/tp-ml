import torch
import torch.nn as nn

class ChessModel(nn.Module):
    def __init__(self, input_dim=14, d_model=128, nhead=8, num_encoder_layers=3, dim_feedforward=512, dropout=0.1):
        super(ChessModel, self).__init__()
        self.conv1 = nn.Conv2d(input_dim, d_model, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm2d(d_model)
        
        self.positional_encoding = PositionalEncoding(d_model, dropout)
        
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model, 
            nhead=nhead, 
            dim_feedforward=dim_feedforward, 
            dropout=dropout,
            batch_first=True
        )
        self.transformer_encoder = nn.TransformerEncoder(encoder_layer, num_layers=num_encoder_layers)
        
        self.fc1 = nn.Linear(d_model * 8 * 8, 1024)
        self.dropout = nn.Dropout(dropout)
        self.fc2 = nn.Linear(1024, 1)

    def forward(self, x):
        x = torch.relu(self.bn1(self.conv1(x)))  # (batch_size, d_model, 8, 8)
        
        x = x.flatten(2).permute(0, 2, 1)  # (batch_size, d_model, 8*8) -> (batch_size, 8*8, d_model)
        
        x = self.positional_encoding(x)
        
        x = self.transformer_encoder(x)  # (batch_size, 8*8, d_model)
        
        x = x.contiguous().view(x.size(0), -1)  # (batch_size, 8*8*d_model)
        
        x = torch.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.fc2(x)
        
        return x.squeeze()

class PositionalEncoding(nn.Module):
    def __init__(self, d_model, dropout=0.1, max_len=64):
        super(PositionalEncoding, self).__init__()
        self.dropout = nn.Dropout(p=dropout)

        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-torch.log(torch.tensor(10000.0)) / d_model))
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        pe = pe.unsqueeze(0)
        self.register_buffer('pe', pe)

    def forward(self, x):
        x = x + self.pe[:, :x.size(1), :]
        return self.dropout(x)
