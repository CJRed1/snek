# Import
import pygame
from pygame.locals import *
import constants

sex = 0

class Game():
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(constants.size)
        self.title = pygame.display.set_caption(constants.title)
        icon = pygame.image.load('images/snek.png')
        pygame.display.set_icon(icon)
        self.window.fill(constants.bg_color)
        pygame.display.update()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_s:
                        sex = 1
                    elif event.key == K_e and sex == 1:
                        sex = 2
                    elif event.key == K_x and sex == 2:
                        running = False
                    else:
                        sex = 0
                    
                elif event.type == QUIT:
                    running = False

game = Game()
game.run()