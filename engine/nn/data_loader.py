import os
import chess.pgn
from torch.utils.data import Dataset, DataLoader
import numpy as np

class PGNDataset(Dataset):
    def __init__(self, directory) -> None:
        super().__init__()
        self.directory = directory
        self.pgn_files = list_pgn_files(self.directory)
        
    def __len__(self):
        return len(self.pgn_files)
    
    def __getitem__(self, idx):return extract_features_labels(process_pgn(self.pgn_files[idx]))

def extract_features_labels(game):
    board = game.board()
    features = []
    labels = []
    result = game.headers["Result"]
    for move in game.mainline_moves():
        board.push(move)
        features.append(board_to_features(board))
        labels.append(result_to_label(result))
        
    features = np.array(features)
    labels = np.array(labels)

    # Shuffle features and labels together
    indices = np.arange(features.shape[0])
    np.random.shuffle(indices)
    features = features[indices]
    labels = labels[indices]

    return features, labels

def board_to_features(board):
    # Convert the board state to a suitable feature vector
    feature_vector = np.zeros(64)
    for i in range(64):
        piece = board.piece_at(i)
        if piece:
            feature_vector[i] = piece.piece_type
    return feature_vector.reshape(8,8)

def result_to_label(result):
    if result == "1-0":
        return 1
    elif result == "0-1":
        return 0
    else:
        return 0.5

def list_pgn_files(directory):
    pgn_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.pgn'):
                pgn_files.append(os.path.join(root, file))
    return pgn_files

def process_pgn(file_path):
    with open(file_path) as pgn_file:
        game = chess.pgn.read_game(pgn_file)
        return game


if __name__ == '__main__':
    
    dataset = PGNDataset('data')

    # [batch_size, len_match, len(board_x), len(board_y)]
    dataloader = DataLoader(dataset, shuffle=True)
    
    for i in dataloader:
        print(i[0].shape)
        break

