import chess
from config import *

def get_square(row, col):
    return chess.square(col, 7 - row)

def get_piece(board, row, col):
    if 0 <= row < 8 and 0 <= col < 8:
        piece = board.piece_at(get_square(row, col))
        return piece
    else:
        raise ValueError("Row and column must be in the range 0-7 inclusive.")
    
def get_piece_moves(board, row, col):
    legal_moves = list(board.legal_moves)
    
    # Filter moves to include only those for the piece on the specified square
    piece_moves = [move for move in legal_moves if move.from_square == get_square(row, col)]
    
    destination_squares = chess.SquareSet(move.to_square for move in piece_moves)
    
    return destination_squares
    
def pos_to_rowcol(x, y):
    """Returns row, col"""
    
    if x <= PADDING or y <= PADDING or x >= (WINDOW_SIZE-PADDING) or y >= (WINDOW_SIZE-PADDING):
        return -1, -1
    
    adjusted_x = x-PADDING
    adjusted_y = y-PADDING
    
    return adjusted_y//SQUARE_SIZE, adjusted_x//SQUARE_SIZE
  
def handle_click(board, x, y):
    """Handle the click and return the list of possible moves for the clicked square and the selected square """
    row, col = pos_to_rowcol(x, y)
    
    # check invalid position
    if row == -1 or col == -1:
        return None, None
    
    piece = get_piece(board, row, col)
    
    # check if no piece is found
    if not piece:
        return None, get_square(row, col)
    
    print(piece, 'White' if piece.color else 'Black')
    
    return get_piece_moves(board, row, col), get_square(row, col)