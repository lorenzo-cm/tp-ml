import torch
import numpy as np

from .nn.model import ChessModel
from .nn.utils.feature_extract import create_feature_matrix

def initialize_model(model_path):
    model = ChessModel()
    model.load_state_dict(torch.load(model_path))
    model.eval()
    return model

def model_eval(model, board):
    base_eval = 0
    with torch.no_grad():
        base_eval = model(torch.tensor(create_feature_matrix(board), dtype=torch.float32).unsqueeze(0))
    return process_eval(base_eval)

def process_eval(eval, constant=12, exponent=3, limit=5):
    new_eval = constant * (abs(eval) ** exponent)
    
    new_eval = new_eval / (1 + np.abs(eval))
    
    if eval < 0:
        return max(-new_eval, -limit)
    else:
        return min(new_eval, limit)