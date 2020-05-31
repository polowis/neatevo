import pygame
import random
import math

class Pipe:
    GAP = 200
    VELOCITY = 5

    def __init__(self, img,  x):
        self.x = x
        self.pipe_img = img
        self.height = 0
        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(self.pipe_img, False, True)
        self.PIPE_BOTTOM = self.pipe_img

        self.passed = False

        self.set_height()
    
    def set_height(self):
        """set pipe height"""
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP
    
    def update(self):
        """update pipe location"""
        self.x -= self.VELOCITY
    
    def show(self, win):
        """draw pipe"""
        # draw top
        win.blit(self.PIPE_TOP, (self.x, self.top))
            # draw bottom
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def playerPassed(self, bird):
        """check if player passed"""
        if not self.passed and self.x < bird.x:
            self.passed = True


    def collide(self, bird):
        """check if bird collides"""
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask,top_offset)

        if b_point or t_point:
            return True

        return False