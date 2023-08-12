import game
import os

from random import choices
from random import randint

from pygame.locals import *
from .tile import Tile

import pygame
import assets.colours as colours
import game
import gamestate

from buttons.reset_button import ResetButton
from buttons.continue_button import ContinueButton



class Board(list):

    def __init__(self, interface, rows, columns):
        super().__init__([[None for _ in range(columns)] for _ in range(rows)])
        self.interface = interface
        self.screen = game.screen
        self.rows = rows
        self.columns = columns

        cell_width = (game.SCREEN_WIDTH * 0.75) // self.columns
        cell_height =  (game.SCREEN_HEIGHT * 0.75) // self.rows
        self.cell_width = self.cell_height = min(cell_width, cell_height) #set both the same so cell is perfect square
        self.cell_size = (self.cell_width, self.cell_height) 

        self.width  = int(self.cell_width * self.columns * 1.04)
        self.height = int(self.cell_height * self.rows * 1.04)
        
        self.x_center_offset = (game.SCREEN_WIDTH - (self.cell_height * self.columns)) / 2
        self.y_center_offset = ((game.SCREEN_HEIGHT - (self.cell_height * self.rows)) / 2) + 30

        self.rect = pygame.Rect((int(self.x_center_offset - (self.width * 0.02)), 
                                 int(self.y_center_offset - (self.width * 0.02)), 
                                self.width, self.height))


        

        self.score_width = self.box_width = self.width * 0.3
        self.score_height = self.box_height = (self.height * 0.1)

        self.score_x = self.rect.x
        self.score_y = self.rect.y - self.box_height - 5

        self.best_x = self.rect.centerx - self.box_width // 2
        self.best_y = self.score_y

        
        self.number_font = pygame.font.Font(None, 50)
        self.end_game_font = pygame.font.Font(None, 85)
        self.title_font = pygame.font.Font(None, int(self.box_width * 0.2))

        self.transparent_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        
        self.reset_button = ResetButton(self,
                                        text = "New Game", 
                                        x = (self.rect.x + self.rect.width) - self.box_width, 
                                        y = self.rect.y - self.box_height - 5)

        self.try_again_button = ResetButton(self, 
                                            "Try Again", 
                                            x =  self.rect.centerx - self.box_width // 2,
                                            y =  self.rect.centery - self.box_height // 2)
        
        self.continue_button = ContinueButton(self, 
                                            "Continue", 
                                            x =  (self.rect.centerx - self.box_width // 2 ) - (self.box_width * 0.8),
                                            y =  self.rect.centery - self.box_height // 2)

        self.sweep_sound = pygame.mixer.Sound("assets/sounds/sweep.wav")
        self.sweep_sound.set_volume(0.5)

        self.counter = 0
        self.best = 0
        self.generate()

    def generate(self):
        self.score = 0
        self.generate_tiles()
        self.generate_random_block()

    def generate_tiles(self):
        
        board = [[0,0,0,0],
         [0,8,4,2],
         [256,128, 64,32],
         [1024, 1024,512, 128]]

        for r, row in enumerate(board):
            for c, value in enumerate(row):
                x =  (c * self.cell_width) 
                x += self.x_center_offset
                
                y =  (r * self.cell_height)  
                y += self.y_center_offset
                
                tile = Tile(self, r, c, x, y, self.cell_size)    
                tile.value = value
                self[r][c] = tile 
        return

        for row in range(self.rows):
            for column in range(self.columns):
                x =  (column * self.cell_width) 
                x += self.x_center_offset
                
                y =  (row * self.cell_height)  
                y += self.y_center_offset
                
                tile = Tile(self, row, column, x, y, self.cell_size)     
                self[row][column] = tile 
         
    def generate_random_block(self):
        #10% chance for 4 spawning
        #90% chance for 2 spawning
        row, column = randint(0, self.rows - 1), randint(0, self.columns - 1)
        while self[row][column].value != 0:
            row, column = randint(0, self.rows - 1), randint(0, self.columns - 1)

        self[row][column].value = choices(population=[2, 4], weights=[0.90, 0.10])[0]

    def draw(self):

        if self.get_remaining_spaces() == 0:
            self.check_lose()
                    

        self.reset_button.draw()
        self._draw_score()
        self._draw_best()
        self._draw_base()
        self._draw_tiles()

        if gamestate.end_game:
            self._draw_end_game()

    def _draw_base(self):
        pygame.draw.rect(self.screen, colours.board, self.rect, border_radius=10)

                
    
    def _draw_tiles(self):
        for row in self:
            for tile in row:
                tile.draw()

    def _draw_score(self):
        score_text = self.number_font.render(str(self.score), True, colours.WHITE)
        score_rect = score_text.get_rect()
        score_width = score_rect.width
        score_height = score_rect.height

        if score_width > self.score_width:
            self.score_width = score_width + 30

        self.score_rect = pygame.Rect(self.score_x, self.score_y, self.score_width, self.score_height)
        
        text_x = self.score_rect.x + (self.score_rect.width - score_width) // 2
        text_y = (self.score_rect.y + (self.score_rect.height - score_height) // 2 ) + (self.score_rect.height * 0.05)

        pygame.draw.rect(game.screen, colours.default_tile, self.score_rect, border_radius=5)
        game.screen.blit(score_text, (text_x, text_y))

        
        title = self.title_font.render(str("Score"), True, colours.text)
        title_rect = title.get_rect()

        title_x = self.score_x + (self.score_width - title_rect.width) // 2
        title_y = (self.score_y + (self.score_height - title_rect.height) // 2) - 35

        game.screen.blit(title, (title_x, title_y))

    def _draw_best(self):
        self.best_score_rect = pygame.Rect(self.best_x, self.best_y, self.box_width, self.box_height)
        pygame.draw.rect(game.screen, colours.default_tile, self.best_score_rect, border_radius=5)
        
        best_text = self.number_font.render(str(self.best), True, colours.WHITE)
        best_rect = best_text.get_rect()

        text_x = self.best_x + (self.box_width - best_rect.width) // 2
        text_y = (self.best_y + (self.box_height - best_rect.height) // 2 ) + (self.box_height * 0.05)
        
        game.screen.blit(best_text, (text_x, text_y))


        title = self.title_font.render(str("Best"), True, colours.text)
        title_rect = title.get_rect()

        title_x = self.best_x + (self.box_width - title_rect.width) // 2
        title_y = (self.best_y + (self.box_height - title_rect.height) // 2) - 35

        game.screen.blit(title, (title_x, title_y))
    
    def _draw_end_game(self):

        
        pygame.draw.rect(self.transparent_surface, (237, 207, 114, 100), self.transparent_surface.get_rect())
        game.screen.blit(self.transparent_surface, self.rect)

        if gamestate.win:
            self.try_again_button.x = self.try_again_button.rect.x = (self.rect.centerx - self.box_width // 2) + (self.box_width * 0.8)
            self.continue_button.draw()
        self.try_again_button.draw()
        
    
        text = self.end_game_font.render(self.end_game_text, True, self.end_game_text_colour)
        text_x = (game.SCREEN_WIDTH  - text.get_width()) // 2
        text_y = (game.SCREEN_HEIGHT - text.get_height()) // 2 - 85
        game.screen.blit(text, (text_x, text_y))

    def print_board(self):
        import os
        clear = lambda: os.system('clear')
        clear()

        for row in self:
            print(row)



    def handle(self, event):
        self.reset_button.handle(event)
        shifts = []
        if not gamestate.end_game:
            if event.type == KEYDOWN:
                direction = pygame.key.name(event.key)
                
                if event.key in (K_UP, K_LEFT, K_w, K_a): 
                    for row in range(self.rows):
                        
                        locked_positions = set()
                        for column in range(self.columns):
                            shifts += [(self.shift(direction, row, column, locked_positions))]

               
                    if not any(i for i in shifts): return False
                    else:
                        #self.sweep_sound.play() 
                        self.generate_random_block()


                elif event.key in (K_DOWN, K_RIGHT, K_s, K_d):
                    for row in reversed(range(self.rows)):
                        
                        locked_positions = set()
                        for column in reversed(range(self.columns)):
                            shifts += [(self.shift(direction, row, column, locked_positions))]

             
                    if not any(i for i in shifts): return False
                    else:
                        #self.sweep_sound.play()
                        self.generate_random_block()

        else:
            self.try_again_button.handle(event)
            
            if gamestate.win:
                self.continue_button.handle(event)
        
        return True
    

    def get_remaining_spaces(self):
        return sum (1 for row in self for tile in row if not tile.value)

    def shift(self, direction, row, column, locked_positions):
        
        shifted = False

        if self[row][column].value != 0:

            new_position = new_row, new_column =  self.get_next_position(direction, (row, column))
            positions = [(new_row, new_column)]

            while self.in_bounds(row, column):

                if self[row][column].value == self[new_row][new_column].value:
                    if new_position in locked_positions: break
                    shifted = True

                    self.score += self[row][column].value
                    self.best = max(self.best, self.score)
                    
                    locked_positions.add((new_position))

                    self[new_row][new_column].value *= 2
                    self[row][column].value = 0
                    return shifted

                elif self[new_row][new_column].value not in (0, self[row][column].value):
                    break

                new_position = new_row, new_column = self.get_next_position(direction, (new_row, new_column))
                positions.append((new_position))

            if len(positions) >= 2:
                new_row, new_column = positions[-2]
                self[row][column].value, self[new_row][new_column].value = self[new_row][new_column].value, self[row][column].value  
                shifted = True
            return shifted
                
    def get_next_position(self, direction, current_position):
 
        row, column = current_position

        if direction in ("left", "a"):
            return (row, column - 1)
        
        elif direction in ("right", "d"):
            return (row, column + 1)
        
        elif direction in ("up", "w"):
            return (row - 1, column)
        
        elif direction in ("down", "d"):
            return (row + 1, column)
    
    def check_win(self):

        for row in self:
            for tile in row:
                if tile.value == game.goal:
                    gamestate.win = True
                    gamestate.end_game = True
                    self.end_game_text = "You Win"
                    self.end_game_text_colour = colours.WHITE
                    


                    """
                    stop all handling of keys and only allow clicking
                    
                    """

    def check_lose(self):
        if not gamestate.lose:
            for row in self:
                for tile in row:
                    directions = [self.get_next_position(direction, tile.position) for direction in ("left", "right", "up", "down")]
                    if any(1 for (row, column) in directions if self.in_bounds(row, column) and self[row][column].value == tile.value):
                        return 
                
            gamestate.lose = True
            gamestate.end_game = True
            self.end_game_text = "You Lose"
            self.end_game_text_colour = colours.text
            print("lose")
            
    def in_bounds(self, row, column):
        return (0 <= row < self.rows) and (0 <= column < self.columns)