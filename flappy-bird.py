#-----IMPORT STANDARD MODULES-----
import time
import os
import random

#-----INSTALL MODULES IF NEEDED-----
from pipinst import pipin
if pipin("pygame","neat-python"):
    exit()
#-----IMPORT OTHER MODULES-----
import pygame
pygame.font.init()
import neat







##########################################

#-----WINDOW SIZE-----
WIN_WIDTH = 500
WIN_HEIGHT = 800

#-----PIPE DISTANCE-----
PIPE_DIST = 600

#-----IMPORT IMAGES-----
BIRD_IMGS = [
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird1.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird2.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird3.png")))
]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bg.png")))

#-----FONTS-----
STAT_FONT = pygame.font.SysFont("comicsans", 50)

#-----FPS-----
FPS = 30

#-----Gen initialization-----
gens = 0
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

    # For object collision
    def get_mask(self):
        return pygame.mask.from_surface(self.img)

##########################################

class Pipe:
    GAP = 200  # Space between the pipe
    VEL = 5

    def __init__(self, x):
        self.x = x
        self.height = 0

        # Top and Bottom possition of pipe
        self.top = 0
        self.bottom = 0

        # Top and Bottom pipe images
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)  # The top pipe is flipped
        self.PIPE_BOTTOM = PIPE_IMG

        self.passed = False  # If the bird is passed by the pipe... (for AI)
        self.set_height()

    #Set the random height of the pipe
    def set_height(self):  # Random pipe height
        self.height = random.randrange(50,450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    # Move the pipe
    def move(self):
        self.x -= self.VEL

    # Draw the pipe
    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    # It returns the pixels that are not transparent on each rectangle to check if those collide
    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)
        
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = self.x - bird.x, self.bottom - round(bird.y)

         # Tells us the point of collision between the bird mask and the bottom pipe. Returns none if they don't collide
        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        if t_point or b_point: # If we are colliding, return True. Else false
            return True
        return False

##########################################

class Base:
    VEL = 5
    WIDTH = BASE_IMG.get_width() # How wide the image is
    IMG = BASE_IMG

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        # If position+width = 0 (if image is off the screen), move the image to the back
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))

##########################################

def draw_window(win, birds, pipes, base, score, gen):
    win.blit(BG_IMG, (0,0))  # Blit is used to draw

    for pipe in pipes: # We can have several pipes on the screen at once
        pipe.draw(win)

    text = STAT_FONT.render("Score: "+str(score), 1, (255,255,255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    gen = STAT_FONT.render("Gen: "+str(gens), 1, (255,255,255))
    win.blit(gen, (10,10))

    base.draw(win)
    for bird in birds:
        bird.draw(win)

    pygame.display.update()

##########################################

def main(genomes, config):
    global gens
    gens += 1
    nets = []
    ge = []
    birds = []

    for _, g in genomes:  # _,g because the tuple is like (x,x) and we only care about the second item
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird(230, 350))
        g.fitness = 0
        ge.append(g)

    base = Base(730)
    pipes = [Pipe(PIPE_DIST)] # Pipe with x=600
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    score = 0

    run = True
    while run:
        clock.tick(FPS)
        # for each event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        # Get the first pipe
        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_ind = 1
        else: # If there are no birds left
            run = False
            break


        # Move birds
        for x, bird in enumerate(birds):
            bird.move()
            ge[x].fitness += 0.1  # If the bird is alive, add 0.1

            output = nets[x].activate((bird.y, abs(bird.y - pipes[pipe_ind].height), 
                     abs(bird.y - pipes[pipe_ind].bottom)))
            
            # If conditions are favorable -> jump
            if (output[0] > 0.5):  # Output is a list, so since we have just 1 output, pich the first one (output[0])
                bird.jump()

        #bird.move()
        add_pipe = False
        rem = [] #remove
        for pipe in pipes: # for each pipe
            for x,bird in enumerate(birds):
                if pipe.collide(bird): # if bird collides with pipe
                    ge[x].fitness -= 1 # Birds that hit pipes will have lower fitness
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)
                if not pipe.passed and pipe.x < bird.x: # Check if we have passed the pipe (and if we hadn't already passed it)
                    pipe.passed = True
                    add_pipe = True
            if pipe.x + pipe.PIPE_TOP.get_width() < 0: # If pipe is off the screen
                    rem.append(pipe)
            pipe.move()

        if add_pipe:
            score += 1
            for g in ge: # Increase fitness if they make it between the two pipes
                g.fitness += 5
            pipes.append(Pipe(PIPE_DIST))

        for r in rem:
            pipes.remove(r)

        for x,bird in enumerate(birds):
            if bird.y + bird.img.get_height() >= 730 or bird.y < 0: # If bird hits the ground or the top
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)

        base.move()
        draw_window(win, birds, pipes, base, score, gens)

##########################################

def run(config_path):
    # Define the subheadings used in the config file
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
    neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    p = neat.Population(config)

    # Show output each generation
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # Calls the main function 50 times
    winner = p.run(main, 50)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)