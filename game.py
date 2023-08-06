
import pygame
import sys
import assets.colours as colour
import gamestate

from buttons.menu_button import MenuButton

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

GRID_GOAL = {4  : '2048',
             5  : '4096',
             6  : '8192',
             7  : '16384',
             8  : '32768',
             9  : '65536',
             10 : '131072'}

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

            if gamestate.handle_menu_buttons:
                for button in self.buttons:
                    selected = button.handle_event(event)

                    if selected:
                        pygame.display.set_caption(button.highlight_text)
                        gamestate.handle_menu_buttons = False
                        gamestate.dissolve_buttons = True
                        self.start_time = pygame.time.get_ticks()



    def update(self):
        pass

    def draw(self):
        screen.fill(colour.BACKGROUND)

        if gamestate.show_menu:
            for button in self.buttons:
                button.draw()

                if gamestate.dissolve_buttons:
                    has_dissolved = button.dissolve(self.start_time)  
 
                    if has_dissolved:
                        self.buttons = []
                        gamestate.show_menu = False
                        gamestate.dissolve_buttons = False
                        gamestate.play_game = True
                        break

        if gamestate.play_game:
            print("playing")

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            clock.tick(FPS)

        pygame.quit()
        sys.exit()
    
    def init_menu_buttons(self):
        for i, grid in enumerate(range(4, 11), start=0):
            button = MenuButton(screen, y=(i*80) + 30 , width=200, height=60, text=f"{grid} X {grid}", highlight_text=GRID_GOAL[grid])
            button.center_x()
            self.buttons.append(button)

