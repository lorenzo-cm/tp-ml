import pygame
import chess.svg as csvg
import chess
import io
import cairosvg

from config import *


def convert_svg_to_png_in_memory(svg_data):
    png_data = cairosvg.svg2png(bytestring=svg_data)
    return io.BytesIO(png_data)

class Draw:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption("Chess AI")
        self.font = pygame.font.Font(None, 74)
        
        self.window_size = WINDOW_SIZE
    
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
        
    def draw_game_over(self, result_text):
        text = self.font.render(result_text, True, (255, 0, 0))
        self.screen.blit(text, (100, 400))
        
    def draw_promotion(self):
        symbols_list = ['n', 'b', 'r', 'q']
        map_symbol_to_int = [2, 3, 4, 5]
        svgs_list = [csvg.piece(chess.Piece.from_symbol(symbol.capitalize()), size=92) for symbol in symbols_list]
        SPACING = 92
        for i, svg in enumerate(svgs_list):
            x = i * SPACING + PADDING
            image = pygame.image.load(convert_svg_to_png_in_memory(svg))
            rect = image.get_rect(topleft=(x, PADDING))
            draw_rect = pygame.Rect(x, PADDING, 90, 90)
            pygame.draw.rect(self.screen, '#9dc791', draw_rect)
            self.screen.blit(image, rect)
            
        pygame.display.flip()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if y < SPACING+PADDING and y >= PADDING:
                        if not x < PADDING: 
                            index = x // SPACING
                            if index < len(symbols_list):
                                return map_symbol_to_int[index]
        return None
        
    def update(self):
        pygame.display.flip()