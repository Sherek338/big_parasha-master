import pygame

class ButtonClass(pygame.sprite.Sprite):
    def __init__(self, pos, background, onhover, onclick, label = None) -> None:
        super().__init__()
        self.onclick = onclick
        
        self.image = background
        self.background = background
        self.onhover = onhover
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.label = label
    
    def is_press(self, mx, my, props = None):
        if self.rect.collidepoint(mx, my):
            if props is None: 
                self.onclick()
            else: 
                self.onclick(props) 
            return True
        return False
    
    def on_hover(self, mx, my):
        if self.rect.collidepoint(mx, my):
            self.image = self.onhover
        else:
            self.image = self.background
            
    def update(self):
        if self.label is not None:
            self.image.blit(self.label, (((self.rect.width / 2) - (self.label.get_rect().width / 2)), ((self.rect.height / 2) - (self.label.get_rect().height / 2))))