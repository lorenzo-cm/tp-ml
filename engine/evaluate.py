import chess
import chess.pgn
import numpy as np
from .utils_engine import *

def evaluate_board(board: chess.Board):    
    
    initial_turn = board.turn
    
    if board.is_checkmate():
        print('checkmate')
        return -np.inf if board.turn else np.inf
    
    if board.is_stalemate():
        return 0
    
    board.turn = chess.WHITE
    mobility_w = len(list(board.legal_moves))
    
    board.turn = chess.BLACK
    mobility_b = len(list(board.legal_moves))
    
    board.turn = initial_turn
    
    mobility_score = weights['mobility'] * (mobility_w - mobility_b)
    
    white_material = 0
    black_material = 0
    
    count_attack_squares_w = 0
    count_attack_squares_b = 0
    
    for square in range(64):
        if board.is_attacked_by(chess.BLACK, square):
            count_attack_squares_b += 1
        
        if board.is_attacked_by(chess.WHITE, square):
            count_attack_squares_w += 1
        
        piece = board.piece_at(square)
        
        if piece:
            value = weights[piece.piece_type]
            if piece.color == chess.WHITE:
                white_material += value
            else:
                black_material += value
                
    count_attack_squares_score = weights['qnt_attack_squares'] * (count_attack_squares_w - count_attack_squares_b)
    
    material_score = white_material - black_material
    
    endgame_score = 0
    if board.fullmove_number >= 30:
        endgame_score = endgame_score_bonus(board)
    
    pawn_score = 0
    if board.fullmove_number >= 20:
        pawn_score = passed_pawn_score(board)
            
    # print('Material ', material_score)
    # print('Attack squares ', count_attack_squares_score)
    # print('Mobility ', mobility_score)
    # print('Endgame score: ', endgame_score)
    # print('pawn score: ', pawn_score)
    
    score = material_score + count_attack_squares_score + mobility_score + endgame_score + pawn_score

    return score


# Define the piece values
weights = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 200,
    'mobility': 0.045,
    'qnt_attack_squares': 0.075,
}


def endgame_score_bonus(board: chess.Board, weight=2.25):
    initial_turn = board.turn
    
    piece2square = piece2squareDICT(board)
    
    ally_king_square = piece2square[chess.Piece(chess.KING, initial_turn)][0]
    enemy_king_square = piece2square[chess.Piece(chess.KING, not initial_turn)][0]
    
    # more -> worse
    # danger score
    ally_king_danger_score = 0
    enemy_king_danger_score = 0
    
    ally_pieces_count = 0
    enemy_pieces_count = 0
    
    for square, piece in board.piece_map().items():
        
        if piece.piece_type == chess.KING:
            continue
        
        if piece.color == initial_turn:
            ally_pieces_count += 1
            enemy_king_danger_score += (weights[piece.piece_type]**1.5) * 0.5/(np.abs(chess.square_distance(square, enemy_king_square)))
                
        else:
            enemy_pieces_count += 1
            ally_king_danger_score += (weights[piece.piece_type]**1.5) * 0.5/(np.abs(chess.square_distance(square, ally_king_square)))


    # print('ally ', ally_king_danger_score, ' enemy ', enemy_king_danger_score)
    # print('count: ', ally_pieces_count, ' e ', enemy_pieces_count)

    ally_king_danger_score /= enemy_pieces_count + 0.00031247533457532
    enemy_king_danger_score /= ally_pieces_count + 0.00031247533457532
    
    # print('ally ', ally_king_danger_score, ' enemy ', enemy_king_danger_score)
    
    score = 0
    
    if initial_turn:
        score = -(ally_king_danger_score - enemy_king_danger_score)
        
    else:
        score = (ally_king_danger_score - enemy_king_danger_score)
                
    return score * weight
    
    
def passed_pawn_score(board: chess.Board):
    """
    Avalia o tabuleiro com base na posição dos peões.
    
    Pontua peões avançados, passados e passados avançados.
    """
    score = 0
    
    # Definindo pesos para os diferentes estados dos peões
    pawn_advanced_weight = 0.1
    passed_pawn_weight = 0.25
    passed_pawn_advanced_weight = 0.4
    
    # Avaliando cada peão no tabuleiro
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        
        if piece and piece.piece_type == chess.PAWN:
            rank = chess.square_rank(square)
            file = chess.square_file(square)
            if piece.color == chess.WHITE:
                # Peão branco
                advancement = rank  # Rank vai de 0 (8ª fileira) a 7 (1ª fileira)
                if advancement > 1:  # Peão avançado
                    score += pawn_advanced_weight * advancement
                    
                if is_passed_pawn(board, square, chess.WHITE):
                    score += passed_pawn_weight
                    if advancement > 3:
                        score += passed_pawn_advanced_weight * advancement
            
            else:
                # Peão preto
                advancement = 7 - rank  # Rank vai de 7 (1ª fileira) a 0 (8ª fileira)
                if advancement > 1:  # Peão avançado
                    score -= pawn_advanced_weight * advancement
                    
                if is_passed_pawn(board, square, chess.BLACK):
                    score -= passed_pawn_weight
                    if advancement > 3:
                        score -= passed_pawn_advanced_weight * advancement

    return score


def king_winning_goes_to_combat(board: chess.Board, current_score, weight=1.5, threshold=15):
    """
    Evaluate the board giving a higher score if the king moves towards the other king,
    but only if one side is significantly winning.
    """
    initial_turn = board.turn

    # Check if one side is significantly winning
    if abs(current_score) < threshold:
        return 0

    piece2square = piece2squareDICT(board)
    
    ally_king_square = piece2square[chess.Piece(chess.KING, initial_turn)][0]
    enemy_king_square = piece2square[chess.Piece(chess.KING, not initial_turn)][0]
    
    # Calculate the distance between the two kings
    king_distance = chess.square_distance(ally_king_square, enemy_king_square)
    
    # Reward closer distances
    score = (8 - king_distance) * weight
    
    # If the current side is losing, negate the score
    if (score < 0 and initial_turn) or (score > 0 and not initial_turn):
        score = -score

    return score


def evaluate_board_stockfish(board):
    stockfish_path = "./stockfish/stockfish-ubuntu-x86-64-avx2"
    with chess.engine.SimpleEngine.popen_uci(stockfish_path) as engine:
        # Get the evaluation from Stockfish
        info = engine.analyse(board, chess.engine.Limit(time=0.08))

        # Extract the score
        score = info["score"].relative

        # Convert the score to centipawns or a mate in n
        if score.is_mate():
            mate_in = info["score"].pov(1).mate()
            mate_centipaws = None
            if mate_in > 0 :
                mate_centipaws = 120 - np.log2(np.abs(mate_in)**3.5)
            else:
                mate_centipaws = -120 + np.log2(np.abs(mate_in)**3.5)
                
            return mate_centipaws
        else:
            centipawns = score.score()
            return float(centipawns)