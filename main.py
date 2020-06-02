import pygame
import os
import math
import random
import time
from player import Player
from pipe import Pipe
from population import Population


population = 100 # set initial population

config = [
        # 3 input: bird y position, top pipe position and bottom pipe position
		{"nodeCount": 3, "type": "input"},
        # output 1: jump or not
		{"nodeCount": 1, "type": "output"}
	]

birds = [] # array contains bird object

def setup():
    global WIN_WIDTH
    global WIN_HEIGHT
    global FLOOR
    global STAT_FONT
    global END_FONT
    global DRAW_LINES
    global WIN
    global population
    global bg_img
    global bird_images
    global pipe_img
    global neat

    pygame.font.init()
    WIN_WIDTH = 600
    WIN_HEIGHT = 750
    FLOOR = 730

    # font style for displaying text
    STAT_FONT = pygame.font.SysFont("comicsans", 50)
    END_FONT = pygame.font.SysFont("comicsans", 70)

    # indicate whether to show line from birds to pipes or not
    # set to true if you want to draw lines
    DRAW_LINES = False

    WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption("Flappy Bird")
    
    # load image assets
    pipe_img = pygame.transform.scale2x(pygame.image.load(os.path.join("img","pipe.png")).convert_alpha())
    bg_img = pygame.transform.scale(pygame.image.load(os.path.join("img","bg.png")).convert_alpha(), (600, 900))
    bird_images = [pygame.transform.scale2x(pygame.image.load(os.path.join("img","bird" + str(x) + ".png"))) for x in range(1,4)]

    # init population
    for i in range(population):
        birds.append(Player(WIN, bird_images, 200, 200))
    
    # init NEAT algorithm
    neat = Population(config)
    






def draw(birds, win, pipes):
    """draw birds to the screen \n
    add line indication for detecting closest pipes
    """
    for pipe in pipes:
        pipe.show(WIN)
    for bird in birds:
        # draw lines from bird to pipe
        if DRAW_LINES:
            try:
                # draw lines from bird to closest pipe
                pygame.draw.line(win, (255,0,0), (bird.x+bird.img.get_width()/2, bird.y + bird.img.get_height()/2), (pipes[pipe_ind].x + pipes[pipe_ind].PIPE_TOP.get_width()/2, pipes[pipe_ind].height), 5)
                pygame.draw.line(win, (255,0,0), (bird.x+bird.img.get_width()/2, bird.y + bird.img.get_height()/2), (pipes[pipe_ind].x + pipes[pipe_ind].PIPE_BOTTOM.get_width()/2, pipes[pipe_ind].bottom), 5)
            except:
                pass
        # draw bird
        if bird.dead == False:
            bird.show()
    pygame.display.update()






setup()


#player = Player(WIN, bird_images ,200, 200)
pipes = [Pipe(pipe_img, 700)]
while True:
    add_pipe = False
    rem = []
    pipe_ind = 0
    
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

    if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():  # determine whether to use the first or second
                pipe_ind = 1

    WIN.blit(bg_img, (0, 0))
    for pipe in pipes:
        for bird in birds:
            # detect for bird collision
            if pipe.collide(bird):
                bird.dead = True

        if pipe.x + pipe.PIPE_TOP.get_width() < 0:
            rem.append(pipe)
        
        if not pipe.passed and pipe.x < bird.x:
            pipe.passed = True
            add_pipe = True
        pipe.update()
    
    # send bird location to the nn, top pipe location and bottom pipe location
    for i in range(population):
        birds[i].update()
        neat.observe([birds[i].y, abs(birds[i].y - pipes[pipe_ind].height), abs(birds[i].y - pipes[pipe_ind].bottom)], i)

    neat.feed_forward() # feed forward the network
    decisions = neat.think() # get neural network output in form of array

    for i in range(population):
        if decisions[i] > 0.5: # for tanh activation, we decide whether to jump or not if the value is larger than 0.5
            birds[i].jump()

    finish = True
    for i in range(len(birds)):
        if birds[i].dead == False:
            finish = False
            break
    
    if finish:
        pipes = [Pipe(pipe_img, 700)] # start over again 
        for i in range(population):
            neat.set_fitness(birds[i].score, i) # set fitness score after all birds are killed
            birds[i] = Player(WIN, bird_images , 200, 200) # create new bird at given index postion
        print(neat.print_statistic())
        neat.perform_natural_selection() # do crossover and mutation method


    for bird in birds:
            # if bird goes out of map
            if bird.y + bird.img.get_height() - 10 >= FLOOR or bird.y < -50:
                bird.dead = True
    if add_pipe:
        pipes.append(Pipe(pipe_img, 700))

    for i in rem:
        pipes.remove(i)
        
    draw(birds, WIN, pipes) #draw everything to the screen