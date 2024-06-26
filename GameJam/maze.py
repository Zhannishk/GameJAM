from cell import Cell
import random

class Maze:
    def __init__(self, cols, rows):
        self.cols = cols
        self.rows = rows
        self.thickness = 12
        self.grid_cells = [Cell(col, row, self.thickness) for row in range(self.rows) for col in range(self.cols)]
        stuffs = ['stuffs/burger', 'stuffs/bottle', 'stuffs/medicine']
        for stuff in stuffs:
            cell = random.choice(self.grid_cells)
            cell.set_stuff(stuff)

    def remove_walls(self, current, nextt):
        dx = current.x - nextt.x
        if dx == 1:
            current.walls['left'] = False
            nextt.walls['right'] = False
        elif dx == -1:
            current.walls['right'] = False
            nextt.walls['left'] = False
        dy = current.y - nextt.y
        if dy == 1:
            current.walls['top'] = False
            nextt.walls['bottom'] = False
        elif dy == -1:
            current.walls['bottom'] = False
            nextt.walls['top'] = False

    def generate_maze(self):
        current_cell = self.grid_cells[0]
        array = []
        break_count = 1
        while break_count != len(self.grid_cells):
            current_cell.visited = True
            next_cell = current_cell.check_neighbors(self.cols, self.rows, self.grid_cells)
            if next_cell:
                next_cell.visited = True
                break_count += 1
                array.append(current_cell)
                self.remove_walls(current_cell, next_cell)
                current_cell = next_cell
            elif array:
                current_cell = array.pop()
        return self.grid_cells
