import pygame
import game
import assets.colours as colours

class Tile:
    
    def __init__(self, board, row, column,  x, y, cell_size):
        self.board = board
        self.row = row
        self.column = column
        
        self.x = x 
        self.y = y 
        
        self.width, self.height = cell_size
        self.inner_width = self.inner_height = self.width * 0.90

        self.x += (self.width - self.inner_width) // 2
        self.y += (self.height - self.inner_height) // 2
        self.initial_x, self.initial_y = self.inital_position = (self.x, self.y)

        self.value = 0
        self.colour = colours.default_tile


        
    def draw(self):
        self.rect_colour = colours.get_number_colour(self.value)

        tile = pygame.Rect((self.x, self.y, self.inner_width, self.inner_height))
        pygame.draw.rect(game.screen, self.rect_colour, tile, border_radius=3)

        if self.value:
            if self.value >= 8:
                colour = colours.WHITE
            else:
                colour = colours.text
        
            font = pygame.font.Font(None, int(self.width * 0.7))
            text_surface = font.render(str(self.value), True, colour)

            text_x = self.x + (self.inner_width - text_surface.get_width()) // 2
            text_y = self.y + (self.inner_height - text_surface.get_height()) // 2  + (self.height * 0.05)
            
            game.screen.blit(text_surface, (text_x, text_y))

        
    def __repr__(self) -> str:
        return str(self.value)
    
    def __str__(self) -> str:
        return str(self.value)