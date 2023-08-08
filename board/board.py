import game
import os

from .tile import Tile




class Board(list):

    def __init__(self, screen, rows, columns):
        super().__init__([[None for _ in range(columns)] for _ in range(rows)])
        self.screen = screen
        self.rows = rows
        self.columns = columns

        cell_width  =  (game.SCREEN_WIDTH  * 0.75) // self.columns
        cell_height =  (game.SCREEN_HEIGHT * 0.75) // self.rows
        self.cell_width = self.cell_height = min(cell_width, cell_height) #set both the same so cell is perfect square
        self.cell_size = (self.cell_width, self.cell_height) 
        #print(self.cell_size)

        self.generate_tiles()


    def generate_tiles(self):
        x_center_offset = (game.SCREEN_WIDTH - (self.cell_height * self.columns)) / 2
        y_center_offset = ((game.SCREEN_HEIGHT - (self.cell_height * self.rows)) / 2) #+ 30
  

        for row in range(self.rows):
            for column in range(self.columns):
                x =  (column * self.cell_width) 
                x += x_center_offset
                
                y =  (row * self.cell_height)  
                y += y_center_offset
                
                tile = Tile(self.screen, row, column, x, y, self.cell_size)     
                self[row][column] = tile 
         

    def draw(self):
        clear = lambda: os.system('clear')
        clear()

        for row in self:
            print(row)
            for tile in row:
                tile.draw()
