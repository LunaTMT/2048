import pygame
pygame.init()

click = pygame.mixer.Sound("assets/sounds/click.wav")
click.set_volume(0.05)

sweep = pygame.mixer.Sound("assets/sounds/sweep.wav")
sweep.set_volume(0.5)

win = pygame.mixer.Sound("assets/sounds/win.wav")
win.set_volume(0.5)

lose = pygame.mixer.Sound("assets/sounds/lose.wav")
lose.set_volume(0.5)
