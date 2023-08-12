import pygame
import gamestate
from .reset_button import ResetButton

class ContinueButton(ResetButton):

    def __init__(self, board, text, x, y):
        super().__init__(board, text, x, y)
        self.hover = False

    def handle(self, event) -> None:
        """
        This function handles the events that pertain to the reset button.
        If the user clicks on the button we reset all necessary states and the board for a new game to be played
        """
        if event.type == pygame.MOUSEMOTION:
            self.hover = True if self.rect.collidepoint(event.pos) else False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                print("Continuefnc")
                gamestate.reset_endgame_states()
                self.select_sound.play()