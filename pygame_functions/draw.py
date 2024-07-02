import pygame
import chess.svg as csvg
import chess

import io
import cairosvg

def convert_svg_to_png_in_memory(svg_data):
    png_data = cairosvg.svg2png(bytestring=svg_data)
    return io.BytesIO(png_data)

class Draw:
    def __init__(self, screen, window_size) -> None:
        self.screen = screen
        self.window_size = window_size
    
    def all(self, board, list_moves):
        self.draw_board(board, list_moves)
        self.update()

    def draw_board(self, board, list_moves):
        if list_moves:
            svg_board = csvg.board(board,
                                fill=dict.fromkeys(list_moves, "#ff8fa0"),
                                size=self.window_size)
        else:
            svg_board = csvg.board(board,
                                size=self.window_size)
        
        image = pygame.image.load(convert_svg_to_png_in_memory(svg_board))
        self.screen.blit(image, (0,0))
        
    def update(self):
        pygame.display.flip()