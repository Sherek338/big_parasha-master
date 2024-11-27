import os
import sys
import pygame
import random
from screeninfo import get_monitors

import events.Events as Events
import entity.Hero as Hero
import entity.Enemy as Enemy
import tools.Cell as Cell
import tools.Close as Close
import tools.Button as Button
import tools.funcs as Funcs
import tools.Modal as Modal


class Scene:
    ROWS = 8
    COLS = 9
    BLOCK_SIZE = 86
    hp = 3
    cur_type = -1
    cur_position = (4, 5)
    heart_pos = [(250, 720), (250, 500), (250, 270)]
    can_play = True

    @staticmethod
    def init(swith_scene):
        Scene.WIDTH, Scene.HEIGHT = get_monitors()[0].width, get_monitors()[0].height
        Scene.CENTER_MARGIN_X = (Scene.WIDTH / 2) - ((Scene.COLS * Scene.BLOCK_SIZE) / 2)
        Scene.CENTER_MARGIN_Y = Scene.HEIGHT - 150 - (Scene.ROWS * Scene.BLOCK_SIZE)
        Scene.is_modal_open = False
        
        main_bg_path = os.path.join(os.getcwd(), 'assets', 'sprites', 'bg.png')
        attack_btn_path = os.path.join(os.getcwd(), 'assets', 'image', 'static', 'ctbg1.png')
        attack_btn_hover_path = os.path.join(os.getcwd(), 'assets', 'image', 'static', 'ctbg.png')
        ornament_path = os.path.join(os.getcwd(), 'assets', 'sprites', 'orn.png')
        heart_full_path = os.path.join(os.getcwd(), 'assets', 'sprites', 'HP_FULL.png')
        heart_lost_path = os.path.join(os.getcwd(), 'assets', 'sprites', 'HP_LOST.png')
        game_name_path = os.path.join(os.getcwd(), 'assets', 'sprites', 'NAME.png')
        lvl_music_path = os.path.join(os.getcwd(), 'assets', 'ost', 'lvl_theme.wav')
        font_path = os.path.join(os.getcwd(), 'assets', 'fonts', 'Inter-Regular.ttf')
        Scene.hero_death_path = os.path.join(os.getcwd(), 'assets', 'image', 'animated', 'hero', 'hero_3.png')
        
        # assets
        Scene.MAIN_BG = pygame.transform.scale(pygame.image.load(main_bg_path).convert(), (Scene.WIDTH, Scene.HEIGHT))
        Scene.ATTACK_BTN = pygame.image.load(attack_btn_path).convert_alpha()
        Scene.ATTACK_HOVER_BTN = pygame.image.load(attack_btn_hover_path).convert_alpha()
        Scene.ORNAMENT = pygame.image.load(ornament_path).convert_alpha()
        Scene.HEART_FULL = pygame.image.load(heart_full_path).convert_alpha()
        Scene.HEART_LOST = pygame.image.load(heart_lost_path).convert_alpha()
        Scene.GAME_NAME = pygame.image.load(game_name_path).convert_alpha()
        Scene.font = pygame.font.Font(font_path, 32)
        pygame.mixer.music.load(lvl_music_path)
        pygame.mixer.music.play(100, 0, 0)
        
        # groups
        Scene.all_sprites = pygame.sprite.Group()
        Scene.game_over_modal = pygame.sprite.Group()

        Scene.grid = [[0 for _ in range(Scene.COLS)] for _ in range(Scene.ROWS)]
        Funcs.draw_grid(Scene.grid, Scene.cur_position, Scene.all_sprites, Scene.BLOCK_SIZE, Scene.CENTER_MARGIN_X, Scene.CENTER_MARGIN_Y)
        Scene.cur_sequence = [Scene.grid[5][4]]
        Scene.cur_sequence_set = set(Scene.cur_sequence)
        
        Scene.go_modal = Modal.ModuleClass((45, 35), Scene.font.render("Вы проиграли", 1, (0, 0, 0)),
                                            Scene.font.render("Меню", 1, (0, 0, 0)), swith_scene)
        
        Scene.attack_btn = Button.ButtonClass((1350, 800), Scene.ATTACK_BTN, Scene.ATTACK_HOVER_BTN, Scene.on_attack, Scene.font.render("АТАКОВАТЬ", 1, (255, 255, 255)))

        Scene.all_sprites.add(Scene.attack_btn)
        Scene.game_over_modal.add(Scene.go_modal)
        Scene.go_modal.add_group(Scene.game_over_modal)

        Scene.close_cells = Close.get_close(Scene.grid, Scene.cur_position, Scene.ROWS, Scene.COLS)

    @staticmethod
    def update(win):
        is_click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                Scene.switch_modal_mode()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                is_click = True
                # if not Scene.can_play:
                #     Scene.main_menu_btn.is_press(mx, my)
                # if Scene.can_play:
                #     if Scene.attack_btn.is_press(mx, my, [Scene.cur_sequence]):
                #         Scene.cur_type = -1
                #         x, y = Scene.cur_position
                #         Scene.cur_sequence = [Scene.grid[y][x]]
                #         Scene.cur_sequence_set = set(Scene.cur_sequence)
                #         Scene.close_cells = Close.get_close(Scene.grid, Scene.cur_position, Scene.ROWS, Scene.COLS)
                #         for cell in Scene.close_cells:
                #             if cell.item.is_angry:
                #                 Scene.hp -= 1
                #                 if Scene.hp <= 0:
                #                     pygame.event.post(pygame.event.Event(Events.DEADTH_EVENT))
                #     for cell in Scene.close_cells:
                #         if not cell.is_mouse_over(mx, my):
                #             continue
                #         if cell in Scene.cur_sequence_set:
                #             continue
                #         if Scene.cur_type == cell.item.type or Scene.cur_type == -1:
                #             cell.item.image = cell.item.image_selected
                #             Scene.cur_type = cell.item.type
                #             Scene.cur_position = cell.pos
                #             Scene.cur_sequence.append(cell)
                #             Scene.cur_sequence_set.add(cell)
                #             Scene.close_cells = Close.get_close(Scene.grid, Scene.cur_position, Scene.ROWS, Scene.COLS)
            if event.type == Events.DEADTH_EVENT:
                Scene.cur_sequence[0].item.image = pygame.image.load(Scene.hero_death_path)
                Scene.can_play = False

        win.blit(Scene.MAIN_BG, (0, 0))
        win.blit(Scene.GAME_NAME, ((Scene.WIDTH / 2) - (Scene.GAME_NAME.get_rect().width / 2), 130))
        win.blit(Scene.ORNAMENT, (1420, 150))

        count = 0
        for pos in Scene.heart_pos:
            if count < Scene.hp:
                count += 1
                win.blit(Scene.HEART_FULL, pos)
            else:
                win.blit(Scene.HEART_LOST, pos)

        Scene.all_sprites.draw(win)

        for cell in Scene.close_cells:
            if cell in Scene.cur_sequence_set:
                cell.item.image = cell.item.image_selected


        if not Scene.is_modal_open:
            Scene.all_sprites.update(is_click)
        else:
            Scene.game_over_modal.draw(win)
            Scene.game_over_modal.update(is_click)

        pygame.display.flip()

    @staticmethod
    def on_attack(props):
        cur_sequence = props[0]
        if len(cur_sequence) < 2:
            return
        hero_cell = cur_sequence[-1]
        herx, hery = hero_cell.pos
        hero = Hero.HeroClass((herx * Scene.BLOCK_SIZE + Scene.CENTER_MARGIN_X, hery * Scene.BLOCK_SIZE + Scene.CENTER_MARGIN_Y), (Scene.BLOCK_SIZE, Scene.BLOCK_SIZE))
        Scene.all_sprites.remove(hero_cell.item)
        Scene.all_sprites.add(hero)
        Scene.grid[hery][herx] = Cell.CellClass(hero, (herx, hery))
        for cell in cur_sequence[:-1]:
            Scene.all_sprites.remove(cell.item)
            x, y = cell.pos
            enemy = Enemy.EnemyClass(random.randint(1, 3), (x * Scene.BLOCK_SIZE + Scene.CENTER_MARGIN_X, y * Scene.BLOCK_SIZE + Scene.CENTER_MARGIN_Y), (Scene.BLOCK_SIZE, Scene.BLOCK_SIZE))
            Scene.grid[y][x] = Cell.CellClass(enemy, (x, y))
            Scene.all_sprites.add(enemy)
            
    @staticmethod
    def switch_modal_mode():
        Scene.is_modal_open = not Scene.is_modal_open
