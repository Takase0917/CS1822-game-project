import pygame
from pygame.locals import *

pygame.init()

screen_width = 800
screen_height = 700

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Platformer')

background_img = pygame.image.load('img/background.jpg')

run = True
while run:
    screen.blit(background_img, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
