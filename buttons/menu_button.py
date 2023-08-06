import pygame
import game
import time
import assets.colours as colours

from .button import Button

class MenuButton(Button):
    
    def __init__(self, screen, x=0, y=0, width=0, height=0, text=None, font=None):
        super().__init__(screen, x, y, width, height, text, font)
        self.font = pygame.font.Font(None, 30)
        self.default_text_colour = self.text_colour = colours.text,
        self.default_rect_colour = self.rect_colour = colours.inner_rect

    def draw(self):
        if self.hover:
            self.rect_colour = colours.yellow
            self.text_colour = colours.WHITE  
        else:
            self.rect_colour = self.default_rect_colour
            self.text_colour = self.default_text_colour

            
        self._draw_base_rectangle()
        self._draw_text()

        self.screen.blit(self.surface, (self.rect.x , self.rect.y))      

    """The following 4 functions are self explanatory"""
    def _draw_base_rectangle(self):
        rounded_rect_rect = pygame.Rect(0, 0, self.width, self.height)
        pygame.draw.rect(self.surface, self.rect_colour, rounded_rect_rect, border_radius=20)

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
        
