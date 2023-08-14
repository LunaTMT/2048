import pygame
import game
import assets.colours as colours

class Tile:
    
    def __init__(self, board, row, column,  x, y, cell_size):
        self.board = board
        self.row = row
        self.column = column
        self.position = (row, column)

        self.x = x 
        self.y = y 
        
        self.width, self.height = cell_size
        self.inner_width = self.inner_height = self.width * 0.90

        self.x += (self.width - self.inner_width) // 2
        self.y += (self.height - self.inner_height) // 2
        self.initial_x, self.initial_y = self.inital_position = (self.x, self.y)

        self.value = 0
        self.colour = colours.default_tile
        self.font = pygame.font.Font(None, int(self.width * 0.7))
        self.tile_rect = pygame.Rect((self.x, self.y, self.inner_width, self.inner_height))

        
    def draw(self):
        self.rect_colour = colours.get_number_colour(self.value)

        pygame.draw.rect(game.screen, self.rect_colour, self.tile_rect, border_radius=3)

        if self.value:
            if self.value >= 8:
                self.text_colour = colours.WHITE
            else:
                self.text_colour = colours.text

            

            if self.value >= 1000:
                text_surface = self.fit_text_in_rect()
            else:
                text_surface = self.font.render(str(self.value), True, self.text_colour)

            text_x = self.x + (self.inner_width - text_surface.get_width()) // 2
            text_y = self.y + (self.inner_height - text_surface.get_height()) // 2  + (self.height * 0.05)
            
            game.screen.blit(text_surface, (text_x, text_y))


    def fit_text_in_rect(self):
        font = self.font
        default_font_size = int(self.width * 0.7)

        for font_size in range(default_font_size, 0, -1):
            font = pygame.font.Font(None, font_size)
            text_surface = font.render(str(self.value), True, self.text_colour)
            text_rect = text_surface.get_rect()
            if (text_rect.width <= self.tile_rect.width - 10) and (text_rect.height <= self.tile_rect.height):
                return text_surface
        return None


    def __repr__(self) -> str:
        return str(self.value)
    
    def __str__(self) -> str:
        return str(self.value)