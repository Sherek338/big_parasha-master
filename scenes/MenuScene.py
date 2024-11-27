import pygame
import sys
import os
from screeninfo import get_monitors
import tools.Button as Button
import tools.Modal as Modal

class Scene:
    @staticmethod
    def init(swith_scene):
        WIDTH, HEIGHT = get_monitors()[0].width, get_monitors()[0].height
        Scene.is_modal_open = False
                
        bg_path = os.path.join(os.getcwd(), 'assets', 'image', 'static', 'mainmenubg.png')
        music_path = os.path.join(os.getcwd(), 'assets', 'ost', 'Main_theme.wav')
        btn_bg_path = os.path.join(os.getcwd(), 'assets', 'image', 'static', 'ctbg1.png')
        btn_hover_path = os.path.join(os.getcwd(), 'assets', 'image', 'static', 'ctbg.png')
        font_path = os.path.join(os.getcwd(), 'assets', 'fonts', 'Inter-Medium.ttf')
        
        Scene.BG =  pygame.transform.scale(pygame.image.load(bg_path).convert(), (WIDTH, HEIGHT))
        BTN_PLAY_BG = pygame.image.load(btn_bg_path).convert_alpha()
        BTN_EXIT_BG = pygame.image.load(btn_bg_path).convert_alpha()
        BTN_PLAY_HOVER_BG = pygame.image.load(btn_hover_path).convert_alpha()
        BTN_EXIT_HOVER_BG = pygame.image.load(btn_hover_path).convert_alpha()
        font = pygame.font.Font(font_path,  40)
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play(100,0,0)

        Scene.btn_group = pygame.sprite.Group()
        Scene.modal_group = pygame.sprite.Group()
        
        Scene.modal = Modal.ModuleClass((45, 35), font.render("Вы уверенны, что хотите выйти?", 1, (0, 0, 0)),
                                        font.render("Да", 1, (0, 0, 0)), sys.exit, font.render("Нет", 1, (0, 0, 0)), Scene.switch_modal_mode)
        Scene.play_btn = Button.ButtonClass((580, 600), BTN_PLAY_BG, BTN_PLAY_HOVER_BG, swith_scene, font.render("Играть", 1, (0, 0, 0)))
        Scene.exit_btn = Button.ButtonClass((580, 700), BTN_EXIT_BG, BTN_EXIT_HOVER_BG, Scene.switch_modal_mode, font.render("Выход", 1, (0, 0, 0)))
        
        Scene.btn_group.add(Scene.play_btn)
        Scene.btn_group.add(Scene.exit_btn)
        Scene.modal_group.add(Scene.modal)
        Scene.modal.add_group(Scene.modal_group)

    @staticmethod
    def update(win):
        is_click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                Scene.switch_modal_mode()
            
            if event.type == pygame.MOUSEBUTTONDOWN: 
                is_click = True
                
        win.blit(Scene.BG, (0, 0))
        
        Scene.btn_group.draw(win)
        
        if not Scene.is_modal_open:
            Scene.btn_group.update(is_click)
        else:
            Scene.modal_group.draw(win)
            Scene.modal_group.update(is_click)
    
        pygame.display.flip()
        
    @staticmethod
    def switch_modal_mode():
        Scene.is_modal_open = not Scene.is_modal_open