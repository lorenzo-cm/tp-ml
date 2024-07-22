import time
import pygame
import chess
import threading
from pygame_functions.draw import Draw
from engine.minimax import get_best_move
from engine.zobrist import ZobristHasher, ZobristHasherPoly
from utils import *

draw = Draw()

class BestMoveThread(threading.Thread):
    def __init__(self, board, depth, zobrist, transposition_table, iterative_deepening=True, verbose=False):
        threading.Thread.__init__(self)
        self.board = board
        self.depth = depth
        self.zobrist = zobrist
        self.transposition_table = transposition_table
        self.verbose = verbose
        self.iterative_deepening = iterative_deepening
        
        self.best_move = None
        self.position_value = None

    def run(self):
        self.best_move, self.position_value, self.transposition_table = get_best_move(
            self.board,
            self.depth,
            self.zobrist,
            self.transposition_table,
            iterative_deepening=self.iterative_deepening,
            verbose=self.verbose)

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
    board.set_fen('r2q1rk1/ppp2ppp/4b3/4B3/2B4P/1P6/n1PPQPP1/1K2R2R b - - 1 17')
    # board.set_fen('8/8/8/8/3k4/8/3q4/K7 w - - 0 1') # easy final
    board.fullmove_number = 17
    
    INITIAL_MOVES = False
    
    prev_selected_square = None
    selected_square = None

    best_move_thread = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                
                if board.turn:
                    list_moves, selected_square = handle_click(board, *event.pos)
                    
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
                
                prev_selected_square = selected_square

        if not game_over:
            game_over, result_text = check_game_over(board)

        if not board.turn and not game_over:
            if board.fullmove_number < 3 and INITIAL_MOVES:
                move = opening_move(board.fullmove_number)
                if board.is_legal(move):
                    board.push(move)
            else:
                if best_move_thread is None:
                    init_time = time.perf_counter()
                    best_move_thread = BestMoveThread(board.copy(), BOT_DEPTH, zobrist, transposition_table, verbose=True)
                    best_move_thread.start()
                elif not best_move_thread.is_alive():
                    print(f'Time taken: {time.perf_counter() - init_time} s')
                    move = best_move_thread.best_move
                    position_value = best_move_thread.position_value
                    transposition_table = best_move_thread.transposition_table
                    if move:
                        board.push(move)
                        transposition_table.clear()
                    print(f"Evaluation: {position_value}")
                    best_move_thread = None

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
    torch.cuda.init()
    
    main()
