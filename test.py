import pygame
import sys

pygame.init()

# Set up display dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Slide Square')

white = (255, 255, 255)
blue = (0, 0, 255)

square_size = 50
initial_position = (0, 0)
target_position = (700, 500)

current_position = initial_position

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if current_position != target_position:
        step_x = (target_position[0] - initial_position[0]) / 100.0
        step_y = (target_position[1] - initial_position[1]) / 100.0
        current_position = (current_position[0] + step_x, current_position[1] + step_y)

    screen.fill(white)
    pygame.draw.rect(screen, blue, (current_position[0], current_position[1], square_size, square_size))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
