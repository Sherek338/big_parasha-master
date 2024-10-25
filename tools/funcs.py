import random
import sys
import entity.Hero as Hero
import entity.Enemy as Enemy
import tools.Cell as Cell

def draw_grid(grid, pos, all_sprites, BLOCK_SIZE, CENTER_MARGIN_X, CENTER_MARGIN_Y):
    posx, posy = pos
    for i, row in enumerate(grid):
        for j, col in enumerate(row):
            if i == posy and j == posx:
                hero = Hero.HeroClass((j * BLOCK_SIZE + CENTER_MARGIN_X, i * BLOCK_SIZE + CENTER_MARGIN_Y), (BLOCK_SIZE, BLOCK_SIZE))
                all_sprites.add(hero)
                grid[i][j] = Cell.CellClass(hero, (j, i))
                continue
            enemy = Enemy.EnemyClass(random.randint(1, 3), (j * BLOCK_SIZE + CENTER_MARGIN_X, i * BLOCK_SIZE + CENTER_MARGIN_Y), (BLOCK_SIZE, BLOCK_SIZE))
            all_sprites.add(enemy)
            grid[i][j] = Cell.CellClass(enemy, (j, i))

def exit(props):
    sys.exit()