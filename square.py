import pygame

class Square():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.barrier = 0
        self.width = 25
        self.rect = pygame.Rect(self.x, self.y, self.width, self.width)