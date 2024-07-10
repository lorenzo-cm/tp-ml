import numpy as np
import random
import chess

def generate_random_board():
    board = chess.Board()
    
    number_moves = np.random.choice(np.arange(151))
    
    for _ in range(number_moves):
        all_moves = list(board.legal_moves)
        random_move = random.choice(all_moves)
        board.push(random_move)
        if board.is_game_over():
            break
    
    return board