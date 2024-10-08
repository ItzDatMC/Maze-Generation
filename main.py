import pygame
import color
import numpy as np
import random
import sys
from collections import deque

sys.setrecursionlimit(20000)

pygame.init()

BLOCK = 20
BLOCK_WIDTH = 21
BLOCK_HEIGHT = 21
FIND_SHORTEST_PATH = True

WIDTH, HEIGHT = BLOCK*BLOCK_WIDTH, BLOCK*BLOCK_HEIGHT

WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Maze_Generation")
FPS = 60

arr_check = [[0 for _ in range(int(WIDTH/BLOCK)+5)] for _ in range(int(HEIGHT/BLOCK)+5)]

# Find the shortest path from cell (1,1) to the bottom right cell. The path will be highlighted in red.
def bfs():  
    
    for i in range(0, int(WIDTH/BLOCK)):
        for j in range(0, int(HEIGHT/BLOCK)):
            if arr_check[i][j] != 0:
                arr_check[i][j] = 2

    dx = [0, 0, 1, -1]
    dy = [1, -1, 0, 0]

    Queue = deque([(1, 1)])

    arr_par = [[(0, 0) for _ in range(int(WIDTH/BLOCK)+5)] for _ in range(int(HEIGHT/BLOCK)+5)]
    visited = [[False for _ in range(int(WIDTH/BLOCK)+5)] for _ in range(int(HEIGHT/BLOCK)+5)]

    visited[1][1] = True

    while len(Queue) > 0:
        x = Queue[0][0]
        y = Queue[0][1]
        Queue.popleft()

        for i in range(0, 4):
            x_ = x + dx[i]
            y_ = y + dy[i]
            if visited[x_][y_] == False and arr_check[x_][y_] == 2:
                Queue.append((x_,y_))
                visited[x_][y_] = True
                arr_par[x_][y_] = (x, y)

    x = int(WIDTH/BLOCK)-2
    y = int(HEIGHT/BLOCK)-2
    while x > 1 or y > 1:
        arr_check[x][y] = 1
        x, y = arr_par[x][y]
    
    arr_check[1][1] = 1



def create_table():
    for i in range(1, int(WIDTH/BLOCK)-1):
        for j in range(1, int(HEIGHT/BLOCK)-1):
            if i % 2 == 1 and j % 2 == 1:
                
                arr_check[i][j] = 1

def delete_wall(x, y, x_, y_):
    if x == x_:
        arr_check[x][int((y+y_)/2)] = 2
    else:
        arr_check[int((x+x_)/2)][y] = 2

def dfs(par_x, par_y, x, y):
    arr_d = [[0,2], [0, -2], [2, 0], [-2, 0]]
    check = True
    while check and len(arr_d) > 0:
        pos = random.randint(0, len(arr_d) - 1)
        x_ = x + arr_d[pos][0]
        y_ = y + arr_d[pos][1]
        if x_ > 0 and x_ < int(WIDTH/BLOCK)-1 and y_ > 0 and y_ < int(HEIGHT/BLOCK)-1 and arr_check[x_][y_] == 1:
            delete_wall(x, y, x_, y_)
            arr_check[x_][y_] = 2
            dfs(x, y, x_, y_)
            # check = False
        arr_d.pop(pos)

    

def draw_window():
    WIN.fill(color.BLACK)

def draw_grid():
    for i in range(0, int(WIDTH/BLOCK)):
        for j in range(0, int(HEIGHT/BLOCK)):
            x = i*BLOCK
            y = j*BLOCK
            if arr_check[i][j] == 0:
                pygame.draw.rect(WIN, color.BLACK, (x, y, BLOCK, BLOCK))
            elif arr_check[i][j] == 2:
                pygame.draw.rect(WIN, color.WHITE, (x, y, BLOCK, BLOCK))
            elif arr_check[i][j] == 1:
                pygame.draw.rect(WIN, color.GREEN, (x, y, BLOCK, BLOCK))
            else:
                pygame.draw.rect(WIN, color.BLUE, (x, y, BLOCK, BLOCK))

def sum_side_wall(x, y):
    sum = 0
    if arr_check[x+1][y] == 0 and arr_check[x-1][y] == 0 and arr_check[x][y+1] != 0 and arr_check[x][y-1] != 0:     
        return True
    if arr_check[x+1][y] != 0 and arr_check[x-1][y] != 0 and arr_check[x][y+1] == 0 and arr_check[x][y-1] == 0:     
        return True

def delete_random_wall(n):
    while n > 0:
        x = random.randint(1, int(WIDTH/BLOCK)-2)
        y = random.randint(1, int(HEIGHT/BLOCK)-2)
        if arr_check[x][y] == 0 and sum_side_wall(x,y):
            arr_check[x][y] = 1
            n -= 1


def maze_generation():
    create_table()
    arr_check[1][1] = 2
    dfs(1, 1, 1, 1)
    NUMBER_WALLS = random.randint(0,BLOCK_WIDTH)
    delete_random_wall(NUMBER_WALLS)
    if FIND_SHORTEST_PATH:
        bfs()

def main():
    maze_generation()
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        draw_window()

        draw_grid()
        
        pygame.display.flip()

    pygame.quit()

main()
