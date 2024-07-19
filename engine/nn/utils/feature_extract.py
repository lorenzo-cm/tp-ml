import chess
import numpy as np
from stockfish import Stockfish

def initialize_stockfish(path):
    stockfish = Stockfish(path)
    stockfish.set_skill_level(20)
    stockfish.set_depth(20)
    return stockfish

def get_position_score(stockfish, board: chess.Board) -> dict:
    
    if board.is_checkmate():
        return -1000 if board.turn else 1000
    
    stockfish.set_fen_position(board.fen())
    evaluation = stockfish.get_evaluation()
    
    score = 0
    if evaluation['type'] == 'cp':
        score = evaluation['value'] / 100
    else:
        score = np.tanh(5 / evaluation['value']) * 25

    return score

def create_piece_matrix(board):
    piece_matrix = np.zeros((12, 8, 8), dtype=int)
    piece_types = [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN, chess.KING]

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            piece_index = piece_types.index(piece.piece_type)
            if piece.color == chess.BLACK:
                piece_index += 6
            row, col = divmod(square, 8)
            piece_matrix[piece_index][row][col] = 1

    return piece_matrix

def create_move_matrix(board):
    initial_turn = board.turn
    
    white_moves_matrix = np.zeros((8, 8), dtype=int)
    black_moves_matrix = np.zeros((8, 8), dtype=int)

    board.turn = True
    for move in board.legal_moves:
        to_square = move.to_square
        row, col = divmod(to_square, 8)
        white_moves_matrix[row][col] = 1
    
    board.turn = False
    for move in board.legal_moves:
        to_square = move.to_square
        row, col = divmod(to_square, 8)
        black_moves_matrix[row][col] = 1
            
    board.turn = initial_turn

    return white_moves_matrix, black_moves_matrix

def create_feature_matrix(board):
    piece_matrix = create_piece_matrix(board)
    white_moves_matrix, black_moves_matrix = create_move_matrix(board)
    
    feature_matrix = np.vstack([
        piece_matrix,
        white_moves_matrix[np.newaxis, :, :],
        black_moves_matrix[np.newaxis, :, :]
    ])

    return feature_matrix