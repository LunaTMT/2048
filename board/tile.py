import pygame
import game
import assets.colours as colours

class Tile:
    
    def __init__(self, screen, row, column,  x, y, cell_size):
        #self.board = board
        self.screen = screen
        self.row = row
        self.column = column
        self.position = (self.row, self.column)
        self.x = x
        self.y = y
        self.width, self.height  = cell_size

        self.value = 2

    def draw(self):
        
        #inner_rect = pygame.Rect((WIDTH - INNER_RECT_SIZE) // 2, (HEIGHT - INNER_RECT_SIZE) // 2, INNER_RECT_SIZE, INNER_RECT_SIZE)

        """Draw one large rectangle for the outter rectangle of the tile, its pointless having it here plus round its edges as in actual game"""
        outer_rect = pygame.Rect((self.x, self.y, self.width, self.height))
        pygame.draw.rect(self.screen, colours.outer_rect, outer_rect)

        
        inner_width = inner_height = self.width * 0.90
        inner_x = self.x + (self.width - inner_width) // 2
        inner_y = self.y + (self.height - inner_height) // 2

        inner_rect = pygame.Rect((inner_x, inner_y, inner_width, inner_height))
        pygame.draw.rect(self.screen, colours.inner_rect, inner_rect, border_radius=5)

        if self.value:
            
            if self.value >= 8:
                colour = colours.WHITE
            else:
                colour = colours.text
        
            font = pygame.font.Font(None, int(self.width * 0.7))
            text_surface = font.render(str(self.value), True, colour)

            text_x = self.x + (self.width - text_surface.get_width()) // 2
            text_y = (self.y + (self.height - text_surface.get_height()) // 2 ) + self.height * 0.05

        
            self.screen.blit(text_surface, (text_x, text_y))

        
    def __repr__(self) -> str:
        return str(self.value)
    
    def __str__(self) -> str:
        return str(self.value)