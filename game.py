import pygame
import sys
from os.path import join
import Maze_genrator as mg
from pg_buttons import Buttons as Btn
import csv

# initilizing pygame
pygame.init()

# defining Global variables
WIDTH , HEIGHT = 1400, 920
FPS = 60
PLAYER_VEL = 7
PLAYER_NAME = "Jasper Stone"
Visibility = 250
player_health = 3
Score = 0
Font = pygame.font.Font(join("Assets","Font","font.ttf"),50)
Music_play = True
Animation_speed = 0.4
frames_counter = 0
reset_timer = 0
clock = pygame.time.Clock()
music_go = pygame.mixer.Sound(join("Assets","Music","go.mp3"))

# Checking if argument is passed or not for music
if (len(sys.argv)-1) > 0:
    sound = sys.argv[1]
    Music = pygame.mixer.Sound(join("Assets","Music",sound))
else:
    Music = pygame.mixer.Sound(join("Assets","Music","Sound_bg.mp3"))

# creating window / screen
window = pygame.display.set_mode((WIDTH,HEIGHT))

# creating function to load sprite sheets
def Load_sprite(sheet,width,hight):
    sprites = []
    sprite_width, sprite_hight = sheet.get_size()
    for y in range(0, sprite_hight, hight):
        for x in range(0, sprite_width, width):
            sprite = sheet.subsurface(pygame.Rect(x, y, width, hight))
            sprites.append(sprite)

    return sprites

# Player Sprite Class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height,ply_movements):
        self.rect = pygame.Rect(x, y, width, height)
        self.vel_x = 0
        self.vel_y = 0
        self.Mask = None
        self.Direction = "left"
        self.Move_animation = ply_movements
        self.current_frame = 0
    
    def Animate(self,sprites):
        self.current_frame += Animation_speed
        if self.current_frame >= len(sprites):
            self.current_frame = 0
        window.blit(sprites[int(self.current_frame)],self.rect)

    def Movement(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def Move_left(self, vel):
        self.vel_x = -vel
        if self.Direction != "left":
            self.Direction = "left"

    def Move_right(self, vel):
        self.vel_x = vel
        if self.Direction != "right":
            self.Direction = "right"

    def Move_forward(self, vel):
        self.vel_y = -vel
        if self.Direction != "forward":
            self.Direction = "forward"

    def Move_backward(self, vel):
        self.vel_y = vel
        if self.Direction != "backward":
            self.Direction = "backward"
    
    def Draw (self,window):
        keys = pygame.key.get_pressed()
        if self.Direction == "left":
            if keys[pygame.K_a]:
                self.Animate(self.Move_animation[0])
            else:
                window.blit(self.Move_animation[0][4],self.rect)
        
        if self.Direction == "right":
            if keys[pygame.K_d]:
                self.Animate(self.Move_animation[1])
            else:
                window.blit(self.Move_animation[1][4],self.rect)

        if self.Direction == "forward":
            if keys[pygame.K_w]:
                self.Animate(self.Move_animation[2])
            else:
                window.blit(self.Move_animation[2][4],self.rect)

        if self.Direction == "backward":
            if keys[pygame.K_s]:
                self.Animate(self.Move_animation[3])
            else:
                window.blit(self.Move_animation[3][5],self.rect)

# Function to control movements
def Movement_handler(player):
    keys = pygame.key.get_pressed()
    player.vel_x = 0
    player.vel_y = 0
    if keys[pygame.K_a]:
        player.Move_left(PLAYER_VEL)
        player.Movement(player.vel_x, player.vel_y)
    elif keys[pygame.K_d]:
        player.Move_right(PLAYER_VEL)
        player.Movement(player.vel_x, player.vel_y)
    elif keys[pygame.K_w]:
        player.Move_forward(PLAYER_VEL)
        player.Movement(player.vel_x, player.vel_y)
    elif keys[pygame.K_s]:
        player.Move_backward(PLAYER_VEL)
        player.Movement(player.vel_x, player.vel_y)

def Scorebord():
    global PLAYER_NAME
    global Score

    # Read existing scoreboard
    scoreboard = {}
    file_exists = False
    with open("Scorebord.csv", "r") as file:
        for line in file:
            name, score = line.strip().split(',')
            scoreboard[name] = int(score)
            file_exists = True

    # Update or add entry
    if PLAYER_NAME in scoreboard:
        if Score > scoreboard[PLAYER_NAME]:
            scoreboard[PLAYER_NAME] = Score
    else:
        scoreboard[PLAYER_NAME] = Score

    # Write back to the file
    with open("Scorebord.csv", "w") as file:
        if file_exists:
            for name, score in scoreboard.items():
                file.write(f"{name},{score}\n")
        else:
            # If file didn't exist, write the new entry directly
            file.write(f"{PLAYER_NAME},{Score}\n")

def get_sorted_score(csv_file):
    scoreboard = {}

    # Read the CSV file and populate the scoreboard dictionary
    with open(csv_file, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            name, score = row
            scoreboard[name] = int(score)

    # Sort players in descending order of scores
    sorted_players = sorted(scoreboard.items(), key=lambda item: item[1], reverse=True)

    # Create a dictionary with players sorted by score
    sorted_dict = {player[0]: player[1] for player in sorted_players}

    return sorted_dict

# Making the timer function
def Timer(time,lvl_score):
    global Score
    global player_health
    timer_font = pygame.font.Font(join("Assets","Font","font.ttf"),26)
    timer_surface = pygame.image.load(join("Assets","Others","Surface.png"))
    timer_surface = pygame.transform.rotozoom(timer_surface,0,0.65)
    timer_rect = timer_surface.get_rect(center=(1200,33))
    Current_time = time - ((int(pygame.time.get_ticks()/1000)) - reset_timer)
    time_text = timer_font.render(f"Time:{Current_time}",True,"#000000")
    current_rect = time_text.get_rect(center=(1200,33))
    if (Current_time == 0):
        player_health = 3
        Game_over(lvl_score)
    window.blit(timer_surface,timer_rect)
    window.blit(time_text,current_rect)


def Score_Handler(player,colt_maze, colt_block, colt_index):
    global Score
    scr_font = pygame.font.Font(join("Assets","Font","font.ttf"),26)
    bar = pygame.image.load(join("Assets","Others","Surface.png"))
    bar = pygame.transform.rotozoom(bar,0,0.65)
    bar_rect = bar.get_rect(center=(700,33))
    score_txt = scr_font.render(f"SCORE:{Score}",True,"#000000")
    # showing on the screen
    window.blit(bar,bar_rect)
    window.blit(score_txt,(600,20))
    # checking for collision with the gem
    for i in range(len(colt_block)):
            coll = colt_block[i]
            if coll.colliderect(player.rect):
                idx = colt_index[i]
                Score = Score + 1
                colt_maze[idx[0]][idx[1]] = 0
    return Score

def Powerup_handller(player,obj_maze,obj_block,obj_index):
    global player_health
    music_yeah = pygame.mixer.Sound(join("Assets","Music","yeah.mp3"))
    # checking for the collision
    for i in range(len(obj_block)):
        hert = obj_block[i]
        if hert.colliderect(player.rect):
            music_yeah.play()
            idx = obj_index[i]
            if (player_health < 4):
                player_health += 1
            obj_maze[idx[0]][idx[1]] = 0

# Function for Health and obstical
def Health_and_obstical(player,obs_maze,obs_block,obs_index,lvl_score):
    global Score
    global player_health
    music_hit = pygame.mixer.Sound(join("Assets","Music","hit.mp3"))
    bar = pygame.image.load(join("Assets","Others","Surface.png"))
    bar = pygame.transform.rotozoom(bar,0,0.65)
    bar_rect = bar.get_rect(center=(200,33))
    heart = pygame.image.load(join("Assets","Others","Heart.png"))
    heart = pygame.transform.rotozoom(heart,0,0.7)
    effect = pygame.image.load(join("Assets","Others","effect.png"))
    # checking for collision with the obsticle
    for i in range(len(obs_block)):
            obsti = obs_block[i]
            if obsti.colliderect(player.rect):
                music_hit.play()
                idx = obs_index[i]
                player_health = player_health - 1
                window.blit(effect,(obsti.x-100,obsti.y-90))
                obs_maze[idx[0]][idx[1]] = 0
    # Surface for the heart
    window.blit(bar,bar_rect)
    if (player_health >= 1):
        window.blit(heart,(100,5))
    if (player_health >= 2):
        window.blit(heart,(170,5))
    if (player_health >= 3):
        window.blit(heart,(240,5))
    if (player_health == 0):
        player_health = 3
        player.rect.x = 1295
        player.rect.y = 810
        Game_over(lvl_score)

def Path_cheatcode(window, path, cell_size):
    path_block = pygame.Surface((cell_size,cell_size))
    path_block.fill('Green')

    for row, col in path:
        window.blit(path_block, (col * cell_size, row * cell_size))


# Function to check Collision
def Check_collision(walls, player):
    for wall_rect in walls:
            if player.rect.colliderect(wall_rect):
                player.rect.x -= player.vel_x
                player.rect.y -= player.vel_y

# making backgroung function
def Make_background(name):
    image = pygame.image.load(join("Assets","Background",name))
    x,y,width,height = image.get_rect()
    tiles = []

    for i in range (WIDTH // width+1):
        for j in range (HEIGHT // height+1):
            position = (i * width, j * height)
            tiles.append(position)

    return tiles, image

# making function to draw background
def Draw_background(window,tiles,image):
    for tile in tiles:
        window.blit(image,tile)

# Function to draw Goal / end
def Draw_goal(window,name,width,height,zoom,cell_size, dx, dy):
    global frames_counter
    image = pygame.image.load(join("Assets","Goal",name)).convert_alpha()
    image = pygame.transform.rotozoom(image,0,zoom)
    imge_arr = Load_sprite(image,width,height)
    goal_rect = imge_arr[0].get_rect(topleft=((1 * cell_size) + dx, (1 * cell_size) + dy))
    # enter width and height after mutiplying it by zoom
    frames_counter += 0.5
    if frames_counter >= len(imge_arr):
        frames_counter = 0
    window.blit(imge_arr[int(frames_counter)],goal_rect)
    return goal_rect

#==========================================Importing Game Assets==============================================#
# function to import player assets
def player_impoter(scale, width, height):
    #importing main player sprites(right)
    harry_r = pygame.image.load(join("Assets","Player","links_r.png")).convert_alpha() #right
    harry_r = pygame.transform.rotozoom(harry_r,0,scale)
    harry_right = Load_sprite(harry_r,width,height)
    # (left)
    harry_l = pygame.image.load(join("Assets","Player","links_l.png")).convert_alpha() #left
    harry_l = pygame.transform.rotozoom(harry_l,0,scale)
    harry_left = Load_sprite(harry_l,width,height)
    # (forward)
    harry_f = pygame.image.load(join("Assets","Player","links_f.png")).convert_alpha() #forward
    harry_f = pygame.transform.rotozoom(harry_f,0,scale)
    harry_forward = Load_sprite(harry_f,width,height)
    # (backward)
    harry_b = pygame.image.load(join("Assets","Player","links_b.png")).convert_alpha() #backward
    harry_b = pygame.transform.rotozoom(harry_b,0,scale)
    harry_backward = Load_sprite(harry_b,width,height)
    # array of all the movements
    harry_movements = [harry_left,harry_right,harry_forward,harry_backward] #storing the player movement sheets in a list

    return harry_movements

# function importing maze walls
def import_wall(scale):
    wall = pygame.image.load(join("Assets","Obsticles","block.png")).convert_alpha()
    wall = pygame.transform.rotozoom(wall, 0, scale)  # Scale as needed 
    return wall

# function importing obsticles
def import_obsticles(scale):
    obst = pygame.image.load(join("Assets","Obsticles","spike_head.png")).convert_alpha()
    obst = pygame.transform.rotozoom(obst, 0, scale) 
    return obst

# function importing Gem
def import_gem(scale):
    Gem = pygame.image.load(join("Assets","Collatable","Gem.png")).convert_alpha()
    Gem = pygame.transform.rotozoom(Gem,0,scale) 
    return Gem

# function importing Heart Power up
def import_powerup(scale):
    powerup_heart = pygame.image.load(join("Assets","Others","Heart.png")).convert_alpha()
    powerup_heart = pygame.transform.rotozoom(powerup_heart,0,scale) 
    return powerup_heart

# (End Goal)
Goal_text = Font.render("PRESS ENTER TO CLEAR LEVEL", False, "#FFFFFF").convert()
#========================================================Game Assets=====================================================#

# Level 1
def Level_1():
    tiles , bg_image = Make_background("Purple.png")
    global reset_timer
    global Visibility
    pygame.display.set_caption("Labyrinth Leap (Level-1)")
    # Importing player assets
    harry_movements = player_impoter(0.4,40,40)
    # importing game assets
    wall = import_wall(0.8)
    obst = import_obsticles(1)
    Gem = import_gem(1)
    powerup_heart = import_powerup(0.6)
    # The main Player initilization
    player = Player(1295,810,25,35,harry_movements)
    # Define the radius and color for the visible circle
    visible_circle_radius = 250
    visible_circle_color = (0, 0, 0)  # White color for visibility circle
    # Create a surface for the visibility mask
    mask_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)  # Use SRCALPHA for transparency
    mask_color = (0, 0, 0, Visibility)  # Semi-ransparent black (adjust alpha as needed)
    # Maze for the game
    maze = mg.generate_maze(23,15)
    # Solution to the maze
    solution = mg.solve_maze(maze,13,21,1,1)
    # function to genrate the Solution.txt file
    mg.Genrate_soltxt(solution)
    # Maze with Powerups
    temp_sol = solution.copy()
    powerup_maze = mg.Powerup_maze(maze,temp_sol,3)
    # maze with the obsticles
    obs_maze = mg.obs_maze(powerup_maze,solution,23,15,0.2,1)
    #  maze with the Collatables
    collt_maze = mg.Collatable_maze(obs_maze,23,15,0.5)

    # Game Loop for level_1
    while True:
        clock.tick(FPS) #FPS Counter
        pygame.display.update() # Updateing the screen
        # Clear the mask surface with semi-transparent black
        mask_surface.fill(mask_color)
        # Clear the game screen with black
        window.fill((0, 0, 0))
        #drawing background
        Draw_background(window,tiles,bg_image)
        #drawing maze
        Walls = mg.Draw_maze(window,maze,wall,23,15,61)
        # drawing obsticals
        obsticles_block , obsticles_indx = mg.Draw_Obsticles(window,obs_maze,obst,23,15,61)
        # Drawing Collatables
        collect_block, collect_indx = mg.Draw_Collatable(window,collt_maze,Gem,23,15,61)
        # Drawing Powerups
        obj_block, obj_index = mg.Draw_powerup(window,powerup_maze,powerup_heart,23,15,61)
        # drawing the player in the window
        player.Draw(window)
        # for movement of the player
        Movement_handler(player)
        # checking collision with the walls
        Check_collision(Walls,player)
         # Draw the visible circle on the mask surface (fully transparent inside circle, opaque outside)
        pygame.draw.circle(mask_surface, (0, 0, 0, 0), player.rect.center, visible_circle_radius)
        # Blit the mask surface onto the game screen with the correct blending mode
        window.blit(mask_surface, (0, 0))
        # Draw the visible circle around the player
        pygame.draw.circle(window, visible_circle_color, player.rect.center, visible_circle_radius, width=3)
         #drwaing goal
        end = Draw_goal(window,"Pig (36x30).png",54,45,1.5,61,5,5) # enter width and height after mutiplying it by zoom
         # Score and collatable manager
        player_score = Score_Handler(player,collt_maze,collect_block,collect_indx)
        # Health and obstical dection
        Health_and_obstical(player,obs_maze,obsticles_block,obsticles_indx,player_score)
        # powerup handdler
        Powerup_handller(player, maze, obj_block, obj_index)
        # Timer
        Timer(100,player_score)
        # msg when collided
        if end.colliderect(player.rect):
            window.blit(Goal_text,(55,430))
        #Event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    global player_health
                    player_health = 3
                    player.rect.x = 1295
                    player.rect.y = 810
                    Menu_screen()
                if event.key == pygame.K_BACKQUOTE:
                    Path_cheatcode(window,solution,61)
                if end.colliderect(player.rect) and event.key == pygame.K_RETURN:
                    music_go.play()
                    reset_timer = int(pygame.time.get_ticks()/1000)
                    Level_2()

# Level 2
def Level_2():
    tiles , bg_image = Make_background("Blue.png")
    global reset_timer
    global Visibility
    pygame.display.set_caption("Labyrinth Leap (Level-2)")
    # Importing player assets
    harry_movements = player_impoter(0.4,40,40)
    # importing game assets
    wall = import_wall(0.73)
    obst = import_obsticles(0.95)
    Gem = import_gem(0.9)
    powerup_heart = import_powerup(0.6)
    # The main Player initilization
    player = Player(1360,810,24,34,harry_movements)
    # Define the radius and color for the visible circle
    visible_circle_radius = 200
    visible_circle_color = (0, 0, 0)  # White color for visibility circle
    # Create a surface for the visibility mask
    mask_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)  # Use SRCALPHA for transparency
    mask_color = (0, 0, 0, Visibility)  # Semi-ransparent black (adjust alpha as needed)
    # Maze for the game
    maze = mg.generate_maze(27,17)
    # Solution to the maze
    solution = mg.solve_maze(maze,15,25,1,1)
    # function to genrate the Solution.txt file
    mg.Genrate_soltxt(solution)
    # Maze with Powerups
    temp_sol = solution.copy()
    powerup_maze = mg.Powerup_maze(maze,temp_sol,2)
    # maze with the obsticles
    obs_maze = mg.obs_maze(powerup_maze,solution,27,17,0.2,2)
    #  maze with the Collatables
    collt_maze = mg.Collatable_maze(obs_maze,27,17,0.4)

    # Game Loop for level_1
    while True:
        clock.tick(FPS) #FPS Counter
        pygame.display.update() # Updateing the screen
        # Clear the mask surface with semi-transparent black
        mask_surface.fill(mask_color)
        # Clear the game screen with black
        window.fill((0, 0, 0))
        #drawing background
        Draw_background(window,tiles,bg_image)
        #drawing maze
        Walls = mg.Draw_maze(window,maze,wall,27,17,53.8)
        # drawing obsticals
        obsticles_block , obsticles_indx = mg.Draw_Obsticles(window,obs_maze,obst,27,17,53.8)
        # Drawing Collatables
        collect_block, collect_indx = mg.Draw_Collatable(window,collt_maze,Gem,27,17,53.8)
        # Drawing Powerups
        obj_block, obj_index = mg.Draw_powerup(window,powerup_maze,powerup_heart,27,17,53.8)
        # drawing the player in the window
        player.Draw(window)
        # for movement of the player
        Movement_handler(player)
        # checking collision with the walls
        Check_collision(Walls,player)
         # Draw the visible circle on the mask surface (fully transparent inside circle, opaque outside)
        pygame.draw.circle(mask_surface, (0, 0, 0, 0), player.rect.center, visible_circle_radius)
        # Blit the mask surface onto the game screen with the correct blending mode
        window.blit(mask_surface, (0, 0))
        # Draw the visible circle around the player
        pygame.draw.circle(window, visible_circle_color, player.rect.center, visible_circle_radius, width=3)
        #drwaing goal
        end = Draw_goal(window,"Bunny (34x44).png",34,44,1,53.8,10,5) # enter width and height after mutiplying it by zoomtj
         # Score and collatable manager
        player_score = Score_Handler(player,collt_maze,collect_block,collect_indx)
        # Health and obstical dection
        Health_and_obstical(player,obs_maze,obsticles_block,obsticles_indx,player_score)
        # powerup handdler
        Powerup_handller(player, maze, obj_block, obj_index)
        # Timer
        Timer(100,player_score)
        # msg when collided
        if end.colliderect(player.rect):
            window.blit(Goal_text,(55,430))
        #Event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    global player_health
                    player_health = 3
                    player.rect.x = 1360
                    player.rect.y = 810
                    Menu_screen()
                if event.key == pygame.K_BACKQUOTE:
                    Path_cheatcode(window,solution,53.8)
                if end.colliderect(player.rect) and event.key == pygame.K_RETURN:
                    music_go.play()
                    reset_timer = int(pygame.time.get_ticks()/1000)
                    Level_3()

# Level 3
def Level_3():
    tiles , bg_image = Make_background("Green.png")
    global reset_timer
    global Visibility
    pygame.display.set_caption("Labyrinth Leap (Level-3)")
    # Importing player assets
    harry_movements = player_impoter(0.4,40,40)
    # importing game assets
    wall = import_wall(0.63)
    obst = import_obsticles(0.8)
    Gem = import_gem(0.8)
    powerup_heart = import_powerup(0.45)
    # The main Player initilization
    player = Player(1340,875,23,33,harry_movements)
    # Define the radius and color for the visible circle
    visible_circle_radius = 170
    visible_circle_color = (0, 0, 0)  # White color for visibility circle
    # Create a surface for the visibility mask
    mask_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)  # Use SRCALPHA for transparency
    mask_color = (0, 0, 0, Visibility)  # Semi-ransparent black (adjust alpha as needed)
    # Maze for the game
    maze = mg.generate_maze(31,21)
    # Solution to the maze
    solution = mg.solve_maze(maze,19,29,1,1)
    # function to genrate the Solution.txt file
    mg.Genrate_soltxt(solution)
    # Maze with Powerups
    temp_sol = solution.copy()
    powerup_maze = mg.Powerup_maze(maze,temp_sol,2)
    # maze with the obsticles
    obs_maze = mg.obs_maze(powerup_maze,solution,31,21,0.4,3)
    #  maze with the Collatables
    collt_maze = mg.Collatable_maze(obs_maze,31,21,0.3)

    # Game Loop for level_1
    while True:
        clock.tick(FPS) #FPS Counter
        pygame.display.update() # Updateing the screen
        # Clear the mask surface with semi-transparent black
        mask_surface.fill(mask_color)
        # Clear the game screen with black
        window.fill((0, 0, 0))
        #drawing background
        Draw_background(window,tiles,bg_image)
        #drawing maze
        Walls = mg.Draw_maze(window,maze,wall,31,21,45.8)
        # drawing obsticals
        obsticles_block , obsticles_indx = mg.Draw_Obsticles(window,obs_maze,obst,31,21,45.8)
        # Drawing Collatables
        collect_block, collect_indx = mg.Draw_Collatable(window,collt_maze,Gem,31,21,45.8)
        # Drawing Powerups
        obj_block, obj_index = mg.Draw_powerup(window,powerup_maze,powerup_heart,31,21,45.8)
        # drawing the player in the window
        player.Draw(window)
        # for movement of the player
        Movement_handler(player)
        # checking collision with the walls
        Check_collision(Walls,player)
         # Draw the visible circle on the mask surface (fully transparent inside circle, opaque outside)
        pygame.draw.circle(mask_surface, (0, 0, 0, 0), player.rect.center, visible_circle_radius)
        # Blit the mask surface onto the game screen with the correct blending mode
        window.blit(mask_surface, (0, 0))
        # Draw the visible circle around the player
        pygame.draw.circle(window, visible_circle_color, player.rect.center, visible_circle_radius, width=3)
        #drwaing goal
        end = Draw_goal(window,"Chicken (32x34).png",32,34,1,45.8,10,5) # enter width and height after mutiplying it by zoomtj
         # Score and collatable manager
        player_score = Score_Handler(player,collt_maze,collect_block,collect_indx)
        # Health and obstical dection
        Health_and_obstical(player,obs_maze,obsticles_block,obsticles_indx,player_score)
        # powerup handdler
        Powerup_handller(player, maze, obj_block, obj_index)
        # Timer
        Timer(100,player_score)
        # msg when collided
        if end.colliderect(player.rect):
            window.blit(Goal_text,(55,430))
        #Event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    global player_health
                    player_health = 3
                    player.rect.x = 1340
                    player.rect.y = 875
                    Menu_screen()
                if event.key == pygame.K_BACKQUOTE:
                    Path_cheatcode(window,solution,45.8)
                if end.colliderect(player.rect) and event.key == pygame.K_RETURN:
                    music_go.play()
                    reset_timer = int(pygame.time.get_ticks()/1000)
                    Win_Screen()

# Level Danger
def Level_danger():
    tiles , bg_image = Make_background("Brown.png")
    global reset_timer
    global Visibility
    pygame.display.set_caption("Labyrinth Leap (Bonus Level)")
    # Importing player assets
    harry_movements = player_impoter(0.2,20,20)
    # importing game assets
    wall = import_wall(0.4)
    obst = import_obsticles(0.6)
    Gem = import_gem(0.6)
    powerup_heart = import_powerup(0.35)
    # The main Player initilization
    player = Player(1365,880,13,15,harry_movements)
    # Define the radius and color for the visible circle
    visible_circle_radius = 170
    visible_circle_color = (0, 0, 0)  # White color for visibility circle
    # Create a surface for the visibility mask
    mask_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)  # Use SRCALPHA for transparency
    mask_color = (0, 0, 0, Visibility)  # Semi-ransparent black (adjust alpha as needed)
    # Maze for the game
    maze = mg.generate_maze(47,31)
    # Solution to the maze
    solution = mg.solve_maze(maze,29,45,1,1)
    # function to genrate the Solution.txt file
    mg.Genrate_soltxt(solution)
    # Maze with Powerups
    temp_sol = solution.copy()
    powerup_maze = mg.Powerup_maze(maze,temp_sol,4)
    # maze with the obsticles
    obs_maze = mg.obs_maze(powerup_maze,solution,47,31,0.2,4)
    #  maze with the Collatables
    collt_maze = mg.Collatable_maze(obs_maze,47,31,0.4)

    # Game Loop for level_1
    while True:
        clock.tick(FPS) #FPS Counter
        pygame.display.update() # Updateing the screen
        # Clear the mask surface with semi-transparent black
        mask_surface.fill(mask_color)
        # Clear the game screen with black
        window.fill((0, 0, 0))
        #drawing background
        Draw_background(window,tiles,bg_image)
        #drawing maze
        Walls = mg.Draw_maze(window,maze,wall,47,31,30.3)
        # drawing obsticals
        obsticles_block , obsticles_indx = mg.Draw_Obsticles(window,obs_maze,obst,47,31,30.3,4,4)
        # Drawing Collatables
        collect_block, collect_indx = mg.Draw_Collatable(window,collt_maze,Gem,47,31,30.3,10,7)
        # Drawing Powerups
        obj_block, obj_index = mg.Draw_powerup(window,powerup_maze,powerup_heart,47,31,30.3,5,5)
        # drawing the player in the window
        player.Draw(window)
        # for movement of the player
        Movement_handler(player)
        # checking collision with the walls
        Check_collision(Walls,player)
         # Draw the visible circle on the mask surface (fully transparent inside circle, opaque outside)
        pygame.draw.circle(mask_surface, (0, 0, 0, 0), player.rect.center, visible_circle_radius)
        # Blit the mask surface onto the game screen with the correct blending mode
        window.blit(mask_surface, (0, 0))
        # Draw the visible circle around the player
        pygame.draw.circle(window, visible_circle_color, player.rect.center, visible_circle_radius, width=3)
        #drwaing goal
        end = Draw_goal(window,"Trunk (64x32).png",64,32,1,30.3,-15,0) # enter width and height after mutiplying it by zoomtj
         # Score and collatable manager
        player_score = Score_Handler(player,collt_maze,collect_block,collect_indx)
        # Health and obstical dection
        Health_and_obstical(player,obs_maze,obsticles_block,obsticles_indx,player_score)
        # powerup handdler
        Powerup_handller(player, maze, obj_block, obj_index)
        # Timer
        Timer(150,player_score)
        # msg when collided
        if end.colliderect(player.rect):
            window.blit(Goal_text,(55,430))
        #Event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    global player_health
                    player_health = 3
                    player.rect.x = 1365
                    player.rect.y = 880
                    Menu_screen()
                if event.key == pygame.K_BACKQUOTE:
                    Path_cheatcode(window,solution,30.3)
                if end.colliderect(player.rect) and event.key == pygame.K_RETURN:
                    music_go.play()
                    reset_timer = int(pygame.time.get_ticks()/1000)
                    Win_Screen()

# Screen Main Menu
def Menu_screen():
    global Music_play
    global PLAYER_NAME
    pygame.display.set_caption("Main Menu")
    Menu_background = pygame.image.load(join("Assets","Screens","menu_screen.jpg")).convert()
    button_img = pygame.image.load(join("Assets","Buttons","button.png")).convert_alpha()
    scr_img = pygame.image.load(join("Assets","Buttons","scr_btn.png")).convert_alpha()
    scr_img = pygame.transform.rotozoom(scr_img,0,0.7)
    music_img = pygame.image.load(join("Assets","Buttons","Music_BTN.png")).convert_alpha()
    music_img = pygame.transform.rotozoom(music_img,0,0.7)
    menu_text = Font.render("MAIN MENU",False,"#6AD4DD")
    menu_rect = menu_text.get_rect(center=(720,50))
    name_font = pygame.font.Font(join("Assets","Font","font.ttf"),30)
    name = name_font.render(PLAYER_NAME,True,"#FCFFE0")

    while True:
        pygame.display.update()
        window.blit(Menu_background, (0,0))
        Menu_mouse_pos = pygame.mouse.get_pos()

        Play_button = Btn(image=button_img, position=(720,250), text="PLAY")

        Levels_button = Btn(image=button_img, position=(720,500), text="LEVELS")

        Quit_button = Btn(image=button_img, position=(720,750), text="QUIT")

        score_bord_button = Btn(image=scr_img, position=(300,500), text="")

        music_button = Btn(image=music_img, position=(1120,500), text="")

        window.blit(name,(20,30))

        window.blit(menu_text,menu_rect)
        if Music_play:
            Music.set_volume(0.3)
            Music.play(loops = -1)
        else:
            Music.stop()

        for button in [Play_button, Levels_button, Quit_button, score_bord_button, music_button]:
            button.Hover_over(Menu_mouse_pos)
            button.update(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if Play_button.Check_input(Menu_mouse_pos):
                    global reset_timer
                    reset_timer = int(pygame.time.get_ticks()/1000)
                    Level_1()
                if Levels_button.Check_input(Menu_mouse_pos):
                    reset_timer = int(pygame.time.get_ticks()/1000)
                    Levels()
                if Quit_button.Check_input(Menu_mouse_pos):
                    pygame.quit()
                    sys.exit()
                if score_bord_button.Check_input(Menu_mouse_pos):
                    reset_timer = int(pygame.time.get_ticks()/1000)
                    Scorebord_screen()
                if music_button.Check_input(Menu_mouse_pos):
                    if Music_play == True:
                        Music_play = False
                        music_img = pygame.image.load(join("Assets","Buttons","Musicoff_BTN.png")).convert_alpha()
                        music_img = pygame.transform.rotozoom(music_img,0,0.7)
                    else:
                        Music_play = True
                        music_img = pygame.image.load(join("Assets","Buttons","Music_BTN.png")).convert_alpha()
                        music_img = pygame.transform.rotozoom(music_img,0,0.7)

# Screen Levels
def Levels():
    global reset_timer
    pygame.display.set_caption("Levels")
    Levels_background = pygame.image.load(join("Assets","Screens","levels_screen.jpg")).convert()
    button_img = pygame.image.load(join("Assets","Buttons","button.png")).convert_alpha()
    button_img = pygame.transform.rotozoom(button_img,0,1.1)
    danger_img = pygame.image.load(join("Assets","Buttons","Skull.png")).convert_alpha()
    danger_img = pygame.transform.rotozoom(danger_img,0,2)
    back_img = pygame.image.load(join("Assets","Buttons","Back.png")).convert_alpha()
    back_img = pygame.transform.rotozoom(back_img,0,4)
    level_text = Font.render("CHOOSE A LEVEL TO PLAY",False,"#6AD4DD")
    level_rect = level_text.get_rect(center=(740,80))

    while True:
        pygame.display.update()
        window.blit(Levels_background, (0,0))
        lvl_mouse_pos = pygame.mouse.get_pos()

        lvl_1 = Btn(image=button_img, position=(200,450), text="LEVEL 1")

        lvl_2 = Btn(image=button_img, position=(700,450), text="LEVEL 2")

        lvl_3 = Btn(image=button_img, position=(1200,450), text="LEVEL 3")

        lvl_dngr = Btn(image=danger_img, position=(700,720), text="")

        back_button = Btn(image=back_img, position=(80,80), text="")

        window.blit(level_text,level_rect)

        for button in [lvl_1, lvl_2, lvl_3, lvl_dngr, back_button]:
            button.Hover_over(lvl_mouse_pos)
            button.update(window)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if lvl_1.Check_input(lvl_mouse_pos):
                    reset_timer = int(pygame.time.get_ticks()/1000)
                    Level_1()
                if lvl_2.Check_input(lvl_mouse_pos):
                    reset_timer = int(pygame.time.get_ticks()/1000)
                    Level_2()
                if lvl_3.Check_input(lvl_mouse_pos):
                    reset_timer = int(pygame.time.get_ticks()/1000)
                    Level_3()
                if lvl_dngr.Check_input(lvl_mouse_pos):
                    reset_timer = int(pygame.time.get_ticks()/1000)
                    Level_danger()
                if back_button.Check_input(lvl_mouse_pos):
                    reset_timer = int(pygame.time.get_ticks()/1000)
                    Menu_screen()

# Screen Scorebord
def Scorebord_screen():
    pygame.display.set_caption("Scoreborad")
    score_background = pygame.image.load(join("Assets","Screens","scorebord_screen.jpg")).convert()
    score_text = Font.render("SCOREBOARD",False,"#6AD4DD")
    score_rect = score_text.get_rect(center=(740,110))
    back_img = pygame.image.load(join("Assets","Buttons","Back.png")).convert_alpha()
    back_img = pygame.transform.rotozoom(back_img,0,4)
    score_dict = get_sorted_score("Scorebord.csv")
    plr_data = score_dict.items()
    plr_name = []
    scoreb = []
    for name,score in plr_data:
        plr_name.append(name)
        scoreb.append(score)

    ps1 = Font.render(f"{str(plr_name[0])} - {str(scoreb[0])}",True,"#FCFFE0")
    ps2 = Font.render(f"{str(plr_name[1])} - {str(scoreb[1])}",True,"#FCFFE0")
    ps3 = Font.render(f"{str(plr_name[2])} - {str(scoreb[2])}",True,"#FCFFE0")
    ps4 = Font.render(f"{str(plr_name[3])} - {str(scoreb[3])}",True,"#FCFFE0")
    ps5 = Font.render(f"{str(plr_name[4])} - {str(scoreb[4])}",True,"#FCFFE0")

    while True:
        pygame.display.update()
        scr_mouse_pos = pygame.mouse.get_pos()
        window.blit(score_background,(0,0))
        window.blit(score_text,score_rect)

        window.blit(ps1,(450,200))
        window.blit(ps2,(450,300))
        window.blit(ps3,(450,400))
        window.blit(ps4,(450,500))
        window.blit(ps5,(450,600))

        back_button = Btn(image=back_img, position=(80,110), text="")

        for button in [back_button]:
            button.update(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.Check_input(scr_mouse_pos):
                    Menu_screen()

# Screen Game over
def Game_over(lvl_score):
    global reset_timer
    global Score
    background = pygame.image.load(join("Assets","Screens","Game_Over.png"))
    score = Font.render(str(Score),True,"#FCFFE0")
    Scorebord()
    while True:
        pygame.display.update()
        window.blit(background,(0,0))
        window.blit(score,(630,750))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                Score = Score - lvl_score
                reset_timer = int(pygame.time.get_ticks()/1000)
                Menu_screen()

def Win_Screen():
    global PLAYER_NAME
    global Score
    Score =100
    background = pygame.image.load(join("Assets","Screens","Win_Screen.png"))
    p_name = Font.render(PLAYER_NAME,True,"#0C0C0C")
    name_rect = p_name.get_rect(center=(700,500))
    tfont = pygame.font.Font(join("Assets","Font","font.ttf"),27)
    text = tfont.render("Press Space For Main Menu OR Enter For Bouns Level",True,"#FCFFE0")
    scr = Font.render(f":{str(Score)}",True,"#000000")
    Scorebord()
    while True:
        pygame.display.update()
        window.blit(background,(0,0))
        window.blit(p_name,name_rect)
        window.blit(text,(20,850))
        window.blit(scr,(770,700))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                Menu_screen()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                Level_danger()

def Start_Game():
    global PLAYER_NAME
    pygame.display.set_caption("Labyrinth Leap")
    screen_background = pygame.image.load(join("Assets","Screens","Starting_screen.jpg"))
    startFont = pygame.font.Font(join("Assets","Font","font.ttf"),40)
    screen_text = startFont.render("What Is Your Name Adventurer",True,"#FCFFE0")
    write_font = pygame.font.Font(join("Assets","Font","font.ttf"),30)
    text_input = ""
    input_rect = pygame.Rect(200,500,300,50)
    boder = pygame.Rect(200,500,300,50)
    color = pygame.Color("#000000")
    bcolor = pygame.Color("#8DECB4")
    while True:
        pygame.display.flip()
        clock.tick(FPS) #FPS Counter
        # events loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    text_input = text_input[:-1]
                elif event.key == pygame.K_RETURN:
                    if (text_input != ""):
                        PLAYER_NAME = text_input
                        Menu_screen()
                    else:
                        Menu_screen()
                else:
                    text_input += event.unicode

        window.blit(screen_background,(0,0))
        window.blit(screen_text,(160,440))
        pygame.draw.rect(window,color,input_rect)
        pygame.draw.rect(window,bcolor,boder,3)
        input_surface = write_font.render(text_input,True,"#FCFFE0")
        window.blit(input_surface,(input_rect.x + 10, input_rect.y + 10))

        input_rect.w = max(300, input_surface.get_width()+20)
        boder.w = max(300, input_surface.get_width()+20)

Start_Game()