# Import
import pygame
from pygame.locals import *
import constants
import time

nocontext = 0

class Snek():
    def __init__(self, parent_window):
        self.parent_window = parent_window
        self.snake_body = pygame.image.load('images/snek_body.png')
        self.x = 100
        self.y = 100
        self.direction = 'none'

    def draw(self):
        self.parent_window.fill(constants.bg_color)
        self.parent_window.blit(self.snake_body, (self.x, self.y))
        pygame.display.flip()

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def walk(self):
        if self.direction == 'up':
            self.y -= 32

        if self.direction == 'down':
            self.y += 32

        if self.direction == 'left':
            self.x -= 32

        if self.direction == 'right':
            self.x += 32
        
        self.draw()
        

class Game():
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(constants.size)
        self.title = pygame.display.set_caption(constants.title)
        icon = pygame.image.load('images/snek.png')
        pygame.display.set_icon(icon)
        self.window.fill(constants.bg_color)
        
        self.snek = Snek(self.window)
        self.snek.draw()

        pygame.display.update()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_UP:
                        self.snek.move_up()
                    if event.key == K_DOWN:
                        self.snek.move_down()
                    if event.key == K_LEFT:
                        self.snek.move_left()
                    if event.key == K_RIGHT:
                        self.snek.move_right()


                    if event.key == K_s:
                        nocontext = 1
                    elif event.key == K_e and nocontext == 1:
                        nocontext = 2
                    elif event.key == K_x and nocontext == 2:
                        running = False
                    else:
                        nocontext = 0
                    
                elif event.type == QUIT:
                    running = False

            self.snek.walk()
            time.sleep(0.1)

game = Game()
game.run()