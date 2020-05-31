import random
import pygame





class Player:
    MAX_ROTATION = 25
    ROTATION_VELOCITY = 20
    ANIMATION_TIME = 5

    def __init__(self, win, img, x, y):
        self.IMG = img
        self.win = win
        self.x = y
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMG[0]


        self.fitness = 0
        self.vision = [] # the input array fed into neutral net
        self.decision = [] # the output of NN
        self.lifespan = 0 #how long the player live for this fitness
        self.bestScore = 0 #score of the player
        self.dead = False
        self.score = 0
        self.gen = 0

        self.genomeInputs = 5
        self.genomeOutputs = 2

    #
    #----------------------------------------
    #

    def show(self):
        """show"""
        self.img_count += 1
        if self.img_count <= self.ANIMATION_TIME:
            self.img = self.IMG[0]
        elif self.img_count <= self.ANIMATION_TIME*2:
            self.img = self.IMG[1]
        elif self.img_count <= self.ANIMATION_TIME*3:
            self.img = self.IMG[2]
        elif self.img_count <= self.ANIMATION_TIME*4:
            self.img = self.IMG[1]
        elif self.img_count == self.ANIMATION_TIME*4 + 1:
            self.img = self.IMG[0]
            self.img_count = 0
        
        if self.tilt <= -80:
            self.img = self.IMG[1]
            self.img_count = self.ANIMATION_TIME*2

        blitRotateCenter(self.win, self.img, (self.x, self.y), self.tilt)
    #
    #----------------------------------------
    #

    def move(self):
        """Move player"""
        self.tick_count += 1
        displacement = self.vel*(self.tick_count) + 0.5*(3) *(self.tick_count)**2
        if displacement >= 16:
            displacement = (displacement/abs(displacement)) * 16
        
        if displacement < 0:
            displacement -= 2
        
        self.y = self.y + displacement

        if displacement < 0 or self.y < self.height + 50:  # tilt up
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:  # tilt down
            if self.tilt > -90:
                self.tilt -= self.ROTATION_VELOCITY

    #
    #----------------------------------------
    #
    def updatePipes(self, pipes):
        for pipe in pipes:
            pipe.update()



    def update(self):
        """ """
        self.lifespan += 1
        self.score += 1
        self.move()

    #
    #----------------------------------------
    #

    def look(self):
        """ """
        print('look function ')
    
    #
    #----------------------------------------
    

    #
    #----------------------------------------
    #

    def jump(self):
        """Make the bird jump"""
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    #
    #-------
    #
    def get_mask(self):
        return pygame.mask.from_surface(self.img)

        
   
    
    #
    #----------------------------------------
    #
            
    
    #
    #----------------------------------------
    #



def blitRotateCenter(surf, image, topleft, angle):
    """
    Rotate a surface and blit it to the window
    """
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)

    surf.blit(rotated_image, new_rect.topleft)