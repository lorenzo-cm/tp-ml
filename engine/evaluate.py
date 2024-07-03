import chess
import chess.pgn

# Define the piece values
piece_values = {
    chess.PAWN: 100,
    chess.KNIGHT: 300,
    chess.BISHOP: 300,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 10000  # Kings are not counted in material value
}

def evaluate_board(board):
    # Initialize counters for white and black
    white_material = 0
    black_material = 0

    # Iterate over all squares
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            value = piece_values[piece.piece_type]
            if piece.color == chess.WHITE:
                white_material += value
            else:
                black_material += value

    return white_material - black_material