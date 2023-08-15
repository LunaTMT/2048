import game
import os

from random import choices
from random import randint

from pygame.locals import *
from .tile import Tile
from buttons.reset_button import ResetButton
from buttons.continue_button import ContinueButton

import pygame
import assets.colours as colours
import assets.sounds as sound
import game
import gamestate

class Board(list):

    def __init__(self, interface, rows, columns):
        super().__init__([[None for _ in range(columns)] for _ in range(rows)])
        self.interface = interface
        self.screen = game.screen
        self.rows = rows
        self.columns = columns

        self.score = 0
        self.counter = 0
        self.best = 0

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

        self.box_width = self.width * 0.3
        self.box_height = (self.height * 0.1)

        self.number_font = pygame.font.Font(None, 50)
        self.end_game_font = pygame.font.Font(None, 85)
        self.title_font = pygame.font.Font(None, int(self.box_width * 0.2))

        self.score_width = self.box_width 
        self.score_height = self.box_height 
        self.score_x = self.rect.x
        self.score_y = self.rect.y - self.box_height - 5

        self.best_x = self.rect.centerx - self.box_width // 2
        self.best_y = self.score_y

    
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

        self.valid_inputs = (K_UP, K_DOWN, K_LEFT, K_RIGHT, K_w, K_s, K_a, K_d)
        self.generate()

    def generate(self):
        """
        This function generate the initial prerequisites for the board.
        - The tiles and a random block must be placed on the board
        """
        #self.score = 0
        self.generate_tiles()
        self.generate_random_block()

    def generate_tiles(self):
        """
        This function will generate X tiles for the board
        where X = row * column
        Each tile is placed accordingly to give the appearance of a KxK board
        """
        for row in range(self.rows):
            for column in range(self.columns):
                x =  (column * self.cell_width) 
                x += self.x_center_offset
                
                y =  (row * self.cell_height)  
                y += self.y_center_offset
                
                tile = Tile(self, row, column, x, y, self.cell_size)     
                self[row][column] = tile 
         
    def generate_random_block(self):
        """
        This function will first find a tile on the board that is empty
        It will generate a random number 2 or 4 with (90/10)%.
        It will assign the tile this value
        """
        row, column = randint(0, self.rows - 1), randint(0, self.columns - 1)
        while self[row][column].value != 0:
            row, column = randint(0, self.rows - 1), randint(0, self.columns - 1)

        self[row][column].value = choices(population=[2, 4], weights=[0.90, 0.10])[0]



    def draw(self):
        """
        This function draws all the components parts of the board
        If the game has reached an end state (win or lose) the correct endstate will be shown on top of the board
        """
        self.reset_button.draw()
        self._draw_score()
        self._draw_best()
        self._draw_base()
        self._draw_tiles()

        if gamestate.end_game:
            self._draw_end_game()

    def _draw_base(self):
        """
        This funciton simple draws the base rectangle of the board
        """
        pygame.draw.rect(self.screen, colours.BOARD, self.rect, border_radius=10)
 
    def _draw_tiles(self):
        """
        This function draws every tile for each tile that exists on the board
        """
        for row in self:
            for tile in row:
                tile.draw()

    def _draw_score(self):
        """
        This function will draw the score the player currently has in the game 
        It also adjusts the rect size if the score is going to go over the boundaries of the rectangle that it is contained within
        """
        score_text = self.number_font.render(str(self.score), True, colours.WHITE)
        score_rect = score_text.get_rect()
        score_width = score_rect.width
        score_height = score_rect.height

        if score_width > self.score_width:
            self.score_width = score_width + 30

        #Drawing base rectangle with altered size
        self.score_rect = pygame.Rect(self.score_x, self.score_y, self.score_width, self.score_height)
        pygame.draw.rect(game.screen, colours.DEFUALT_TILE, self.score_rect, border_radius=5)

        #Drawing text
        text_x = self.score_rect.x + (self.score_rect.width - score_width) // 2
        text_y = (self.score_rect.y + (self.score_rect.height - score_height) // 2 ) + (self.score_rect.height * 0.05)
        game.screen.blit(score_text, (text_x, text_y))
        
        #Draw "Score" Title above the box
        title = self.title_font.render(str("Score"), True, colours.GREY_BLACK)
        title_rect = title.get_rect()
        title_x = self.score_x + (self.score_width - title_rect.width) // 2
        title_y = (self.score_y + (self.score_height - title_rect.height) // 2) - 35
        game.screen.blit(title, (title_x, title_y))

    def _draw_best(self):
        """
        This funciton will draw the best score the player has achieved for that give board grid
        """
        #Base rectangle
        self.best_score_rect = pygame.Rect(self.best_x, self.best_y, self.box_width, self.box_height)
        pygame.draw.rect(game.screen, colours.DEFUALT_TILE, self.best_score_rect, border_radius=5)
        
        #The best score
        best_text = self.number_font.render(str(self.best), True, colours.WHITE)
        best_rect = best_text.get_rect()
        best_rect_text_x = self.best_x + (self.box_width - best_rect.width) // 2
        best_rect_text_y = (self.best_y + (self.box_height - best_rect.height) // 2 ) + (self.box_height * 0.05)
        game.screen.blit(best_text, (best_rect_text_x, best_rect_text_y))

        #The title "Best" blitted just above the rectangle
        title = self.title_font.render(str("Best"), True, colours.GREY_BLACK)
        title_rect = title.get_rect()
        title_x = self.best_x + (self.box_width - title_rect.width) // 2
        title_y = (self.best_y + (self.box_height - title_rect.height) // 2) - 35
        game.screen.blit(title, (title_x, title_y))
    
    def _draw_end_game(self):
        """
        This function draws the endgame state
        This consists of a translucent rect blitted over the board in yellow
        
        If the user has won, we will draw:
            - a try again button and a continue button
        and if they have lost then only the try again button is displayed
        """
        pygame.draw.rect(self.transparent_surface, (237, 207, 114, 100), self.transparent_surface.get_rect())
        game.screen.blit(self.transparent_surface, self.rect)

        if gamestate.win:
            self.try_again_button.x = self.try_again_button.rect.x = (self.rect.centerx - self.box_width // 2) + (self.box_width * 0.8)
            self.continue_button.draw()
        self.try_again_button.draw()
        
        """
        This is a title indicating the end gamestate state
        For example You Won or You Lose
        """
        text = self.end_game_font.render(self.end_game_text, True, self.end_game_text_colour)
        text_x = (game.SCREEN_WIDTH  - text.get_width()) // 2
        text_y = (game.SCREEN_HEIGHT - text.get_height()) // 2 - 85
        game.screen.blit(text, (text_x, text_y))


    def handle(self, event):
        """
        This function handles all inputs for the board that are made by the user
        """
        self.reset_button.handle(event)
        
        """
        Default index values for searching board for shift function
        """
        row_iterator = 1
        row_start = 0
        row_end = self.rows

        column_iterator = 1
        column_start = 0
        column_end = self.columns

        """
        If the key is down or right me must change the start and end values so the shift function works correctly
        """
        if event.type == KEYDOWN and event.key in (K_DOWN, K_RIGHT, K_s, K_d):
            row_iterator = -1
            row_start, row_end = row_end-1, -1
            column_iterator = -1
            column_start, column_end = column_end-1, -1

        #Whilst the game has not ended we want to handle all keyboard inputs 
        if not gamestate.end_game and event.type == KEYDOWN and event.key in self.valid_inputs: 
            shifts = []
            direction = pygame.key.name(event.key)
            
            for row in range(row_start, row_end, row_iterator):
                locked_positions = set() 
                for column in range(column_start, column_end, column_iterator):
                    shifts.append(self.shift(direction, row, column, locked_positions))
            
            #If there are absolutely no values that have moved we break out of the function by returning
            if not any(has_shifted for has_shifted in shifts): return  
            else:
                #if there are tiles that have been shifted we generate a new block and play the move sound (sweep)
                sound.sweep.play()
                self.generate_random_block()

        else:
            #When the game has ended (win or lose) we want to handle the middle screen buttons
            self.try_again_button.handle(event)
            
            if gamestate.win:
                self.continue_button.handle(event)
        
        self.check_end_game()

    def get_remaining_spaces(self):
        """
        This function simple counts the number of current free tiles on the board
        That is to say when the tile has a value of 0
        """
        return sum (1 for row in self for tile in row if not tile.value)

    def get_next_position(self, direction, current_position):
        """
        This function will simply return the next cardinal position based upon the direction given
        for example:
        if (0, 0) if passed with direciton left the return value is: (0, -1)
        """
        row, column = current_position

        if direction in ("left", "a"):
            return (row, column - 1)
        
        elif direction in ("right", "d"):
            return (row, column + 1)
        
        elif direction in ("up", "w"):
            return (row - 1, column)
        
        elif direction in ("down", "s"):
            return (row + 1, column)


    def shift(self, direction, row, column, locked_positions):
        """
        This function shifts the given tile/block to the maximum boundary it can reach given the direction of movement
        It returns a boolean to indicate whether a shift was possible or not
        """
        if self[row][column].value != 0:
            shifted = False
            new_position = new_row, new_column =  self.get_next_position(direction, (row, column))
            positions = [(new_row, new_column)]

            while self.check_in_bounds(new_row, new_column):

                """
                If the current tile is the same as the new one then we can merge the tiles
                This is multipling the value by 2.
                """
                if self[row][column].value == self[new_row][new_column].value:
                    """
                    If the new position is in a locked position we cannot go further and so break
                    A locked position is one where a merge has already taken place.
                    
                    for example:
                    
                    Without locked positions the following row 
                    2 2 2 2
                    becomes 
                    0 0 0 8 

                    with locked positions, however, it becomes:
                    0 0 4 4
                    0 1 2 3
                    with index positions 3 and 2 being locked

                    In short, the set 'locked positions' contains all positions where one merge has already taken place 
                    """
                    if new_position in locked_positions: break

                    #Score and Best score is updated accordingly
                    self.score += self[row][column].value
                    self.best = max(self.best, self.score)
                
                    #New and old value changed accordingly 
                    self[new_row][new_column].value *= 2
                    self[row][column].value = 0

                    locked_positions.add((new_position))
                    return True

                #If the new tile is not empty or the same as the original tile we break
                #This means we have hit "the wall" of the given row and no more shifts will take place
                elif self[new_row][new_column].value not in (0, self[row][column].value):
                    break
                
                #The new position is valid and a shiftable position for the given tile
                else:
                    new_position = new_row, new_column = self.get_next_position(direction, (new_row, new_column))
                    positions.append((new_position))

            """
            This last part finds the max boundary tile the initial tile can "move" to and then updates the tile
            """
            if len(positions) >= 2:
                new_row, new_column = positions[-2]
                self[row][column].value, self[new_row][new_column].value = self[new_row][new_column].value, self[row][column].value  
                shifted = True
            return shifted
                
    def check_end_game(self):
        """
        This funciton checks the endgame states based upon whether there are spaces left on the board
        """
        if self.get_remaining_spaces() == 0:
            self.check_lose()
        else:
            self.check_win()   

    def check_win(self):
        """
        This function simply check to see if any tile on the board is identical to the game goal
        """
        for row in self:
            for tile in row:
                if tile.value == int(game.goal):
                    gamestate.continuing = True
                    gamestate.win = True
                    gamestate.end_game = True
                    self.end_game_text = "You Win"
                    self.end_game_text_colour = colours.WHITE
                    sound.win.play()

    def check_lose(self):
        """
        This function checks to see if there are not more valid shifts to be made for each tile
        """
        if not gamestate.lose:
            for row in self:
                for tile in row:
                    directions = [self.get_next_position(direction, tile.position) for direction in ("left", "right", "up", "down")]
                    #if there is at least one valid move we can return from this function as there has been no lose yet
                    if any(1 for (row, column) in directions if self.check_in_bounds(row, column) and self[row][column].value == tile.value):
                        return 
                
            gamestate.lose = True
            gamestate.end_game = True
            self.end_game_text = "You Lose"
            self.end_game_text_colour = colours.GREY_BLACK
            sound.lose.play()
          
    def check_in_bounds(self, row, column):
        """
        This function checks to see if the given row and column provided is within the bounds of the board
        """
        return (0 <= row < self.rows) and (0 <= column < self.columns)
