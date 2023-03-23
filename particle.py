import pygame
import random


# ma kohe kindlasti ei ahvinud seda internetist maha :)
class Particle:

    def __init__(self, startx, starty):
        self.x = startx
        self.y = starty
        self.col = (255, 0, 0)
        self.sx = startx
        self.sy = starty

    def move(self):
        self.x += random.randint(-5, 5)
        self.y += random.randint(-5, 5)
