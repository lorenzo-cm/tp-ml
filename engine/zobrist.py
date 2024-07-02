import chess
import random

def initialize_zobrist():
    table = {}
    pieces = [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN, chess.KING]
    colors = [chess.WHITE, chess.BLACK]
    
    for piece in pieces:
        for color in colors:
            for square in chess.SQUARES:
                table[(piece, color, square)] = random.getrandbits(64)
    
    # Hash for castling rights
    table['castling'] = [random.getrandbits(64) for _ in range(16)]
    
    # Hash for en passant
    table['en_passant'] = [random.getrandbits(64) for _ in range(8)]
    
    # Hash for side to move
    table['turn'] = random.getrandbits(64)
    
    return table


def compute_zobrist_hash(board, zobrist_table):
    hash_value = 0
    
    # Piece positions
    for square, piece in board.piece_map().items():
        if piece:
            piece_type = piece.piece_type
            color = piece.color
            hash_value ^= zobrist_table[(piece_type, color, square)]
    
    # Castling rights
    castling_index = castling_rights_index(board)
    hash_value ^= zobrist_table['castling'][castling_index]
    
    # En passant
    if board.ep_square:
        ep_file = chess.square_file(board.ep_square)
        hash_value ^= zobrist_table['en_passant'][ep_file]
    
    # Side to move
    if board.turn == chess.WHITE:
        hash_value ^= zobrist_table['turn']
    
    return hash_value


def castling_rights_index(board):
    index = 0
    if board.has_kingside_castling_rights(chess.WHITE):
        index |= 1
    if board.has_queenside_castling_rights(chess.WHITE):
        index |= 2
    if board.has_kingside_castling_rights(chess.BLACK):
        index |= 4
    if board.has_queenside_castling_rights(chess.BLACK):
        index |= 8
    return index