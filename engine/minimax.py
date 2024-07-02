import time

from .evaluate import evaluate_board
from .zobrist import compute_zobrist_hash

transposition_table = {}

def get_best_move(board, depth, zobrist_table):
    count = [0]
    best_move = None

    # Initialize best_value for the minimizing player (black)
    best_value = float('inf')

    for move in board.legal_moves:
        board.push(move)
        board_value = minimax(board, depth - 1, float('-inf'), float('inf'), True, count, zobrist_table)
        board.pop()

        if board_value < best_value:
            best_value = board_value
            best_move = move

    print(count[0])

    return best_move


def minimax(board, depth, alpha, beta, maximizing_player, count, zobrist_table):
    
    zobrist_hash = compute_zobrist_hash(board, zobrist_table)

    if zobrist_hash in transposition_table:
        return transposition_table[zobrist_hash]
    
    if depth == 0 or board.is_game_over():
        count[0] += 1
        eval = evaluate_board(board)
        transposition_table[zobrist_hash] = eval
        return eval

    if maximizing_player:
        max_eval = float('-inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth-1, alpha, beta, False, count, zobrist_table)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        transposition_table[zobrist_hash] = max_eval
        return max_eval
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth-1, alpha, beta, True, count, zobrist_table)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        transposition_table[zobrist_hash] = min_eval
        return min_eval
