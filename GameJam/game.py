import pygame

pygame.font.init()


class Game:
    def __init__(self, goal_cell, tile):
        self.font = pygame.font.Font('font/Pixeltype.ttf', 100)
        self.message_color = pygame.Color("red")
        self.goal_cell = goal_cell
        self.tile = tile

    # add goal point for player to reach
    def add_goal_point(self, screen):
        # adding gate for the goal point
        img = pygame.image.load("door/closed_door.png")
        img = pygame.transform.scale(img, (self.tile, self.tile))
        screen.blit(img, (self.goal_cell.x * self.tile, self.goal_cell.y * self.tile))

    # winning message
    def message(self):
        msg = self.font.render('You survived !', True, self.message_color, 'white')
        return msg

    # checks if player reached the goal point
    def is_game_over(self, player):
        goal_cell_abs_x, goal_cell_abs_y = self.goal_cell.x * self.tile, self.goal_cell.y * self.tile
        if player.x >= goal_cell_abs_x and player.y >= goal_cell_abs_y:
            return True
        else:
            return False
