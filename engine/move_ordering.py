import chess

def move_order(board):
    legal_moves = list(board.legal_moves)
    legal_moves.sort(key=lambda move: (board.gives_check(move), board.is_capture(move), move_creates_threat(board,move)), reverse=True)
    return legal_moves

def move_creates_threat(board, move):
    color_to_move = board.turn
    board.push(move)
    threat = 0
    
    to_square = move.to_square
    attacked_squares = list(board.attacks(to_square))
    
    for square in attacked_squares:
        piece_in_square = board.piece_at(square)
        if piece_in_square != None and piece_in_square.color != color_to_move:
            threat += weights[piece_in_square.piece_type]
    
    board.pop()
    return threat

weights = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 200
}