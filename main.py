# Import
import pygame
from pygame.locals import *
import constants
import time
import random

nocontext = 0
game_speed = 0.3 
pygame.mixer.init()

# Sounds
rotato = pygame.mixer.Sound("sounds/rotato.ogg")
aple = pygame.mixer.Sound("sounds/aple.ogg")
collision = pygame.mixer.Sound("sounds/collision.ogg")
pygame.mixer.Sound.set_volume(rotato, 0.2)
pygame.mixer.Sound.set_volume(aple, 0.2)
pygame.mixer.Sound.set_volume(collision, 0.2)

class Aple():
    def __init__(self, parent_window):
        self.parent_window = parent_window
        self.image = pygame.image.load('images/aple.png')
        self.x = 32 * random.randint(1, 19)
        self.y = 32 * random.randint(1, 14)

    def draw(self):
        self.parent_window.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = 32 * random.randint(1, 19)
        self.y = 32 * random.randint(1, 14)

class Snek():
    def __init__(self, parent_window, length):
        self.parent_window = parent_window
        self.snake_body = pygame.image.load('images/snek_body.png')
        self.direction = 'none'

        self.length = length
        self.x = [constants.snek_size]*length
        self.y = [constants.snek_size]*length

    def increase(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def draw(self):
        self.parent_window.fill(constants.bg_color)
        for i in range(self.length):
            self.parent_window.blit(self.snake_body, (self.x[i], self.y[i]))
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
        for i in range(self.length-1, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]
        
        # Head
        if self.direction == 'up':
            self.y[0] -= constants.snek_size

        if self.direction == 'down':
            self.y[0] += constants.snek_size

        if self.direction == 'left':
            self.x[0] -= constants.snek_size

        if self.direction == 'right':
            self.x[0] += constants.snek_size
    
        self.draw()
        

class Game():
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(constants.size)
        self.title = pygame.display.set_caption(constants.title)
        icon = pygame.image.load('images/snek.png')
        pygame.display.set_icon(icon)
        self.window.fill(constants.bg_color)
        self.speed = 0.3
        
        self.snek = Snek(self.window, 5)
        self.snek.draw()

        self.aple = Aple(self.window)
        self.aple.draw()

        pygame.display.update()

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + constants.snek_size:
            if y1 >= y2 and y1 < y2 + constants.snek_size:
                return True
        return False
    
    def play(self):
        self.snek.walk()
        self.aple.draw()

        if self.is_collision(self.snek.x[0], self.snek.y[0], self.aple.x, self.aple.y):
            self.aple.move()
            self.snek.increase()
            if self.speed >= 0.05:
                self.speed -= 0.01


    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_UP:
                        self.snek.move_up()
                        pygame.mixer.Sound.play(rotato)
                    if event.key == K_DOWN:
                        self.snek.move_down()
                        pygame.mixer.Sound.play(rotato)
                    if event.key == K_LEFT:
                        self.snek.move_left()
                        pygame.mixer.Sound.play(rotato)
                    if event.key == K_RIGHT:
                        self.snek.move_right()
                        pygame.mixer.Sound.play(rotato)


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

            self.play()
            time.sleep(self.speed)

game = Game()
game.run()