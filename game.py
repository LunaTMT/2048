import pygame
import sys
import gamestate

import assets.colours as colour

from board.board import Board
from buttons.menu_button import MenuButton
from buttons.return_button import ReturnButton

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
goal = 0

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2048")
clock = pygame.time.Clock()


class Game:
    def __init__(self):
        self.running = True
        self.buttons = []
        self.init_menu_buttons()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            #Handling Menu buttons
            if gamestate.handle_menu_buttons:
                for button in self.buttons:
                    grid = selected = button.handle_event(event)
                    #Until a button has been selected continue to handle the menu buttons
                    if selected:
                        """
                        Once selected we change the pygame display name
                        Change the game state such that we stop handling the buttons and begin dissolving them
                        The board object is then created based upon the grid size associated with the button
                        The return button is also created to return back to the menu when a game is started
                        """
                        pygame.display.set_caption(button.highlight_text)
                        global goal 
                        goal = button.highlight_text

                        gamestate.handle_menu_buttons = False
                        gamestate.dissolve_buttons = True
                        self.start_time = pygame.time.get_ticks()
                        
                        rows = columns = int(grid[0:2])
                        self.board = Board(self, rows, columns)
                        self.return_button = ReturnButton(self)

            #Upon playing the game we want to handle the board for game interaction and the return button
            if gamestate.play_game                                                                                                          :
                self.board.handle(event)
                self.return_button.handle(event)

    def draw(self):
        screen.fill(colour.BACKGROUND)

        #If our current game state is to show the menu we will draw its associated buttons
        if gamestate.show_menu:
            for button in self.buttons:
                button.draw()

                #If we need to dissolve the buttons initiate the dissolve draw function and delete the button objects
                if gamestate.dissolve_buttons:
                    has_dissolved = button.dissolve(self.start_time)  
 
                    if has_dissolved:
                        self.buttons = []
                        gamestate.initiate_game() #gamestate change to play game
                        break
        
        #If we're going to play the game then simply draw the board and the return button
        if gamestate.play_game:
            self.board.draw()
            self.return_button.draw()
        
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.draw()
            clock.tick(FPS)
        pygame.quit()
        sys.exit()
    
    def init_menu_buttons(self):
        """
        This function creates the menu buttons in the center with equal gaps between each button
        """
        grid_goal = ('2048', '4096', '8192', '16384', '32768', '65536', '131072')

        for i, (grid, goal) in enumerate(zip(range(4, 11), grid_goal)):
            button = MenuButton(self, y=(i*80) + 30 , width=200, height=60, text=f"{grid} X {grid}", highlight_text=goal)
            button.center_x()
            self.buttons.append(button)

