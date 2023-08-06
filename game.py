
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

"""
2048	4X4
4096	5X5
8192	6X6
16384	7X7
32768	8X8
65536 	9X9
131072	10X10
"""

MAX_TILES = {4  : 2048,
             5  : 4096,
             6  : 8192,
             7  : 16384,
             8  : 32768,
             9  : 65536,
             10 : 131072}

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

            if gamestate.show_menu:
                for button in self.buttons:
                    button.handle_event(event)


    def update(self):
        pass

    def draw(self):
        screen.fill(colour.BACKGROUND)

        if gamestate.show_menu:
            for button in self.buttons:
                button.draw()

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
            button = MenuButton(screen, y=(i*80) + 30 , width=200, height=60, text=f"{grid} X {grid}")
            button.center_x()
            self.buttons.append(button)

