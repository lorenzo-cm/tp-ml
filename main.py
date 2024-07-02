import pygame
import chess

from pygame_functions.draw import Draw
from engine.minmax import get_best_move

from config import *
from utils import *

pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Chess AI")
font = pygame.font.Font(None, 74)

draw = Draw(screen, WINDOW_SIZE)

def main():
    running = True
    board = chess.Board()
    game_over = False
    text_resutl = ''
    
    list_moves = []
    prev_selected_square = None
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                
                if board.turn:
                    list_moves, selected_square = handle_click(board, *event.pos)
                    
                    if prev_selected_square is not None:
                        move = chess.Move(prev_selected_square, selected_square)
                        if board.is_legal(move):
                            board.push(move)
                        
                    prev_selected_square = selected_square
        
        
        if not game_over:
            if board.is_checkmate():
                game_over = True
                result_text = "White wins by checkmate!" if board.turn else "Black wins by checkmate!"
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
            
        
        if not board.turn and not game_over:            
            move = get_best_move(board, depth=10, time_limit=1)
            board.push(move)
             
        draw.all(board, list_moves)
        
        if game_over:
            text = font.render(result_text, True, (255, 0, 0))
            screen.blit(text, (100, 400))
            pygame.display.flip()
            
    pygame.quit()
    
    
if __name__ == "__main__":
    main()
