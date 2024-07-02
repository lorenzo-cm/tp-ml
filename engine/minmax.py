import time

from .evaluate import evaluate_board

def get_best_move(board, depth, time_limit):
    start_time = time.time()
    best_move = None

    # Initialize best_value for the maximizing player (white)
    best_value = float('-inf')

    for move in board.legal_moves:
        board.push(move)
        board_value = minimax(board, depth - 1, float('-inf'), float('inf'), False, time_limit, start_time)
        board.pop()

        if board_value > best_value:
            best_value = board_value
            best_move = move

        if time.time() - start_time > time_limit:
            break

    return best_move


def minimax(board, depth, alpha, beta, maximizing_player, time_limit, start_time):
    if time.time() - start_time > time_limit:
        return evaluate_board(board)

    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    if maximizing_player:
        max_eval = float('-inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth-1, alpha, beta, False, time_limit, start_time)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth-1, alpha, beta, True, time_limit, start_time)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval
