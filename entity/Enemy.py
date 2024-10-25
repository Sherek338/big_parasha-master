import pygame
import random

class EnemyClass(pygame.sprite.Sprite):
    def __init__(self, type, pos, size):
        super().__init__()
        self.type = type
        self.psevdo = 5
        self.is_angry = False
        self.warn = pygame.image.load("./assets/image/animated/attention/attention_2.png")
        
        self.image_reg = None
        self.image_selected = None
        
        if random.randint(0, 100) < self.psevdo:
            self.psevdo = 0
            self.is_angry = True
            
        if self.type == 1:
            self.image_reg = pygame.image.load("./assets/image/animated/enemy_1/enemy_standart1.png")
            self.image_selected = pygame.image.load("./assets/image/animated/enemy_1/enemy_selection1.png")
        if self.type == 2:
            self.image_reg = pygame.image.load("./assets/image/animated/enemy_2/enemy_standart1.png")
            self.image_selected = pygame.image.load("./assets/image/animated/enemy_2/enemy_selection1.png")
        if self.type == 3:
            self.image_reg = pygame.image.load("./assets/image/animated/enemy_3/enemy_standart1.png")
            self.image_selected = pygame.image.load("./assets/image/animated/enemy_3/enemy_selection1.png")
        
        self.image = self.image_reg
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        
    def update(self):
        if self.is_angry:
            self.image.blit(self.warn, (0, 0))
        
        