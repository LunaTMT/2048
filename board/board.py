import game
import os

from random import choices
from random import randint

from pygame.locals import *
from .tile import Tile

import pygame
import assets.colours as colours
import game


from buttons.reset_button import ResetButton



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

        self.score_width = self.width * 0.3    
        self.score_height = self.height * 0.1
        self.score_rect_x = self.rect.x
        self.score_rect_y = self.rect.y - self.score_height - 5

        self.font = pygame.font.Font(None, 50)

        self.reset_button = ResetButton(self)
        self.best = 0
        self.generate()

    def generate(self):
        self.score = 0
        self.generate_tiles()
        self.generate_random_block()

    def generate_tiles(self):
    
        for row in range(self.rows):
            for column in range(self.columns):
                x =  (column * self.cell_width) 
                x += self.x_center_offset
                
                y =  (row * self.cell_height)  
                y += self.y_center_offset
                
                tile = Tile(self.screen, row, column, x, y, self.cell_size)     
                self[row][column] = tile 
         
    def generate_random_block(self):
        #10% chance for 4 spawning
        #90% chance for 2 spawning
        row, column = randint(0, self.rows - 1), randint(0, self.columns - 1)
        while self[row][column].value != 0:
            row, column = randint(0, self.rows - 1), randint(0, self.columns - 1)
        
        self[row][column].value = choices(population=[2, 4], weights=[0.90, 0.10])[0]

    def draw(self):
        self.reset_button.draw()
        self._draw_score()
        self._draw_best()

        pygame.draw.rect(self.screen, colours.board, self.rect, border_radius=10)
        for row in self:
            print(row)
            for tile in row:
                tile.draw()
        
        

    def _draw_score(self):
    

        text_surface = self.font.render(str(self.score), True, colours.WHITE)
        text_rect = text_surface.get_rect()
        text_width = text_rect.width
        text_height = text_rect.height

        if text_width > self.score_width:
            self.score_width = text_width + 30

        self.score_rect = pygame.Rect(self.score_rect_x, self.score_rect_y, self.score_width, self.score_height)
        
        text_x = self.score_rect.x + (self.score_rect.width - text_width) // 2
        text_y = (self.score_rect.y + (self.score_rect.height - text_height) // 2 ) + (self.score_rect.height * 0.05)

        

        pygame.draw.rect(game.screen, colours.default_tile, self.score_rect, border_radius=5)
        game.screen.blit(text_surface, (text_x, text_y))

    def _draw_best(self):
        pass

    

    def handle(self, event):

        self.reset_button.handle(event)

        if event.type == KEYDOWN:
            direction = pygame.key.name(event.key)
            print(direction)
            if event.key in (K_UP, K_LEFT, K_w, K_a): 
                for row in range(self.rows):
                    locked_positions = set()
                    for column in range(self.columns):
                        self.shift(direction, row, column, locked_positions)
                self.generate_random_block()

            elif event.key in (K_DOWN, K_RIGHT, K_s, K_d):
                for row in reversed(range(self.rows)):
                    locked_positions = set()
                    for column in reversed(range(self.columns)):
                        self.shift(direction, row, column, locked_positions)
                self.generate_random_block()
            
    def shift(self, direction, row, column, locked_positions):
        
    
        if self[row][column] != 0:
        
            new_position = new_row, new_column =  self.get_next_position(direction, (row, column))
            positions = [(new_row, new_column)]

            while (0 <= new_row < self.rows) and (0 <= new_column < self.columns):

                if self[row][column].value == self[new_row][new_column].value:
                    if new_position in locked_positions: break

                    self.score += self[row][column].value
                    locked_positions.add((new_position))

                    new_tile = self[new_row][new_column]
                    self[row][column].slide = True
                    self[row][column].target = self[new_row][new_column].coord
                    print((new_tile.x, new_tile.y))

                    self[new_row][new_column].value *= 2
                    self[row][column].value = 0
                    return

                elif self[new_row][new_column].value not in (0, self[row][column].value):
                    break

                new_position = new_row, new_column = self.get_next_position(direction, (new_row, new_column))
                positions.append((new_position))

            if len(positions) >= 2:
                new_row, new_column = positions[-2]
                self[row][column].value, self[new_row][new_column].value = self[new_row][new_column].value, self[row][column].value  
                

                self[row][column].slide = True
                self[row][column].target = self[new_row][new_column].coord
                

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
