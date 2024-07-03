from .evaluate import evaluate_board
from .zobrist import compute_zobrist_hash

def get_best_move(board, depth, zobrist_table, transposition_table):
    # positions, zobrist, collisions
    count = [0, 0, 0]
    best_move = None

    # Initialize best_value for the minimizing player (black)
    best_value = float('inf')

    for move in board.legal_moves:
        board.push(move)
        board_value = minimax(board, depth - 1, float('-inf'), float('inf'), True, count, zobrist_table, transposition_table)
        board.pop()

        if board_value < best_value:
            best_value = board_value
            best_move = move

    print(count)

    return best_move, transposition_table


def minimax(board, depth, alpha, beta, maximizing_player, count, zobrist_table, transposition_table):
    
    zobrist_hash = compute_zobrist_hash(board, zobrist_table)

    if zobrist_hash in transposition_table:
        count[1] += 1
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
            eval = minimax(board, depth-1, alpha, beta, False, count, zobrist_table, transposition_table)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        if transposition_table.get(zobrist_hash):
            count[2]+=1
        transposition_table[zobrist_hash] = max_eval
        return max_eval
    
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth-1, alpha, beta, True, count, zobrist_table, transposition_table)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        if transposition_table.get(zobrist_hash):
            count[2]+=1
        transposition_table[zobrist_hash] = min_eval
        return min_eval
