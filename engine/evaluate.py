import chess
import chess.pgn
import numpy as np

from .utils_engine import *
from .nn_eval import model_eval


def evaluate_board(board: chess.Board, model):    
    
    initial_turn = board.turn
    
    if board.is_checkmate():
        return -np.inf if board.turn else np.inf
    
    if board.is_stalemate():
        return 0
    
    # MOBILITY SCORE
    board.turn = chess.WHITE
    mobility_w = len(list(board.legal_moves))
    
    board.turn = chess.BLACK
    mobility_b = len(list(board.legal_moves))
    
    board.turn = initial_turn
    
    mobility_score = weights['mobility'] * (mobility_w - mobility_b)
    
    
    #  MATERIAL SCORE AND SQUARES ATTACKED SCORE
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
    
    # ENDGAME SCORE
    endgame_score = 0
    if board.fullmove_number >= 30:
        endgame_score = endgame_score_bonus(board) * weights['endgame']
    
    # PASSED PAWN SCORE
    pawn_score = 0
    if board.fullmove_number >= 0:
        pawn_score = passed_pawn_score(board) * weights['passed_pawn']

    # NN MODEL SCORE
    model_score = model_eval(model, board) * weights['nn_model']
    
    # CAN BE CAPTURED SCORE
    can_be_captured_score = can_be_captured_score_func(board) * weights['can_be_captured']
    
    print('Material ', material_score)
    print('Attack squares ', count_attack_squares_score)
    print('Mobility ', mobility_score)
    print('Endgame score: ', endgame_score)
    print('Pawn score: ', pawn_score)
    print('Model score: ', model_score)
    print('Can be captured: ', can_be_captured_score)
    
    score = material_score + count_attack_squares_score + mobility_score + endgame_score + pawn_score + model_score + can_be_captured_score

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
    'endgame': 2,
    'passed_pawn':0.3,
    'nn_model': 0.45,
    'can_be_captured': 0.09,
}


def endgame_score_bonus(board: chess.Board):
    """Calculates the king danger and then converts to score
    
    King danger is calculated by the distance of the weighted pieces to the king
    
    Then the score is generated calculating the difference between the
    white king and black king danger and scaled for a factor weight
    """
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
                
    return score
    
    
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


def can_be_captured_score_func(board):
    """Creates a score based on the pieces attacked
    
    It computes a danger score for each player, which is basically
    the weighted product of:
    - piece weight
    - number of attackers
    - boolean if the piece is attacked
    
    # Main idea: Prevent blunders
    """
    initial_turn = board.turn
    
    ally_pieces_count = 0
    # enemy_pieces_count = 0
    
    ally_danger = 0
    enemy_danger = 0
    
    # verify_dict = {}
    for square, piece in board.piece_map().items():
        
        if piece.piece_type == chess.KING:
            continue
        
        if board.is_attacked_by(not piece.color, square):
            
            attackers = board.attackers(not piece.color, square)
            num_attackers = len(attackers)
            
            if piece.color == initial_turn:
                ally_pieces_count += 1
                ally_danger += (weights[piece.piece_type]**1.5) * num_attackers
                # verify_dict[f'{square}-{piece}-{piece.color}-{piece.piece_type}'] = (weights[piece.piece_type]**1.5) * num_attackers

            # else:
                # enemy_pieces_count += 1
                # enemy_danger += (weights[piece.piece_type]**1.5) * num_attackers
                # verify_dict[f'{square}-{piece}-{piece.color}-{piece.piece_type}'] = (weights[piece.piece_type]**1.5) * num_attackers
    

    ally_danger /= ally_pieces_count + 0.00031247533457532
    # enemy_danger /= enemy_pieces_count + 0.00031247533457532
    
    score = 0
    
    if initial_turn:
        score = (ally_danger - enemy_danger)
        
    else:
        score = -(ally_danger - enemy_danger)
    
    # print(verify_dict)
    return score


# def king_winning_goes_to_combat(board: chess.Board, current_score, weight=1.5, threshold=15):
#     """
#     Evaluate the board giving a higher score if the king moves towards the other king,
#     but only if one side is significantly winning.
#     """
#     initial_turn = board.turn

#     # Check if one side is significantly winning
#     if abs(current_score) < threshold:
#         return 0

#     piece2square = piece2squareDICT(board)
    
#     ally_king_square = piece2square[chess.Piece(chess.KING, initial_turn)][0]
#     enemy_king_square = piece2square[chess.Piece(chess.KING, not initial_turn)][0]
    
#     # Calculate the distance between the two kings
#     king_distance = chess.square_distance(ally_king_square, enemy_king_square)
    
#     # Reward closer distances
#     score = (8 - king_distance) * weight
    
#     # If the current side is losing, negate the score
#     if (score < 0 and initial_turn) or (score > 0 and not initial_turn):
#         score = -score

#     return score