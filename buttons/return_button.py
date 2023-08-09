import pygame
import gamestate
from buttons.button import Button


class ReturnButton(Button):
    
    def __init__(self, interface, x=10, y=0, width=80, height=80, text=None, font=None):
        super().__init__(interface, x, y, width, height, text, font)
    
        self.interface              = interface
        self.init_menu_buttons      = interface.init_menu_buttons
        
        self.hover_image = pygame.image.load("assets/images/yellow_return_button.png")
        self.hover_image = pygame.transform.scale(self.hover_image, (80, 80))
        self.return_image = pygame.image.load("assets/images/return_button.png")
        self.return_image = pygame.transform.scale(self.return_image, (80, 80))
        self.default_image = self.image = self.return_image
    

    def draw(self):
        """
        This function simply draws the return button increased in size a tiny bit if the user hovers over the rect
        Or else just draws the default button
        """
        self.image = self.hover_image if self.hover else self.default_image 

        self.screen.blit(self.image, self.rect)


    def handle(self, event) -> None:
        """
        This function handles all events that pertain to the return button object
        
        If the user clicks the button, all necessary gamestate changes are made to return back to the menu and stop playing the game
        """
        if event.type == pygame.MOUSEMOTION:
            self.hover = True if self.rect.collidepoint(event.pos) else False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                gamestate.reset()
                self.init_menu_buttons()
                self.select_sound.play()

                
