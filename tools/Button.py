import pygame

class ButtonClass(pygame.sprite.Sprite):
    def __init__(self, pos, background, onhover, onclick, label = None) -> None:
        super().__init__()        
        self.image = background
        self.background = background
        self.onhover = onhover
        self.onclick = onclick
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.label = label
            
    def update(self, is_click, props = None):
        if self.label is not None:
            self.image.blit(self.label, (((self.rect.width / 2) - (self.label.get_rect().width / 2)),
                                        ((self.rect.height / 2) - (self.label.get_rect().height / 2))))
        mx, my = pygame.mouse.get_pos() 
        if self.rect.collidepoint(mx, my):
            self.image = self.onhover
            if is_click and props is None: self.onclick()
            elif is_click: self.onclick(props)
        else:
            self.image = self.background