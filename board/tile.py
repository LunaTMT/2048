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
        self.colour = colours.DEFUALT_TILE
        self.font = pygame.font.Font(None, int(self.width * 0.7))
        self.tile_rect = pygame.Rect((self.x, self.y, self.inner_width, self.inner_height))

        
    def draw(self):
        """
        This function draws the tile based upon its value
        """
        #Getting the rectangle colour based on currnent value
        self.rect_colour = self.get_rect_colour()
        
        #Draw base tile rec
        pygame.draw.rect(game.screen, self.rect_colour, self.tile_rect, border_radius=3)

        #If the tile actually has a value, i.e. != 0
        if self.value:

            if self.value >= 8:
                self.text_colour = colours.WHITE 
            else:
                self.text_colour = colours.GREY_BLACK


            """
            When the value of the tile starts to become very large we adjust the size of the text
            based upon the inner rectangle size such that the text will always fit onto the tile
            """
            if self.value >= 1000:
                text_surface = self.fit_text_in_rect()
            else:
                text_surface = self.font.render(str(self.value), True, self.text_colour)

            #Centering x and y
            text_x = self.x + (self.inner_width - text_surface.get_width()) // 2
            text_y = self.y + (self.inner_height - text_surface.get_height()) // 2  + (self.height * 0.05)
            
            #Blit screen onto text surface
            game.screen.blit(text_surface, (text_x, text_y))


    def fit_text_in_rect(self):
        """
        This function finds the most appropriate size for the text such that it will fit into the rect
        """
        font = self.font
        default_font_size = int(self.width * 0.7)

        for font_size in range(default_font_size, 0, -1):
            font = pygame.font.Font(None, font_size)
            text_surface = font.render(str(self.value), True, self.text_colour)
            text_rect = text_surface.get_rect()
            if (text_rect.width <= self.tile_rect.width - 10) and (text_rect.height <= self.tile_rect.height):
                return text_surface
        return None
    
    def get_rect_colour(self):
        """
        This function provides the correct colour for the given tile number value
        """
        match self.value:
            case 0:
                return colours.DEFUALT_TILE
            case 2:
                return colours.TWO
            case 4:
                return colours.FOUR
            case 8:
                return colours.EIGHT
            case 16:
                return colours.SIXTEEN
            case 32:
                return colours.THIRTY_TWO
            case 64:
                return colours.SIXTY_FOUR
            case _:
                pass
            
        if 128 <= self.value <= 2048:
            return colours.YELLOW
        else:
            return colours.BLACKISH