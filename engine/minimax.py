from .evaluate import evaluate_board
from .zobrist import ZobristHasherBase
import numpy as np
import chess

from .nn_eval import initialize_model
from .move_ordering import move_order

def get_best_move(board: chess.Board,
                  depth: int,
                  zobrist: ZobristHasherBase,
                  transposition_table: dict,
                  iterative_deepening = True,
                  verbose: bool = False):
    
    model = initialize_model('./engine/nn/models/model_transformer.pth')
    
    best_move = None

    # Initialize best_value for the minimizing player (black) - The bot
    best_value = float('inf')
    move_value = {}

    if iterative_deepening:
        for d in range(1, depth + 1):
            for move in move_order(board):
                board.push(move)
                board_value = minimax(board,
                                    d,                    # cannot be d-1 in iterative deepening because of zoobrish
                                    float('-inf'),
                                    float('inf'),
                                    True,
                                    zobrist,
                                    transposition_table,
                                    model)
                
                board.pop()
                
                # transposition_table.clear()
                
                move_value[move] = board_value

                if board_value <= best_value:
                    best_value = board_value
                    best_move = move
                    
    else:
        for move in move_order(board):
                board.push(move)
                board_value = minimax(board,
                                    depth - 1,
                                    float('-inf'),
                                    float('inf'),
                                    True,
                                    zobrist,
                                    transposition_table,
                                    model)
                board.pop()
                
                move_value[move] = board_value

                if board_value <= best_value:
                    best_value = board_value
                    best_move = move
                
    if verbose:  
        for move, value in move_value.items():
            print(f'Move: {move} value: {value}')

    return best_move, best_value, transposition_table


def minimax(board: chess.Board,
            depth: int,
            alpha: float,
            beta: float,
            maximizing_player: bool,
            zobrist: ZobristHasherBase,
            transposition_table: dict,
            model):
    
    zobrist_hash = zobrist.compute_zobrist_hash(board)
    
    if zobrist_hash in transposition_table:
        return transposition_table[zobrist_hash]
    
    if depth == 0 or board.is_game_over():
        eval = evaluate_board(board, model)
        transposition_table[zobrist_hash] = eval
        return eval

    if maximizing_player:
        max_eval = float('-inf')
        
        for move in move_order(board):
            board.push(move)
            eval = minimax(board,
                           depth-1,
                           alpha,
                           beta,
                           False,
                           zobrist,
                           transposition_table,
                           model)
            board.pop()
            
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break

        transposition_table[zobrist_hash] = max_eval
                
        return max_eval
    
    else:
        min_eval = float('inf')
        for move in move_order(board):
            board.push(move)
            eval = minimax(board,
                           depth-1,
                           alpha,
                           beta,
                           True,
                           zobrist,
                           transposition_table,
                           model)
            board.pop()
            
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
            
        transposition_table[zobrist_hash] = min_eval
                
        return min_eval
