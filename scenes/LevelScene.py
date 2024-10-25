import pygame
import random
import events.Events as Events
import entity.Hero as Hero
import entity.Enemy as Enemy
import tools.Cell as Cell
import tools.Close as Close
import tools.Button as Button
import tools.funcs as Funcs

class Scene:
    WIDTH = 0
    HEIGHT = 0
    ROWS = 8
    COLS = 9
    BLOCK_SIZE = 86
    CENTER_MARGIN_X = 0
    CENTER_MARGIN_Y = 0
    MAIN_BG = None
    ATTACK_BTN = None
    ORNAMENT = None
    HEART_FULL = None
    HEART_LOST = None
    GAME_NAME = None
    LVL_MUSIC = None
    font_attack = None
    grid = None
    all_sprites = None
    hp = 3
    cur_type = -1
    cur_position = (4, 5)
    cur_sequence = None
    cur_sequence_set = None
    heart_pos = [(250, 720), (250, 500), (250, 270)]
    game_over_group = None
    can_play = True
    game_over_rect = None
    game_over_label = None
    main_menu_btn = None
    attack_btn = None
    close_cells = None

    @staticmethod
    def init(WIDTH, HEIGHT, swith_scene):
        Scene.WIDTH = WIDTH
        Scene.HEIGHT = HEIGHT
        Scene.CENTER_MARGIN_X = (WIDTH / 2) - ((Scene.COLS * Scene.BLOCK_SIZE) / 2)
        Scene.CENTER_MARGIN_Y = HEIGHT - 150 - (Scene.ROWS * Scene.BLOCK_SIZE)

        Scene.MAIN_BG = pygame.transform.scale(pygame.image.load("./assets/sprites/bg.png").convert(), (WIDTH, HEIGHT))
        Scene.ATTACK_BTN = pygame.image.load("./assets/sprites/attack_btn.png").convert_alpha()
        Scene.ORNAMENT = pygame.image.load("./assets/sprites/orn.png").convert_alpha()
        Scene.HEART_FULL = pygame.image.load("./assets/sprites/HP_FULL.png").convert_alpha()
        Scene.HEART_LOST = pygame.image.load("./assets/sprites/HP_LOST.png").convert_alpha()
        Scene.GAME_NAME = pygame.image.load("./assets/sprites/NAME.png").convert_alpha()
        
        Scene.LVL_MUSIC = pygame.mixer.music.load("./assets/ost/lvl_theme.wav")
        pygame.mixer.music.play(100, 0, 0)
        
        Scene.font_attack = pygame.font.Font("./assets/fonts/Inter-Regular.ttf", 32)

        Scene.grid = [[0 for _ in range(Scene.COLS)] for _ in range(Scene.ROWS)]
        
        Scene.all_sprites = pygame.sprite.Group()

        Funcs.draw_grid(Scene.grid, Scene.cur_position, Scene.all_sprites, Scene.BLOCK_SIZE, Scene.CENTER_MARGIN_X, Scene.CENTER_MARGIN_Y)
        
        Scene.cur_sequence = [Scene.grid[5][4]]
        Scene.cur_sequence_set = set(Scene.cur_sequence)
        Scene.game_over_group = pygame.sprite.Group()
        Scene.game_over_rect = pygame.Surface((500, 300))
        Scene.game_over_rect.fill((249, 224, 193))
        Scene.game_over_label = Scene.font_attack.render("Game Over", 1, (0, 0, 0))
        main_menu_btn_rect = pygame.Surface((300, 100))
        main_menu_btn_rect.fill((250, 238, 203))
        Scene.main_menu_btn = Button.ButtonClass((810, 550), main_menu_btn_rect, 0, swith_scene, Scene.font_attack.render("Главное меню", 1, (0, 0, 0)))
        Scene.attack_btn = Button.ButtonClass((1350, 800), Scene.ATTACK_BTN, 0, Scene.on_attack, Scene.font_attack.render("АТАКОВАТЬ", 1, (255, 255, 255)))

        Scene.all_sprites.add(Scene.attack_btn)
        Scene.game_over_group.add(Scene.main_menu_btn)

        Scene.close_cells = Close.get_close(Scene.grid, Scene.cur_position, Scene.ROWS, Scene.COLS)

    @staticmethod
    def update(win):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
                
            elif event.type == pygame.MOUSEMOTION:
                pass

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if not Scene.can_play:
                    Scene.main_menu_btn.is_press(mx, my)
                if Scene.can_play:
                    if Scene.attack_btn.is_press(mx, my, [Scene.cur_sequence]):
                        Scene.cur_type = -1
                        x, y = Scene.cur_position
                        Scene.cur_sequence = [Scene.grid[y][x]]
                        Scene.cur_sequence_set = set(Scene.cur_sequence)
                        Scene.close_cells = Close.get_close(Scene.grid, Scene.cur_position, Scene.ROWS, Scene.COLS)
                        for cell in Scene.close_cells:
                            if cell.item.is_angry:
                                Scene.hp -= 1
                                if Scene.hp <= 0:
                                    pygame.event.post(pygame.event.Event(Events.DEADTH_EVENT))
                    for cell in Scene.close_cells:
                        if not cell.is_mouse_over(mx, my):
                            continue
                        if cell in Scene.cur_sequence_set:
                            continue
                        if Scene.cur_type == cell.item.type or Scene.cur_type == -1:
                            cell.item.image = cell.item.image_selected
                            Scene.cur_type = cell.item.type
                            Scene.cur_position = cell.pos
                            Scene.cur_sequence.append(cell)
                            Scene.cur_sequence_set.add(cell)
                            Scene.close_cells = Close.get_close(Scene.grid, Scene.cur_position, Scene.ROWS, Scene.COLS)
            if event.type == Events.DEADTH_EVENT:
                Scene.cur_sequence[0].item.image = pygame.image.load("./assets/image/animated/hero/hero_3.png")
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


        if not Scene.can_play:
            win.blit(Scene.game_over_rect, (710, 450))
            win.blit(Scene.game_over_label, (870, 470))
            Scene.game_over_group.draw(win)
        
        Scene.all_sprites.update()
        Scene.game_over_group.update()

        pygame.display.update()

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
