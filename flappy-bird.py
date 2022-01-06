import time
import os
import random

import pygame
import neat

##########################################

#-----WINDOW SIZE-----
WIN_WIDTH = 500
WIN_HEIGHT = 800

#-----IMPORT IMAGES-----
BIRD_IMGS = [
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird1.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird2.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird3.png")))
]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bg.png")))

#-----FPS-----
FPS = 30
##########################################

class Bird:
    IMGS = BIRD_IMGS  # Easier to self.IMGS
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0 # rotation
        self.tick_count = 0 # for physics
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]

    def jump(self):
        self.vel = -10.5 # To go upwards, we need a negative velocity, since (0,0) is top left
        self.tick_count = 0  # Keep track of when we last jumped (represents time)
        self.height = self.y

    def move(self):
        self.tick_count += 1
        d = self.vel*self.tick_count + 1.5*self.tick_count**2 # Displacement (movement).

        if d >= 16:  # If we move too much, stop accelerating
            d = 16
        
        if d < 0:  # If we move upwards, move a little more
            d -= 2
        
        self.y = self.y + d
        
        # Rotation of the bird depending on the displacement
        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION

        # When you go up, just tilt slightly
        # When you go down, tilt 90º
        else:
            if self.tilt > -90: 
                self.tilt -= self.ROT_VEL

    # What image we should show based on the image count (flying animation)
    def draw(self, win):
        self.img_count += 1

        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        # If tilt is higher than 80º, just show the nose diving image
        if self.tilt <= -80:  
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2

        # Rotate the image from the center
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft = (self.x, self.y)).center)
        win.blit(rotated_image, new_rect.topleft)

    # Object collision
    def get_mask(self):
        return pygame.mask.from_surface(self.img)

##########################################

def draw_window(win, bird):
    win.blit(BG_IMG, (0,0))  # Blit is used to draw
    bird.draw(win)
    pygame.display.update()

def main():
    bird = Bird(200,200)
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(FPS)
        # for each event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        bird.move()
        draw_window(win, bird)
    pygame.quit()
    quit()

main()