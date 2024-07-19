import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader
from torch.optim import Adam
import numpy as np

from data_loader import split_dataset
from model import ChessModel
from train import train_model

train_loader, valid_loader = split_dataset()

model = ChessModel()
criterion = nn.MSELoss()
optimizer = Adam(model.parameters(), lr=1e-4)

trained_model = train_model(model, train_loader, valid_loader, criterion, optimizer)

torch.save(trained_model.state_dict(), 'models/model_SAMPLE.pth')