import pygame
import random
from library.tile import tile

FPS = 60
#
MAP_WIDTH = int(input("Input the map's width: "))
MAP_HEIGHT = int(input("Input the map's height: "))
TILE_SIZE = int(input("Input the tile's size: "))
#
WIDTH = TILE_SIZE * MAP_WIDTH
HEIGHT = TILE_SIZE * MAP_HEIGHT

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wave Function Collapse")
clock = pygame.time.Clock()
tile_list = []

def clamp_add(value, additives, modulo):
    return (value % modulo + additives % modulo) % modulo

def clamp_sub(value, subtractives, modulo):
    return ((value % modulo) + modulo - (subtractives % modulo)) % modulo

for i in range(MAP_HEIGHT):
    tile_list.append([])
    for j in range(MAP_WIDTH):
        tile_list[i].append(tile(0, TILE_SIZE))

def get_random_lowest_entropy():
    lowest = 2**64
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            e = tile_list[y][x].get_entropy()
            if tile_list[y][x].collapsed == False and e < lowest:
                lowest = e
    list_of_lowest = []
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            if tile_list[y][x].collapsed == False and tile_list[y][x].get_entropy() == lowest:
                list_of_lowest.append((x, y))
    if len(list_of_lowest) == 0:
        return False
    return random.choice(list_of_lowest)
    
def get_new_position(x, y, b):
    if b == 0:
        return x, clamp_sub(y, 1, MAP_HEIGHT)
    if b == 1:
        return clamp_add(x, 1, MAP_WIDTH), y
    if b == 2:
        return x, clamp_add(y, 1, MAP_HEIGHT)
    if b == 3:
        return clamp_sub(x, 1, MAP_WIDTH), y

def collapse(x, y):
    tile_list[y][x].collapse()
    value = tile_list[y][x].tile
    for i in range(4): #up - right - down - left
        nx, ny = get_new_position(x, y, i)
        if (value & (1 << i)) > 0:
            tile_list[ny][nx].add_restriction(clamp_add(i, 2, 4), 1)
        else:
            tile_list[ny][nx].add_restriction(clamp_add(i, 2, 4), 0)

running = True
collapse_timer = 0
max_collapse_timer = 0
while running:
    dt = clock.tick(FPS)/1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)
    for i in range(MAP_HEIGHT):
        for j in range(MAP_WIDTH):
            image, rect = tile_list[i][j].return_image()
            screen.blit(image, (TILE_SIZE * j, TILE_SIZE * i))
    ### Your code comes here

    if collapse_timer <= 0:
        curr = get_random_lowest_entropy()
        if curr == False:
            running = False
            break
        collapse(curr[0], curr[1])
        collapse_timer = max_collapse_timer
    else:
        collapse_timer -= dt

    ## Done after drawing everything to the screen
    pygame.display.flip()       

pygame.image.save(screen, "WFC.png")
pygame.quit()