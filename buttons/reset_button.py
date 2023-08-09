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
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        self.hover = False
        self.select_sound = pygame.mixer.Sound("assets/sounds/click.wav")
        self.select_sound.set_volume(0.1)


    def draw(self) -> None:
        

        self._draw_rect()
        self._draw_text()

        game.screen.blit(self.surface, (self.rect.x , self.rect.y))   

    def _draw_rect(self):
        if self.hover:
            self.rect.width *= 1.05
            self.rect.height *= 1.05

         outer_rect = pygame.Rect(0, 0, self.width, self.height)
        pygame.draw.rect(self.surface, self.outer_rect_colour, outer_rect, border_radius=5)

        pygame.draw.rect(self.surface, colours.new_game, self.rect, border_radius=5)
  

    def _draw_text(self):
        text = self.font.render(self.text, True, colours.WHITE)
        text_x = (self.width  - text.get_width()) // 2
        text_y = (self.height - text.get_height()) // 2
        self.surface.blit(text, (text_x, text_y))


    def handle(self, event) -> None:
        """
        This function handles the events that pertain to the reset button.
        If the user clicks on the button we reset all necessary states and the board for a new game to be played
        """
        if event.type == pygame.MOUSEMOTION:
            self.hover = True if self.rect.collidepoint(event.pos) else False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.select_sound.play()
        

        