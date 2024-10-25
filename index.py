import pygame
import scenes.LevelScene as Level
import scenes.MenuScene as Menu
from screeninfo import get_monitors

WIDTH, HEIGHT = 0, 0
for monitor in get_monitors():
    WIDTH, HEIGHT = monitor.width, monitor.height

pygame.init()
pygame.font.init()
pygame.display.init()

win = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

cur_scene = 'MENU'
def switch_scene_menu():
    Menu.Scene.init(WIDTH, HEIGHT, switch_scene_lvl)
    global cur_scene
    cur_scene = 'MENU' 
def switch_scene_lvl():
    Level.Scene.init(WIDTH, HEIGHT, switch_scene_menu)
    global cur_scene
    cur_scene = 'LEVEL'

def main():    
    Menu.Scene.init(WIDTH, HEIGHT, switch_scene_lvl)
    Level.Scene.init(WIDTH, HEIGHT, switch_scene_menu)

    run = True
    while run:
        clock.tick(60)

        if cur_scene == 'MENU':
            Menu.Scene.update(win)
        elif cur_scene == 'LEVEL':
            Level.Scene.update(win)
        
    pygame.quit()

if __name__ == "__main__":
    main()