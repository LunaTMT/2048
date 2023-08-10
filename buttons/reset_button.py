import pygame
import game
import time

from board.tile import Tile
from .button import Button
import assets.colours as colours

class ResetButton():

    def __init__(self, board):
        self.text = "New Game"
        self.board = board

        self.width = board.width * 0.3        
        self.height = board.height * 0.1
        self.x = (board.rect.x + board.rect.width) - self.width
        self.y = board.rect.y - self.height - 5
  
        self.font = pygame.font.Font(None, int(self.width * 0.2))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.default_rect_colour = self.rect_colour = colours.new_game

        self.hover = False
        self.altered = False
        self.select_sound = pygame.mixer.Sound("assets/sounds/click.wav")
        self.select_sound.set_volume(0.1)


    def draw(self) -> None:
        self._draw_rect()
        self._draw_text()
       


    def _draw_rect(self):
        if self.hover:
            self.rect_colour = colours.yellow
        else:
            self.rect_colour = self.default_rect_colour
        
        
        pygame.draw.rect(game.screen, self.rect_colour, self.rect, border_radius=5)



    def _draw_text(self):
        text = self.font.render(self.text, True, colours.WHITE)
        text_x = self.x + (self.width - text.get_width()) // 2
        text_y = self.y + (self.height - text.get_height()) // 2
        game.screen.blit(text, (text_x, text_y))


    def handle(self, event) -> None:
        """
        This function handles the events that pertain to the reset button.
        If the user clicks on the button we reset all necessary states and the board for a new game to be played
        """
        if event.type == pygame.MOUSEMOTION:
            self.hover = True if self.rect.collidepoint(event.pos) else False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.board.generate()
                self.select_sound.play()
        

        