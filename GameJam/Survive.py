import pygame
import sys
from maze import Maze
from player import Player
from game import Game
from clock import Clock
from result import GameResult

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((1280, 800))
pygame.display.set_caption('SURVIVE')
clock = pygame.time.Clock()
game_active = False
maze_active = False
menu_active = True
show_rule_wake_up = False
final_window = False
game_result = GameResult()
start_time = 0
space_count = 0
pos = 700
change = 0
FPS = 60

# girl
girl = pygame.image.load('player/girl.png').convert_alpha()
girl = pygame.transform.scale(girl, (130, 312))
girl_rect = girl.get_rect(midbottom=(380, 625))
# boy
boy = pygame.image.load('player/boy.png').convert_alpha()
boy = pygame.transform.scale(boy, (130, 312))
boy_rect = boy.get_rect(midbottom=(180, 625))
# arrow
arrow = pygame.image.load('buttons/arrow.png').convert_alpha()
arrow = pygame.transform.scale(arrow, (70, 80))
arrow_rect = arrow.get_rect(midbottom=(180, 310))
# menu
menu_bg = pygame.image.load('background/bricks.png')
menu_bg = pygame.transform.scale_by(menu_bg, (10, 10))
menu_bg_rect = menu_bg.get_rect()
# Game name
test_font = pygame.font.Font('font/Pixeltype.ttf', 200)
game_name = test_font.render('SURVIVE', False, 'black')
game_name_rect = game_name.get_rect(midtop=(645, 35))
game_name_yellow = test_font.render('SURVIVE', False, 'yellow')
game_name_yellow_rect = game_name_yellow.get_rect(midtop=(640, 30))
# rules
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
rule_wake_up = test_font.render('press SPACE 3 times to wake up and go to the door', False, 'black', 'white')
rule_wake_up_rect = rule_wake_up.get_rect(center=(640, 200))
# start button
start_button = pygame.image.load('buttons/button_start.png')
start_button = pygame.transform.scale_by(start_button, (5, 5))
start_button_rect = start_button.get_rect(midbottom=(900, 625))
# select player button
test_font = pygame.font.Font('font/Pixeltype.ttf', 60)
select_player = test_font.render('Select player', False, 'white')
select_player_rect = select_player.get_rect(center=(280, 650))
# ROOM background
room_boy = pygame.image.load('background/room_b.png')
room_boy = pygame.transform.scale_by(room_boy, (20, 17))
room_boy_rect = room_boy.get_rect(center=(640, 400))
room_girl = pygame.image.load('background/room_g.png')
room_girl = pygame.transform.scale_by(room_girl, (20, 17))
room_girl_rect = room_girl.get_rect(center=(640, 400))
# ROOM background game
room_b_bed = pygame.image.load('background/room_b_bed.png')
room_b_bed = pygame.transform.scale_by(room_b_bed, (20, 17))
room_b_bed_rect = room_b_bed.get_rect(center=(640, 400))
room_g_bed = pygame.image.load('background/room_g_bed.png')
room_g_bed = pygame.transform.scale_by(room_g_bed, (20, 17))
room_g_bed_rect = room_g_bed.get_rect(center=(640, 400))
# Final window
win = pygame.image.load('background/win_end.png')
win = pygame.transform.scale(win, (1280, 800))
win_rect = win.get_rect()
lost = pygame.image.load('background/lost_end.png')
lost = pygame.transform.scale(lost, (1280, 800))
lost_rect = lost.get_rect()
# doors
door = pygame.image.load('door/closed_door.png')
door = pygame.transform.scale_by(door, (12, 12))
door_rect = door.get_rect(center=(200, 417))
half_open_door = pygame.image.load('door/half_open_door.png')
half_open_door = pygame.transform.scale_by(half_open_door, (12, 12))
# all sounds
user_select = pygame.mixer.Sound('sounds/user_select.wav')
siren = pygame.mixer.Sound('sounds/siren.mp3')
main_music = pygame.mixer.Sound('sounds/main-menu.mp3')
lullaby = pygame.mixer.Sound('sounds/lullaby.mp3')
lost_song = pygame.mixer.Sound('sounds/lost.mp3')
winny = pygame.mixer.Sound('sounds/winny.mp3')
#Defolt player
player_x = boy
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
        if event.type == pygame.KEYDOWN and not menu_active:
            if event.key == pygame.K_SPACE:
                space_count += 1
                if player_rect.colliderect(door_rect):
                    maze_active = True
                    siren.stop()
                if space_count >= 3:  # Check if space key pressed 3 times
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
    player_rect = pygame.Rect(pos, 250, player_x.get_width() * 1.3, player_x.get_height() * 1.3)

    if door_rect.colliderect(player_rect):
        door = half_open_door

    if game_active:
        main_music.stop()
        lullaby.play()
        start_time += 1
        screen.fill('black')
        screen.blit(room, room_rect)
        screen.blit(door, door_rect)
        if start_time >= 300:
            lullaby.stop()
            siren.play()
            show_rule_wake_up = True
        if show_rule_wake_up:
            screen.blit(rule_wake_up, rule_wake_up_rect)
        if space_count >= 3:
            show_rule_wake_up = False
            screen.blit(pygame.transform.scale_by(player_x, (1.3, 1.3)), (pos, 250))

        if maze_active:
            siren.stop()
            main_music.play()

            class Main():
                def __init__(self, screen):
                    self.screen = screen
                    self.font = pygame.font.SysFont("impact", 30)
                    self.message_color = pygame.Color("red")
                    self.running = True
                    self.game_over = False
                    self.FPS = pygame.time.Clock()

                def instructions(self):
                    instructions1 = self.font.render('Use', True, self.message_color)
                    instructions2 = self.font.render('Arrow Keys', True, self.message_color)
                    instructions3 = self.font.render('to Move', True, self.message_color)
                    self.screen.blit(instructions1, (1165, 300))
                    self.screen.blit(instructions2, (1120, 331))
                    self.screen.blit(instructions3, (1140, 362))

                def _draw(self, maze, tile, player, game, clock, stuffs):
                    # draw maze
                    [cell.draw(self.screen, tile) for cell in maze.grid_cells]
                    # add a goal point to reach
                    game.add_goal_point(self.screen)
                    # draw every player movement
                    player.draw(self.screen)
                    player.update()

                    stuff = player.got_stuff(tile, maze.grid_cells, screen)
                    if stuff:
                        stuffs.append(stuff)

                    # instructions, clock, winning message
                    self.instructions()
                    if self.game_over:
                        clock.stop_timer()
                        self.screen.blit(game.message(), (610, 120))
                        self.running = False
                    else:
                        clock.update_timer()
                    self.screen.blit(clock.display_timer(), (1130,430))

                    # display stuffs on top of the clock display
                    stuff_pos = 700
                    for stuff in stuffs:
                        self.screen.blit(pygame.image.load(f'{stuff}.png'), (1130, stuff_pos))
                        stuff_pos -= 50

                    pygame.display.flip()

                def main(self, frame_size, tile):
                    global event
                    cols, rows = frame_size[0] // tile, frame_size[-1] // tile
                    maze = Maze(cols, rows)
                    game = Game(maze.grid_cells[-1], tile)
                    player = Player(tile // 3, tile // 3)
                    clock = Clock()
                    stuffs = []
                    maze.generate_maze()
                    clock.start_timer()
                    while self.running:
                        self.screen.fill("white")
                        self.screen.fill(pygame.Color("black"), (1100, 0, 800, 800))
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()

                        # if keys were pressed still
                        if event.type == pygame.KEYDOWN:
                            if not self.game_over:
                                if event.key == pygame.K_LEFT:
                                    player.left_pressed = True
                                if event.key == pygame.K_RIGHT:
                                    player.right_pressed = True
                                if event.key == pygame.K_UP:
                                    player.up_pressed = True
                                if event.key == pygame.K_DOWN:
                                    player.down_pressed = True
                                player.check_move(tile, maze.grid_cells, maze.thickness, screen)
                        # if pressed key released
                        if event.type == pygame.KEYUP:
                            if not self.game_over:
                                if event.key == pygame.K_LEFT:
                                    player.left_pressed = False
                                if event.key == pygame.K_RIGHT:
                                    player.right_pressed = False
                                if event.key == pygame.K_UP:
                                    player.up_pressed = False
                                if event.key == pygame.K_DOWN:
                                    player.down_pressed = False
                                player.check_move(tile, maze.grid_cells, maze.thickness, screen)


                        if game.is_game_over(player):
                            game_result.set_won(True)
                            self.game_over = True
                            final_window = True
                            maze_active = False
                            player.left_pressed = False
                            player.right_pressed = False
                            player.up_pressed = False
                            player.down_pressed = False
                            self.running = False

                        if clock.start_time is None:
                            game_result.set_won(False)
                            self.game_over = True
                            final_window = True
                            maze_active = False
                            player.left_pressed = False
                            player.right_pressed = False
                            player.up_pressed = False
                            player.down_pressed = False
                            self.running = False
                        self._draw(maze, tile, player, game, clock, stuffs)
                        self.FPS.tick(60)


            if __name__ == "__main__":
                window_size = (1130, 800)
                screen = (window_size[0] + 150, window_size[-1])
                tile_size = 200
                screen = pygame.display.set_mode(screen)

                game = Main(screen)
                game.main((1130, 800), 110)
                final_window = True
                maze_active = False

        if final_window:
            if game_result.is_won:
                screen.blit(win, win_rect)
                screen.blit(player_x, player_rect)
                siren.stop()
                winny.play()
            else:
                screen.blit(lost, lost_rect)
                screen.blit(player_x, player_rect)
                siren.stop()
                lost_song.play()




    else:
        if not main_music.get_num_channels():
            main_music.play(loops=-1)
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
                    user_select.play()
                    game_active = True
                    menu_active = False

                # selecting player
                if boy_rect.collidepoint(pygame.mouse.get_pos()):
                    arrow_rect = arrow.get_rect(midbottom=(180, 310))
                    user_select.play()
                    player_x = boy
                    player_rect = boy_rect
                    room = room_boy
                    room_rect = room_boy_rect
                    room_bed = room_b_bed
                    room_bed_rect = room_b_bed_rect

                if girl_rect.collidepoint(pygame.mouse.get_pos()):
                    arrow_rect = arrow.get_rect(midbottom=(380, 310))
                    user_select.play()
                    player_x = girl
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
