from pygame import Color as c

WHITE = c('white')
BLACK = c('black')

BACKGROUND = (250, 248, 239)

two = (238, 228, 218)
four = (237, 224, 200)
eight = (242, 177, 121)
sixteen = (245, 149, 99)
thirty_two = (246, 124, 95)
sixty_four = (246, 94, 59)

yellow = (237, 207, 114) #128 - 256 - 512 - 1024 - 2048
blackish = (60, 58, 50) # > 4096

text = (119, 110, 101)
board = (187, 173, 160)
default_tile = (205, 193, 180)
new_game = (143, 122, 102)

def get_number_colour(number):
    match number:
        case 0:
            return default_tile
        case 2:
            return two
        case 4:
            return four
        case 8:
            return eight
        case 16:
            return sixteen
        case 32:
            return thirty_two
        case 64:
            return sixty_four
        case _:
            pass
        
    if 128 <= number <= 2048:
        return yellow
    else:
        return blackish

