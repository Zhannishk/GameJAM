import pygame
from sys import exit
pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((1280, 800))
pygame.display.set_caption('SURVIVE')
clock = pygame.time.Clock()
game_active = False
start_time = 0
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

# Game name
test_font = pygame.font.Font('font/Pixeltype.ttf', 180)
game_name = test_font.render('SURVIVE', False, 'white')
game_name_rect = game_name.get_rect(midtop=(640, 30))

#start button
test_font = pygame.font.Font('font/Pixeltype.ttf', 100)
start_button = test_font.render('Start the game', False, 'white')
start_button_rect = start_button.get_rect(midbottom=(900, 625))

#select player button
test_font = pygame.font.Font('font/Pixeltype.ttf', 60)
select_player = test_font.render('Select player', False, 'white')
select_player_rect = select_player.get_rect(center=(280, 650))

#ROOM background
room_boy = pygame.image.load('background/room_b.png')
room_boy = pygame.transform.scale_by(room_boy, (16,16))
room_boy_rect = room_boy.get_rect(center=(640,400))

room_girl = pygame.image.load('background/room_g.png')
room_girl = pygame.transform.scale_by(room_girl, (16,16))
room_girl_rect = room_girl.get_rect(center=(640,400))

#ROOM background game
room_b_bed = pygame.image.load('background/room_b_bed.png')
room_b_bed = pygame.transform.scale_by(room_b_bed, (15,15))
room_b_bed_rect = room_b_bed.get_rect(center=(640,400))
room_g_bed = pygame.image.load('background/room_g_bed.png')
room_g_bed = pygame.transform.scale_by(room_g_bed, (15,15))
room_g_bed_rect = room_g_bed.get_rect(center=(640,400))
#all sounds
user_select = pygame.mixer.Sound('sounds/user_select.mp3')
start = pygame.mixer.Sound('sounds/start.mp3')

#Defolt player
player = boy
player_rect = boy_rect
room = room_boy
room_rect = room_boy_rect

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    if pygame.mouse.get_pressed()[0] and start_button_rect.collidepoint(pygame.mouse.get_pos()):
        start.play()
        game_active = True

    if pygame.mouse.get_pressed()[0] and boy_rect.collidepoint(pygame.mouse.get_pos()):
        arrow_rect = arrow.get_rect(midbottom=(180, 310))
        user_select.play()
        player = boy
        player_rect = boy_rect
        room = room_boy
        room_rect = room_boy_rect

    if pygame.mouse.get_pressed()[0] and girl_rect.collidepoint(pygame.mouse.get_pos()):
        arrow_rect = arrow.get_rect(midbottom=(380, 310))
        user_select.play()
        player = girl
        player_rect = girl_rect
        room = room_girl
        room_rect = room_girl_rect


    if game_active:
        screen.fill('black')
        screen.blit(room, room_rect)

    else:
        screen.fill((3, 42, 56))
        screen.blit(game_name, game_name_rect)
        screen.blit(start_button, start_button_rect)
        screen.blit(select_player, select_player_rect)
        screen.blit(boy, boy_rect)
        screen.blit(girl, girl_rect)
        screen.blit(arrow, arrow_rect)





    pygame.display.update()
    clock.tick(60)