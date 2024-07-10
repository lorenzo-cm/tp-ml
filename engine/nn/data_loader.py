from torch.utils.data import Dataset, DataLoader, random_split
import h5py
import torch
import numpy as np

class ChessDataset(Dataset):
    def __init__(self, hdf5_file):
        self.hdf5_file = hdf5_file
        self.dataset = h5py.File(hdf5_file, 'r')
        self.data = self.dataset['features'][:]
        self.labels = self.dataset['labels'][:]
        
        # Talvez a diferença muito grande do score pode atrapalhar o modelo
        self.labels = np.tanh(self.labels)
        
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        data_point = self.data[idx]
        label = self.labels[idx]
        
        return torch.tensor(data_point, dtype=torch.float32), torch.tensor(label, dtype=torch.float32)

def split_dataset():
    hdf5_file = 'data/merged_chess_dataset.h5'
    dataset = ChessDataset(hdf5_file)

    train_ratio = 0.95

    train_length = int(train_ratio * len(dataset))
    valid_length = len(dataset) - train_length

    train_dataset, valid_dataset = random_split(dataset, [train_length, valid_length])
    
    train_dataloader = DataLoader(train_dataset, batch_size=64, shuffle=True, num_workers=4)
    valid_dataloader = DataLoader(valid_dataset, batch_size=64, shuffle=False, num_workers=4)
    
    return train_dataloader, valid_dataloader
