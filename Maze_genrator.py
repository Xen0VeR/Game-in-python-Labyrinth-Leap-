import numpy as np
import random
import pygame

pygame.init()
# ===============================================Maze Genrator Algo================================================#
def generate_maze(width, height):
    # Initialize the maze with all walls as 1s
    maze = np.ones((height, width), dtype=np.int8)  
    # Start position (odd indices to ensure walls around paths)
    start_x, start_y = (1, 1)
    # Make the start a path initialy
    maze[start_y][start_x] = 0
    # Stack for backtracking
    stack = [(start_x, start_y)]
    # Possible movements: up, down, left, right
    directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]

    while stack:
        x, y = stack[-1]
        # Possible new moves
        possible_moves = []
        for dx, dy in directions:
            # Check if new position is inside the maze and is a wall
            if 0 <= x + dx < width and 0 <= y + dy < height and maze[y + dy][x + dx] == 1:
                possible_moves.append((dx, dy))
        
        if possible_moves:
            dx, dy = random.choice(possible_moves)
            # Knock down the wall and move to the new cell
            maze[y + dy // 2][x + dx // 2] = 0
            maze[y + dy][x + dx] = 0
            stack.append((x + dx, y + dy))
        else:
            # Backtrack if no moves are possible
            stack.pop()
    
    return maze
# ===============================================End of Maze Genrator Algo================================================#
# Draw the maze
def Draw_maze(window,maze,image,width,height,cell_size):
    objs = []
    for y in range(height):
        for x in range(width):
            if maze[y][x] == 1:
                image_rect = image.get_rect(topleft=(x * cell_size, y * cell_size))
                objs.append(image_rect)
                window.blit(image, image_rect)
    return objs

def obs_maze(maze,path,width,height,prob,num):
    temp_path = path.copy()
    for i in range(height):
        for j in range(width):
            if (i,j) not in path:
                if maze[i][j] != 1 and random.random() < prob:  # Adjust the probability of placing a wall as needed
                    maze[i][j] = 2
    for i in range(0,6):
        temp_path.pop()
        temp_path.pop(i)
    for i in range(0,num):
        x, y = random.choice(temp_path)
        maze[x][y] = 2

    return maze

def Collatable_maze(maze,width,height,prob):
    for i in range(height):
        for j in range(width):
            if maze[i][j] != 1 and maze[i][j] !=2 and maze[i][j] !=4 and  random.random() < prob:  # Adjust the probability of placing a wall as needed
                maze[i][j] = 3
    return maze

def Powerup_maze(maze,path,num):
    for i in range(0,6):
        path.pop()
        path.pop(i)
    for i in range(0,num):
        x, y = random.choice(path)
        maze[x][y] = 4
    return maze

def Draw_powerup(window,maze,image,width,height,cell_size,dx=10,dy=10):
    objs = []
    objs_indx = []
    for y in range(height):
        for x in range(width):
            if maze[y][x] == 4:
                image_rect = image.get_rect(topleft=((x * cell_size)+dx, (y * cell_size)+dy))
                objs.append(image_rect)
                objs_indx.append((y,x))
                window.blit(image, image_rect)
    return objs , objs_indx

def Draw_Obsticles(window,maze,image,width,height,cell_size,dx=10,dy=10):
    objs = []
    objs_indx = []
    for y in range(height):
        for x in range(width):
            if maze[y][x] == 2:
                image_rect = image.get_rect(topleft=((x * cell_size)+dx, (y * cell_size)+dy))
                objs.append(image_rect)
                objs_indx.append((y,x))
                window.blit(image, image_rect)
    return objs , objs_indx

def Draw_Collatable(window,maze,image,width,height,cell_size,dx=20,dy=15):
    objs = []
    objs_indx = []
    for y in range(height):
        for x in range(width):
            if maze[y][x] == 3:
                image_rect = image.get_rect(topleft=((x * cell_size)+dx, (y * cell_size)+dy))
                objs.append(image_rect)
                objs_indx.append((y,x))
                window.blit(image, image_rect)
    return objs , objs_indx

def Give_Direction(Path):
    modified_list = []
    # Modify the first element
    modified_list.append((Path[0][0], Path[0][1], "start"))
    # Iterate through the Path and add direction
    for i in range(len(Path) - 1):
        x, y = Path[i]
        next_x, next_y = Path[i + 1]
        
        if next_y < y:
            direction = "Left"
        elif next_y > y:
            direction = "Right"
        elif next_x < x:
            direction = "Up"
        elif next_x > x:
            direction = "Down"
        else:
            direction = "Unknown"
        
        modified_list.append((x, y, direction))
    # Modify the last element
    modified_list.append((Path[-1][0], Path[-1][1], "End"))
    return modified_list

def Genrate_soltxt(path):
    pathWithDirection = Give_Direction(path)
    with open ("Solution.txt", "w") as file:
        for data in pathWithDirection:
            file.write(str(data) + '\n')
# ========================================Maze solver code (Using DFS)========================================================#
def is_valid_move(maze, row, col, visited):
    # Check if the move is valid.
    num_rows = len(maze)
    num_cols = len(maze[0])
    return (0 <= row < num_rows) and (0 <= col < num_cols) and (maze[row][col] == 0) and not visited[row][col]

def dfs_util(maze, row, col, end_row, end_col, visited, path):
    # Utility function for DFS.
    if row == end_row and col == end_col:
        return True
    # Possible movements: up, down, left, right
    row_moves = [-1, 1, 0, 0]
    col_moves = [0, 0, -1, 1]

    for i in range(4):
        new_row = row + row_moves[i]
        new_col = col + col_moves[i]

        if is_valid_move(maze, new_row, new_col, visited):
            visited[new_row][new_col] = True
            path.append((new_row, new_col))

            if dfs_util(maze, new_row, new_col, end_row, end_col, visited, path):
                return True
            # Backtrack
            path.pop()

    return False

def solve_maze(maze, start_row, start_col, end_row, end_col):
    # Solve the maze using Depth-First Search.
    num_rows = len(maze)
    num_cols = len(maze[0])

    if start_row < 0 or start_row >= num_rows or start_col < 0 or start_col >= num_cols:
        raise ValueError("Start point is outside the maze.")

    if end_row < 0 or end_row >= num_rows or end_col < 0 or end_col >= num_cols:
        raise ValueError("End point is outside the maze.")

    visited = [[False] * num_cols for _ in range(num_rows)]
    path = [(start_row, start_col)]

    visited[start_row][start_col] = True

    if dfs_util(maze, start_row, start_col, end_row, end_col, visited, path):
        return path
    else:
        return None
# ================================================================End of maze Solver======================================================#