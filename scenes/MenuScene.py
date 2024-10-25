import pygame
import sys
import tools.Button as Button

class Scene:
  BG = None
  play_btn = None
  exit_btn = None
  EXIT_BTN = None
  btn_group = None
  LVL_MUSIC = None
  
  @staticmethod
  def init(WIDTH, HEIGHT, swith_scene):
    Scene.BG =  pygame.transform.scale(pygame.image.load("assets\image\static\mainmenubg.png").convert(), (WIDTH, HEIGHT))
    BTN_PLAY_BG = pygame.image.load("assets\image\static\ctbg1.png").convert_alpha()
    BTN_EXIT_BG = pygame.image.load("assets\image\static\ctbg1.png").convert_alpha()
    BTN_PLAY_HOVER_BG = pygame.image.load("assets\image\static\ctbg.png").convert_alpha()
    BTN_EXIT_HOVER_BG = pygame.image.load("assets\image\static\ctbg.png").convert_alpha()
    
    font = pygame.font.Font("./assets/fonts/Inter-Medium.ttf", 40)

    Scene.play_btn = Button.ButtonClass((580, 600), BTN_PLAY_BG, BTN_PLAY_HOVER_BG, swith_scene, font.render("Играть", 1, (0, 0, 0)))
    Scene.exit_btn = Button.ButtonClass((580, 700), BTN_EXIT_BG, BTN_EXIT_HOVER_BG, Scene.exit, font.render("Выход", 1, (0, 0, 0)))
    
    Scene.btn_group = pygame.sprite.Group()
    Scene.btn_group.add(Scene.play_btn)
    Scene.btn_group.add(Scene.exit_btn)

    Scene.LVL_MUSIC = pygame.mixer.music.load("./assets/ost/Main_theme.wav")
    pygame.mixer.music.play(100,0,0)

  @staticmethod
  def update(win):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()
          
      if event.type == pygame.MOUSEMOTION:
        mx, my = pygame.mouse.get_pos() 
        Scene.play_btn.on_hover(mx, my)
        Scene.exit_btn.on_hover(mx, my)
      
      if event.type == pygame.MOUSEBUTTONDOWN: 
        mx, my = pygame.mouse.get_pos() 
        Scene.play_btn.is_press(mx, my)
        Scene.exit_btn.is_press(mx, my)
            
    win.blit(Scene.BG, (0, 0))
    
    Scene.btn_group.draw(win)
    Scene.btn_group.update()
  
    pygame.display.flip()
    
  @staticmethod
  def exit():
    pygame.quit()
    sys.exit()