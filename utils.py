import chess
from config import *

def get_square(row, col):
    return chess.square(col, 7 - row)

# def get_piece(board, row, col):
#     if 0 <= row < 8 and 0 <= col < 8:
#         piece = board.piece_at(get_square(row, col))
#         return piece
#     else:
#         raise ValueError("Row and column must be in the range 0-7 inclusive.")
    
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
    
    return get_piece_moves(board, row, col), get_square(row, col)

def check_game_over(board):
    game_over = False
    result_text = ''
    
    if board.is_checkmate():
        game_over = True
        result_text = "Black wins by checkmate!" if board.turn else "White wins by checkmate!"
    elif board.is_stalemate():
        game_over = True
        result_text = "Stalemate!"
    elif board.is_insufficient_material():
        game_over = True
        result_text = "Draw by insufficient material!"
    elif board.is_seventyfive_moves():
        game_over = True
        result_text = "Draw by 75-move rule!"
    elif board.is_fivefold_repetition():
        game_over = True
        result_text = "Draw by fivefold repetition!"
        
    return game_over, result_text

def opening_move(number_moves):
    if number_moves == 1:
        return chess.Move.from_uci('e7e5')
    if number_moves == 2:
        return chess.Move.from_uci('b8c6')