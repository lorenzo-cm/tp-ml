from concurrent.futures import ProcessPoolExecutor
import pygame
import chess
from pygame_functions.draw import Draw
from engine.minimax import get_best_move
from engine.zobrist import ZobristHasher, ZobristHasherPoly
from utils import *

draw = Draw()

def main():
    BOT_DEPTH = 5
    
    running = True
    game_over = False
    result_text = ''
    
    zobrist = ZobristHasherPoly()
    # zobrist = ZobristHasher()
    transposition_table = {}
    
    position_value = 0
    
    list_moves = []
    
    board = chess.Board()
    # board.set_fen('8/2K5/4k3/3r3b/8/8/8/8 b - - 0 1')
    # board.set_fen('8/8/8/8/3k4/8/3q4/K7 w - - 0 1') # easy final
    # board.fullmove_number = 3
    
    INITIAL_MOVES = True
    
    prev_selected_square = None
    selected_square = None
    
    with ProcessPoolExecutor() as executor:
        future = None

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                    
                    if board.turn:
                        list_moves, selected_square = handle_click(board, *event.pos)
                        
                        # print(prev_selected_square, selected_square)
                        
                        if prev_selected_square is not None and selected_square is not None:
                            
                            if board.piece_at(prev_selected_square):

                                move = chess.Move(prev_selected_square, selected_square)
                                move_promo = chess.Move(move.from_square, move.to_square, promotion=chess.QUEEN)
                                
                                if board.is_legal(move_promo):
                                    piece = draw.draw_promotion()
                                    move = chess.Move(move.from_square, move.to_square, promotion=piece)

                                if board.is_legal(move):
                                    if move:
                                        board.push(move)
                                    # else:
                                    #     print(f'move wrong: {move}')
                                    # print('number moves: ', board.fullmove_number)
                    
                    # print(f'prev square: {prev_selected_square},  selected: {selected_square}')
                    prev_selected_square = selected_square
                    # print(f'prev square: {prev_selected_square},  selected: {selected_square}')
                    

            if not game_over:
                game_over, result_text = check_game_over(board)


            if not board.turn and not game_over:
                if board.fullmove_number < 3 and INITIAL_MOVES:
                    move = opening_move(board.fullmove_number)
                    if board.is_legal(move):
                        board.push(move)
                    
                else:
                    if future is None:
                        future = executor.submit(get_best_move, board.copy(), BOT_DEPTH, zobrist, transposition_table, verbose=False)
                        
                    elif future.done():
                        move, position_value, transposition_table = future.result()
                        if move:
                            board.push(move)
                            # transposition_table.clear()
                        print(f"Evaluation: {position_value}")
                        future = None

            draw.all(board, list_moves)

            if game_over:
                draw.draw_game_over(result_text)
                pygame.display.flip()
            else:
                pygame.time.Clock().tick(60)
                
            pygame.display.flip()
            
    pygame.quit()
    
if __name__ == "__main__":
    import torch

    # Initialize CUDA in the main process
    # torch.cuda.init()
    
    import multiprocessing as mp

    mp.set_start_method('fork')


    main()
