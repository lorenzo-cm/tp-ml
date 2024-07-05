from .evaluate import evaluate_board, evaluate_board_stockfish
from .zobrist import ZobristHasherBase
import numpy as np
import chess

pruning = [0, 0]

def get_best_move(board: chess.Board,
                  depth: int,
                  zobrist: ZobristHasherBase,
                  transposition_table: dict,
                  verbose: bool = False):
    
    global pruning
    pruning = [0, 0]
    
    # positions, zobrist, collisions, len_table
    count = [0, 0, 0, 0]
    best_move = None

    # Initialize best_value for the minimizing player (black)
    best_value = float('inf')
    move_value = {}

    for move in board.legal_moves:
        
        board.push(move)
        board_value = minimax(board,
                              depth - 1,
                              float('-inf'),
                              float('inf'),
                              True,
                              count,
                              zobrist,
                              transposition_table)
        board.pop()
        
        move_value[move] = board_value

        if board_value <= best_value:
            best_value = board_value
            best_move = move
            
    count[3] += len(transposition_table)
    
    if verbose:
        print(f'\nCount moves analysed: {count[0]}\nZobrist uses: {count[1]}\nHash table Collisions: {count[2]}\nLen table: {count[3]}\n')
        
        print('pruning ', pruning, ' => ', pruning[0]+pruning[1])
        
        for move, value in move_value.items():
            print(f'Move: {move} value: {value}')

    return best_move, best_value, transposition_table


def minimax(board: chess.Board,
            depth: int,
            alpha: float,
            beta: float,
            maximizing_player: bool,
            count: int,
            zobrist: ZobristHasherBase,
            transposition_table: dict):
    
    count[0] += 1
    
    zobrist_hash = zobrist.compute_zobrist_hash(board)
    
    if zobrist_hash in transposition_table:
        count[1] += 1
        return transposition_table[zobrist_hash]
    
    if depth == 0 or board.is_game_over():
        eval = evaluate_board(board)
        
        
        if transposition_table.get(zobrist_hash):
            count[2] += 1
        
        transposition_table[zobrist_hash] = eval
            
        return eval

    if maximizing_player:
        max_eval = float('-inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board,
                           depth-1,
                           alpha,
                           beta,
                           False,
                           count,
                           zobrist,
                           transposition_table)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                pruning[0] += 1
                break
            
        if transposition_table.get(zobrist_hash):
            count[2]+=1

        transposition_table[zobrist_hash] = max_eval
                
        return max_eval
    
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board,
                           depth-1,
                           alpha,
                           beta,
                           True,
                           count,
                           zobrist,
                           transposition_table)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                pruning[1] += 1
                break
        
        if transposition_table.get(zobrist_hash):
            count[2] += 1
            
        transposition_table[zobrist_hash] = min_eval
                
        return min_eval
