from concurrent.futures import ProcessPoolExecutor
import pygame
import chess
from pygame_functions.draw import Draw
from engine.minimax import get_best_move
from engine.zobrist import initialize_zobrist, compute_zobrist_hash
from utils import *

draw = Draw()

def main():
    running = True
    game_over = False
    result_text = ''
    
    zobrist_table = initialize_zobrist()
    transposition_table = {}
    
    list_moves = []
    prev_selected_square = None
    
    board = chess.Board()
    # board.set_fen('4k3/8/2pr1p1p/1p4p1/3PK3/1NP2NP1/8/8 w - - 0 1')
    board.set_fen('4k3/8/7p/3r1NpK/6P1/8/8/8 w - - 0 1')
    
    with ProcessPoolExecutor() as executor:
        future = None

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                    if board.turn:
                        list_moves, selected_square = handle_click(board, *event.pos)
                        if prev_selected_square is not None and selected_square is not None:
                            move = chess.Move(prev_selected_square, selected_square)
                            move_promo = chess.Move(move.from_square, move.to_square, promotion=chess.QUEEN)
                            
                            if board.is_legal(move_promo):
                                piece = draw.draw_promotion()
                                move = chess.Move(move.from_square, move.to_square, promotion=piece)
                                
                            if board.is_legal(move):
                                board.push(move)
                                
                        prev_selected_square = selected_square

            if not game_over:
                game_over, result_text = check_game_over(board)

            if not board.turn and not game_over:
                if future is None:
                    future = executor.submit(get_best_move, board, 4, zobrist_table, transposition_table)
                elif future.done():
                    move, transposition_table2 = future.result()
                    board.push(move)
                    future = None
                    transposition_table = transposition_table2

            draw.all(board, list_moves)

            if game_over:
                draw.draw_game_over(result_text)
                pygame.display.flip()
            else:
                pygame.time.Clock().tick(60)
                
            pygame.display.flip()
            
    pygame.quit()
    
if __name__ == "__main__":
    main()
