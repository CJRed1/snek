# Import
import pygame
from pygame.locals import *
import constants
import time
import random

# Hey! CJ here. When I started this project, only
# me and God knew what was going on, now, only God
# knows! So if you try to modify the code (and
# ultimately fail), please update this counter

# total_hours_wasted_here = 253

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

# Classes
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
        self.snake_headL = pygame.image.load('images/snek_lhead.png')
        self.snake_headD = pygame.image.load('images/snek_dhead.png')
        self.snake_headU = pygame.image.load('images/snek_uhead.png')
        self.snake_headR = pygame.image.load('images/snek_rhead.png')
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
            if i == 0:
                if self.direction == 'left':
                    self.parent_window.blit(self.snake_headL, (self.x[i], self.y[i]))
                elif self.direction == 'right':
                    self.parent_window.blit(self.snake_headR, (self.x[i], self.y[i]))
                elif self.direction == 'up':
                    self.parent_window.blit(self.snake_headU, (self.x[i], self.y[i]))
                else:
                    self.parent_window.blit(self.snake_headD, (self.x[i], self.y[i]))
            else:
                self.parent_window.blit(self.snake_body, (self.x[i], self.y[i]))
            pygame.display.flip()

    # Moving
    def move_left(self):
        if self.direction != 'right':
            self.direction = 'left'

    def move_right(self):
        if self.direction != 'left':
            self.direction = 'right'

    def move_up(self):
        if self.direction != 'down':
            self.direction = 'up'

    def move_down(self):
        if self.direction != 'up':
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

# Gun... why not  
class Pitola():
    def __init__(self, parent_window):
        self.parent_window = parent_window
        self.image = pygame.image.load('images/pitola.png')
        self.x = 64
        self.y = 40

    def draw(self):
        self.parent_window.blit(self.image, (self.x, self.y))
        pygame.display.flip()

# Game
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

        self.pitola = Pitola(self.window)
        self.pitola.draw()

        pygame.display.update()

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + constants.snek_size:
            if y1 >= y2 and y1 < y2 + constants.snek_size:
                return True
        return False
    
# Whole game
    def play(self):
        self.pitola.x = self.snek.x[0] + 32
        self.pitola.y = self.snek.y[0] + 8
        self.snek.walk()
        self.aple.draw()
        self.pitola.draw()
        self.show_score()
        pygame.display.flip()
        
        if self.is_collision(self.snek.x[0], self.snek.y[0], self.aple.x, self.aple.y):
            self.aple.move()
            pygame.mixer.Sound.play(aple)
            self.snek.increase()
            if self.speed >= 0.05:
                self.speed -= 0.01

        for i in range(1, self.snek.length):
            if self.snek.direction != 'none' and self.is_collision(self.snek.x[0], self.snek.y[0], self.snek.x[i], self.snek.y[i]):
                self.show_death()
                if self.snek.direction != 'death':
                    pygame.mixer.Sound.play(collision)
                self.snek.direction = 'death'
                self.speed = 0.3
                pygame.display.flip()
        
        # Warping
        if self.snek.x[0] < 0:
            self.snek.x[0] = constants.wscreen - 32
        if self.snek.x[0] >= constants.wscreen:
            self.snek.x[0] = 0

        if self.snek.y[0] < 0:
            self.snek.y[0] = constants.hscreen - 32
        if self.snek.y[0] >= constants.hscreen:
            self.snek.y[0] = 0

    # Texts 
    def show_death(self):
        font = pygame.font.Font('Pixels.ttf', 60)
        death = font.render(f'You lost! - Score: {self.snek.length - 5}', True, (0, 0, 0))
        self.window.blit(death, (120, 120))
        death2 = font.render(f'Press [ENTER] to restart, Press [ESC] to exit', True, (0, 0, 0))
        self.window.blit(death2, (50, 240))
        
    def show_score(self):
        font = pygame.font.Font('Pixels.ttf', 60)
        score = font.render(f'Score: {self.snek.length - 5}', True, (0, 0, 0))
        self.window.blit(score, (5, -15))

    # Running & Events
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    
                    if self.snek.direction != 'death':
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

                    if event.key == K_RETURN and self.snek.direction == 'death':
                        self.snek.direction = 'none'
                        self.snek.length = 5
                        self.snek.x = [constants.snek_size]*5
                        self.snek.y = [constants.snek_size]*5
                        self.aple.move()


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

# Game Loop
game = Game()
game.run()