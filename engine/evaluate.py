import chess
import chess.pgn
import numpy as np

# Define the piece values
weights = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 200,
    'mobility': 0.1,
    'qnt_attack_squares': 0.05,
}

def evaluate_board(board: chess.Board):    
    if board.is_checkmate():
        return np.inf
    
    if board.is_stalemate():
        return 0
    
    mobility_b = board.legal_moves.count()
    board.turn = not board.turn
    mobility_w = board.legal_moves.count()
    board.turn = not board.turn
    
    mobility_score = weights['mobility'] * (mobility_w - mobility_b)
    
    white_material = 0
    black_material = 0
    
    count_attack_squares_w = 0
    count_attack_squares_b = 0
    
    for square, piece in board.piece_map().items():
        if board.is_attacked_by(chess.BLACK, square):
            count_attack_squares_b += 1
        
        if board.is_attacked_by(chess.WHITE, square):
            count_attack_squares_w += 1
        
        if piece:
            value = weights[piece.piece_type]
            if piece.color == chess.WHITE:
                white_material += value
            else:
                black_material += value
                
    count_attack_squares_score = weights['qnt_attack_squares'] * (count_attack_squares_w - count_attack_squares_b)
    
    material_score = white_material - black_material
    
    score = material_score + count_attack_squares_score + mobility_score

    return score