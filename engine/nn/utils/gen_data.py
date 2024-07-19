import h5py
import numpy as np
from feature_extract import *
from random_board import generate_random_board

stockfish = initialize_stockfish("../../../stockfish/stockfish-ubuntu-x86-64-avx2")

num_samples = 10000
file_name = 'chess_data3.h5'

features = []
labels = []

for i in range(num_samples):
    print(f"Generating sample {i + 1}/{num_samples}")
    board = generate_random_board()
    feature_matrix = create_feature_matrix(board)
    score = get_position_score(stockfish, board)
    
    features.append(feature_matrix)
    labels.append(score)

features = np.array(features)
labels = np.array(labels)

# Save data to HDF5 file
with h5py.File(file_name, 'w') as f:
    f.create_dataset('features', data=features)
    f.create_dataset('labels', data=labels)

print("Dataset saved successfully.")
