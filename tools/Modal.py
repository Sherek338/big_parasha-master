import pygame
from screeninfo import get_monitors
import tools.Button as Button

class ModuleClass(pygame.sprite.Sprite):
    def __init__(self, size, label, label_confirm, onconfirm, label_deny = None, ondeny = None) -> None:
        super().__init__()
        self.width, self.height = size
        self.label = label
        self.label_rect = self.label.get_rect()
        self.label_deny = label_deny
        
        self.screen_percent = (get_monitors()[0].width / 100, get_monitors()[0].height / 100)
        self.module_percent = ((self.width * self.screen_percent[0]) / 100, (self.height * self.screen_percent[1]) / 100)
        
        self.image = pygame.Surface((self.screen_percent[0] * size[0], self.screen_percent[1] * size[1])) 
        self.image.fill((250, 250, 210))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.screen_percent[0] * 50 - (self.screen_percent[0] * self.width) / 2,
                            self.screen_percent[1] * 50 - (self.screen_percent[1] * self.height) / 2)
        
        btn_confirm_bg = pygame.Surface((self.module_percent[0] * 25, self.module_percent[1] * 15))
        btn_confirm_hover = pygame.Surface((self.module_percent[0] * 25, self.module_percent[1] * 15))
        btn_confirm_bg.fill((50, 205, 50))
        btn_confirm_hover.fill((152, 251, 152))
        self.btn_confirm = Button.ButtonClass(((self.screen_percent[0] * 50) - (self.module_percent[0] * 25) / 2, self.screen_percent[1] * 55),
                                            btn_confirm_bg, btn_confirm_hover, onconfirm, label_confirm)
        
        if label_deny is not None:
            self.btn_confirm.rect.topleft = ((self.screen_percent[0] * 35, self.screen_percent[1] * 55))
            btn_deny_bg = pygame.Surface((self.module_percent[0] * 25, self.module_percent[1] * 15))
            btn_deny_hover = pygame.Surface((self.module_percent[0] * 25, self.module_percent[1] * 15))
            btn_deny_bg.fill((178, 34, 34))
            btn_deny_hover.fill((220, 20, 60))
            self.btn_deny = Button.ButtonClass((self.screen_percent[0] * 55, self.screen_percent[1] * 55), btn_deny_bg, btn_deny_hover, ondeny, label_deny)
            
            
    def add_group(self, group):
        group.add(self.btn_confirm)
        if self.label_deny is not None:
            group.add(self.btn_deny)
            
    def update(self, a = None):
        self.image.blit(self.label, (self.module_percent[0] * 50 - self.label_rect.width / 2 , self.module_percent[1] * 30))

        