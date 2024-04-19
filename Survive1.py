import pygame
import random
from sys import exit
pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((1280, 800))
pygame.display.set_caption('SURVIVE')
clock = pygame.time.Clock()
game_active = False
maze_active = False
show_rule_wake_up = False
start_time = 0
space_count = 0
pos = 700
change = 0
FPS = 60

#girl
girl = pygame.image.load('player/girl.png').convert_alpha()
girl = pygame.transform.scale(girl, (130, 312))
girl_rect = girl.get_rect(midbottom=(380, 625))

#boy
boy = pygame.image.load('player/boy.png').convert_alpha()
boy = pygame.transform.scale(boy, (130, 312))
boy_rect = boy.get_rect(midbottom=(180, 625))

#arrow
arrow = pygame.image.load('arrow.png').convert_alpha()
arrow = pygame.transform.scale(arrow, (70, 80))
arrow_rect = arrow.get_rect(midbottom=(180, 310))

# menu
menu_bg = pygame.image.load('background/bricks.png')
menu_bg = pygame.transform.scale_by(menu_bg, (10,10))
menu_bg_rect = menu_bg.get_rect()
# Game name
test_font = pygame.font.Font('font/Pixeltype.ttf', 200)
game_name = test_font.render('SURVIVE', False, 'black')
game_name_rect = game_name.get_rect(midtop=(645, 35))
game_name_yellow = test_font.render('SURVIVE', False, 'yellow')
game_name_yellow_rect = game_name_yellow.get_rect(midtop=(640, 30))

#rules
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
rule_wake_up = test_font.render('press SPACE 3 times to wake up and go to the door', False, 'black', 'white')
rule_wake_up_rect = rule_wake_up.get_rect(center=(640, 200))

#start button
start_button = pygame.image.load('buttons/button_start.png')
start_button = pygame.transform.scale_by(start_button, (5,5))
start_button_rect = start_button.get_rect(midbottom=(900, 625))

#select player button
test_font = pygame.font.Font('font/Pixeltype.ttf', 60)
select_player = test_font.render('Select player', False, 'white')
select_player_rect = select_player.get_rect(center=(280, 650))

#ROOM background
room_boy = pygame.image.load('background/room_b.png')
room_boy = pygame.transform.scale_by(room_boy, (20,17))
room_boy_rect = room_boy.get_rect(center=(640,400))

room_girl = pygame.image.load('background/room_g.png')
room_girl = pygame.transform.scale_by(room_girl, (20,17))
room_girl_rect = room_girl.get_rect(center=(640,400))

#ROOM background game
room_b_bed = pygame.image.load('background/room_b_bed.png')
room_b_bed = pygame.transform.scale_by(room_b_bed, (20,17))
room_b_bed_rect = room_b_bed.get_rect(center=(640,400))
room_g_bed = pygame.image.load('background/room_g_bed.png')
room_g_bed = pygame.transform.scale_by(room_g_bed, (20,17))
room_g_bed_rect = room_g_bed.get_rect(center=(640,400))

# doors
door = pygame.image.load('door/closed_door.png')
door = pygame.transform.scale_by(door, (12, 12))
door_rect = door.get_rect(center=(200, 417))
half_open_door = pygame.image.load('door/half_open_door.png')
half_open_door = pygame.transform.scale_by(half_open_door, (12, 12))

#all sounds
user_select = pygame.mixer.Sound('sounds/user_select.wav')
start = pygame.mixer.Sound('sounds/start.mp3')
main_menu_music = pygame.mixer.Sound('sounds/main-menu.mp3')

#Defolt player
player = boy
player_rect = boy_rect
room = room_boy
room_rect = room_boy_rect
room_bed = room_b_bed
room_bed_rect = room_b_bed_rect

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                space_count += 1
                if door_rect.colliderect(player_rect):
                    maze_active = True
                if space_count >= 1:  # Check if space key pressed 5 times
                    game_active = True
                    show_rule_wake_up = False
                    room = room_bed
                    room_rect = room_bed_rect

            if event.key == pygame.K_LEFT:
                change -= 10
            if event.key == pygame.K_RIGHT:
                change += 10

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                change = 0

    pos += change
    pos = max(0, min(pos, 1100))
    player_rect = pygame.Rect(pos, 250, player.get_width() * 1.3, player.get_height() * 1.3)

    if door_rect.colliderect(player_rect):
        door = half_open_door

    if game_active:
        main_menu_music.stop()
        start_time += 1
        screen.fill('black')
        screen.blit(room, room_rect)
        screen.blit(door, door_rect)
        if start_time >= 1000:
            show_rule_wake_up = True
        if show_rule_wake_up:
            screen.blit(rule_wake_up, rule_wake_up_rect)
        if space_count >= 1:
            screen.blit(pygame.transform.scale_by(player, (1.3,1.3)), (pos, 250))

        if maze_active:
            screen.fill('black')

    else:
        if not main_menu_music.get_num_channels():
            main_menu_music.play(loops=-1)
        screen.blit(menu_bg, menu_bg_rect)
        screen.blit(game_name, game_name_rect)
        screen.blit(game_name_yellow, game_name_yellow_rect)
        screen.blit(start_button, start_button_rect)
        screen.blit(select_player, select_player_rect)
        screen.blit(boy, boy_rect)
        screen.blit(girl, girl_rect)
        screen.blit(arrow, arrow_rect)

        if pygame.mouse.get_pressed()[0]:
            if not mouse_pressed:
                if start_button_rect.collidepoint(pygame.mouse.get_pos()):
                    start.play()
                    game_active = True

                # selecting player
                if boy_rect.collidepoint(pygame.mouse.get_pos()):
                    arrow_rect = arrow.get_rect(midbottom=(180, 310))
                    user_select.play()
                    player = boy
                    player_rect = boy_rect
                    room = room_boy
                    room_rect = room_boy_rect
                    room_bed = room_b_bed
                    room_bed_rect = room_b_bed_rect

                if girl_rect.collidepoint(pygame.mouse.get_pos()):
                    arrow_rect = arrow.get_rect(midbottom=(380, 310))
                    user_select.play()
                    player = girl
                    player_rect = girl_rect
                    room = room_girl
                    room_rect = room_girl_rect
                    room_bed = room_g_bed
                    room_bed_rect = room_g_bed_rect
            mouse_pressed = True
        else:
            mouse_pressed = False

    pygame.display.update()
    clock.tick(60)
