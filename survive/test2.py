import pygame
import sys
from maze import Maze
from player import Player
from game import Game
from clock import Clock

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 800
FPS = 60
TILE_SIZE = 100

# Setup Screen and Clock
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('SURVIVE')
clock = pygame.time.Clock()

# Game State Variables
game_active = False
maze_active = False
menu_active = True
show_rule_wake_up = False
space_count = 0
start_time = 0

# Player Movement Variables
player_pos_x = 700
player_speed = 10

# Load Assets
# Load images
girl_img = pygame.image.load('player/girl.png').convert_alpha()
girl_img = pygame.transform.scale(girl_img, (130, 312))

boy_img = pygame.image.load('player/boy.png').convert_alpha()
boy_img = pygame.transform.scale(boy_img, (130, 312))

arrow_img = pygame.image.load('buttons/arrow.png').convert_alpha()
arrow_img = pygame.transform.scale(arrow_img, (70, 80))

# Menu
menu_bg = pygame.image.load('background/bricks.png')
menu_bg = pygame.transform.scale_by(menu_bg, (10, 10))
menu_bg_rect = menu_bg.get_rect()
game_name_font = pygame.font.Font('font/Pixeltype.ttf', 200)
game_name = game_name_font.render('SURVIVE', False, 'black')
game_name_rect = game_name.get_rect(midtop=(645, 35))
game_name_yellow = game_name_font.render('SURVIVE', False, 'yellow')
game_name_yellow_rect = game_name_yellow.get_rect(midtop=(640, 30))

# Rules
rules_font = pygame.font.Font('font/Pixeltype.ttf', 50)
rule_wake_up = rules_font.render('Press SPACE 3 times to wake up and go to the door', False, 'black', 'white')
rule_wake_up_rect = rule_wake_up.get_rect(center=(640, 200))

# Start Button
start_button_img = pygame.image.load('buttons/button_start.png')
start_button_img = pygame.transform.scale_by(start_button_img, (5, 5))
start_button_rect = start_button_img.get_rect(midbottom=(900, 625))

# Select Player Text
select_player_font = pygame.font.Font('font/Pixeltype.ttf', 60)
select_player_text = select_player_font.render('Select Player', False, 'white')
select_player_text_rect = select_player_text.get_rect(center=(280, 650))

# Room backgrounds
room_boy_img = pygame.image.load('background/room_b.png')
room_boy_img = pygame.transform.scale_by(room_boy_img, (20, 17))
room_boy_img_rect = room_boy_img.get_rect(center=(640, 400))

room_girl_img = pygame.image.load('background/room_g.png')
room_girl_img = pygame.transform.scale_by(room_girl_img, (20, 17))
room_girl_img_rect = room_girl_img.get_rect(center=(640, 400))

room_bed_boy_img = pygame.image.load('background/room_b_bed.png')
room_bed_boy_img = pygame.transform.scale_by(room_bed_boy_img, (20, 17))
room_bed_boy_img_rect = room_bed_boy_img.get_rect(center=(640, 400))

room_bed_girl_img = pygame.image.load('background/room_g_bed.png')
room_bed_girl_img = pygame.transform.scale_by(room_bed_girl_img, (20, 17))
room_bed_girl_img_rect = room_bed_girl_img.get_rect(center=(640, 400))

# Door images
door_closed_img = pygame.image.load('door/closed_door.png')
door_closed_img = pygame.transform.scale_by(door_closed_img, (12, 12))
door_closed_rect = door_closed_img.get_rect(center=(200, 417))

door_half_open_img = pygame.image.load('door/half_open_door.png')
door_half_open_img = pygame.transform.scale_by(door_half_open_img, (12, 12))

# Sounds
user_select_sound = pygame.mixer.Sound('sounds/user_select.wav')
start_sound = pygame.mixer.Sound('sounds/start.mp3')
main_menu_music = pygame.mixer.Sound('sounds/main-menu.mp3')

# Default player and room setup
player_img = boy_img
player_rect = boy_img.get_rect(midbottom=(180, 625))
room_img = room_boy_img
room_rect = room_boy_img_rect
room_bed_img = room_bed_boy_img
room_bed_rect = room_bed_boy_img_rect
arrow_rect = arrow_img.get_rect(midbottom=(180, 310))


# Helper Functions
def reset_game():
    global game_active, maze_active, show_rule_wake_up, space_count, start_time
    game_active = False
    maze_active = False
    show_rule_wake_up = False
    space_count = 0
    start_time = 0


def handle_keydown(event):
    global space_count, player_pos_x, game_active, maze_active
    if event.key == pygame.K_SPACE:
        space_count += 1
        if door_closed_rect.colliderect(player_rect):
            maze_active = True
        if space_count >= 3:
            game_active = True
            show_rule_wake_up = False
            screen.blit(room_bed_img, room_bed_rect)

    if event.key == pygame.K_LEFT:
        player_pos_x -= player_speed
    elif event.key == pygame.K_RIGHT:
        player_pos_x += player_speed
    player_pos_x = max(0, min(player_pos_x, 1100))
    player_rect = pygame.Rect(player_pos_x, 250, player_img.get_width(), player_img.get_height())


# Main Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            handle_keydown(event)

    # Game State Handling
    if game_active:
        # Stop menu music and play start sound
        main_menu_music.stop()
        start_time += 1
        screen.fill('black')
        screen.blit(room_bed_img, room_bed_rect)
        screen.blit(door_closed_img, door_closed_rect)
        if start_time >= 1000:
            show_rule_wake_up = True
        if show_rule_wake_up:
            screen.blit(rule_wake_up, rule_wake_up_rect)
        if space_count >= 3:
            screen.blit(pygame.transform.scale_by(player_img, (1.3, 1.3)), (player_pos_x, 250))

        # Handle Maze Activation
        if maze_active:
            maze = Maze(SCREEN_WIDTH // TILE_SIZE, SCREEN_HEIGHT // TILE_SIZE)
            game = Game(maze.grid_cells[-1], TILE_SIZE)
            player = Player(TILE_SIZE // 3, TILE_SIZE // 3)
            clock = Clock()
            maze.generate_maze()
            clock.start_timer()

            # Running the Maze
            while maze_active:
                screen.fill("white")
                screen.fill(pygame.Color("black"), (1100, 0, 800, 800))

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                # Handle keydown events
                if event.type == pygame.KEYDOWN:
                    if not game.is_game_over(player):
                        if event.key == pygame.K_LEFT:
                            player.left_pressed = True
                        elif event.key == pygame.K_RIGHT:
                            player.right_pressed = True
                        elif event.key == pygame.K_UP:
                            player.up_pressed = True
                        elif event.key == pygame.K_DOWN:
                            player.down_pressed = True
                        player.check_move(TILE_SIZE, maze.grid_cells, maze.thickness)

                # Handle keyup events
                if event.type == pygame.KEYUP:
                    if not game.is_game_over(player):
                        if event.key == pygame.K_LEFT:
                            player.left_pressed = False
                        elif event.key == pygame.K_RIGHT:
                            player.right_pressed = False
                        elif event.key == pygame.K_UP:
                            player.up_pressed = False
                        elif event.key == pygame.K_DOWN:
                            player.down_pressed = False
                        player.check_move(TILE_SIZE, maze.grid_cells, maze.thickness)

                # Check game over
                if game.is_game_over(player):
                    maze_active = False
                    game_active = False

                # Draw the maze and game elements
                game.draw_maze(screen, maze, player, clock)

                clock.tick(FPS)

    else:
        # Menu state handling
        if not main_menu_music.get_num_channels():
            main_menu_music.play(loops=-1)

        # Displaying menu background and elements
        screen.blit(menu_bg, menu_bg_rect)
        screen.blit(game_name, game_name_rect)
        screen.blit(game_name_yellow, game_name_yellow_rect)
        screen.blit(start_button_img, start_button_rect)
        screen.blit(select_player_text, select_player_text_rect)
        screen.blit(player_img, player_rect)
        screen.blit(room_img, room_rect)
        screen.blit(arrow_img, arrow_rect)

        # Handling menu button clicks
        mouse_pos = pygame.mouse.get_pos()
        if start_button_rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                game_active = True
                maze_active = False
                reset_game()
                user_select_sound.play()
                start_sound.play()

        # Handling player selection
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_img = girl_img
                room_img = room_girl_img
                room_bed_img = room_bed_girl_img
                user_select_sound.play()
            elif event.key == pygame.K_RIGHT:
                player_img = boy_img
                room_img = room_boy_img
                room_bed_img = room_bed_boy_img
                user_select_sound.play()

    pygame.display.update()
    clock.tick(FPS)
