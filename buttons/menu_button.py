import pygame
import game
import time
import assets.colours as colours

from .button import Button

class MenuButton(Button):
    
    def __init__(self, interface, x=0, y=0, width=0, height=0, font=None, text=None, highlight_text=None):
        super().__init__(interface, x, y, width, height, font, text)

        self.font = pygame.font.Font(None, 30)
        self.highlight_text = highlight_text

        self.default_text_colour = self.text_colour = colours.GREY_BLACK,
        self.default_outer_rect_colour = self.outer_rect_colour = colours.BOARD
        self.default_text = self.text

    def draw(self):
        """
        This funciton daws the menu button 
            - its base rectangle
            - the inner rectangle and,
            - the text
        
        If the user hovers over the button its outer rectangle and text are both changed
        The default layout will be the board grid size, say:
        4X4
        5X5

        Upon highlighting over it we will see the grid goal. e.g. 2048/4096
        """
        self._draw_base_rectangle()

        if self.hover:
            self.outer_rect_colour = colours.YELLOW
            self.text_colour = colours.WHITE  
            self.text = self.highlight_text
            
        else:
            self.outer_rect_colour = self.default_outer_rect_colour
            self.text_colour = self.default_text_colour
            self.text = self.default_text
            self._draw_inner_rectangle()

        self._draw_text()
        self.screen.blit(self.surface, (self.rect.x , self.rect.y))      

    """The following 4 functions are self explanatory"""
    def _draw_base_rectangle(self):
        outer_rect = pygame.Rect(0, 0, self.width, self.height)
        pygame.draw.rect(self.surface, self.outer_rect_colour, outer_rect, border_radius=5)

    def _draw_inner_rectangle(self):
        inner_x = self.width * 0.1 // 2
        inner_y = self.height * 0.2 // 2
        inner_rect = pygame.Rect(inner_x, inner_y, self.width*0.9, self.height*0.8)
        pygame.draw.rect(self.surface, colours.DEFUALT_TILE, inner_rect, border_radius=5)

    def _draw_text(self):
        text = self.font.render(self.text, True, self.text_colour)
        text_x = (self.width  - text.get_width()) // 2
        text_y = (self.height - text.get_height()) // 2
        self.surface.blit(text, (text_x, text_y))
         

    def dissolve(self, start_time):
        """
        This function changes the transparency of the buttons over 1s to give the appearance of dissolving
        """
        # Calculate the time elapsed since the start of the loop
        elapsed_time = pygame.time.get_ticks() - start_time

        # Calculate the current alpha value based on elapsed time
        current_alpha = max(0, 255 - (255 * elapsed_time / 1000))

        # Set the new alpha value for the rectangle
        self.surface.set_alpha(int(current_alpha))

        if current_alpha == 0: 
            game.start_time = time.time()
            return True
        
