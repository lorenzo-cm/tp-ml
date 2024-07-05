import chess
from typing import Dict

def piece2squareDICT(board) -> Dict[chess.Piece, int]:
    piece2square = {}
    for square, piece in board.piece_map().items():
        if piece in piece2square:
            piece2square[piece].append(square)
        else:
            piece2square[piece] = [square]
    return piece2square

def is_passed_pawn(board: chess.Board, square: chess.Square, color: bool):
    """
    Verifica se um peão é passado.
    """
    file = chess.square_file(square)
    rank = chess.square_rank(square)
    
    if color == chess.WHITE:
        # Checar se não há peões pretos nas colunas adjacentes nas filas à frente
        for dfile in [-1, 0, 1]:
            if 0 <= file + dfile < 8:
                for drank in range(rank + 1, 8):
                    if board.piece_at(chess.square(file + dfile, drank)) == chess.Piece(chess.PAWN, chess.BLACK):
                        return False
    else:
        # Checar se não há peões brancos nas colunas adjacentes nas filas à frente
        for dfile in [-1, 0, 1]:
            if 0 <= file + dfile < 8:
                for drank in range(rank - 1, -1, -1):
                    if board.piece_at(chess.square(file + dfile, drank)) == chess.Piece(chess.PAWN, chess.WHITE):
                        return False
    
    return True