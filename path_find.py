import sys, pygame, tkinter, math, os
from square import Square
from node import Node

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

class PathFind:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Path Finder :)')
        self.screen = pygame.display.set_mode((800, 800))
        self.rows = 32
        self.columns = 32
        self.grid = []
        self.grid_squares = []
        self.start_i = 0
        self.start_j = 0
        self.end_i = 0
        self.end_j = 0
        self.barrier_i_j_nonunique = []
        self.barrier_i_j_unique = []
        self.open_list = []
        self.closed_list = set()
        self.start_flag = True
        self.end_flag = False
        self.barrier_flag = False
        self.go_flag = False
        self.f = 0
        self.g = 0
        self.h = 0
        self.screen.fill(black)

    def run_program(self):
        self.create_squares()
        self.draw_grid()
        while True:
            if self.start_flag or self.end_flag or self.barrier_flag:
                self._check_events()
                pygame.display.flip()
            else:
                break
        if self.go_flag:
            path = self.astar()
            self.draw_path(path)
        while True:
            self._check_events()
            pygame.display.flip()

    def draw_path(self, path):
        # print(path)
        for coordinate in path:
            if coordinate != (self.start_i, self.start_j):
                if coordinate != (self.end_i, self.end_j):
                    pygame.draw.rect(self.screen, blue, (self.grid_squares[coordinate[0]][coordinate[1]].x, self.grid_squares[coordinate[0]][coordinate[1]].y, self.grid_squares[0][0].width, self.grid_squares[0][0].width), 0)

    def create_squares(self):
        square = Square(0, 0)
        nboxes = 800 // square.width
        self.grid = [[0] * nboxes for n in range(nboxes)]
        self.grid_squares = [[0] * nboxes for n in range(nboxes)]
        for i in range(self.columns):
            for j in range(self.rows):
                    self.grid_squares[i][j] = Square(i*square.width, j*square.width)

    def draw_grid(self):
         for i in range(self.columns):
            for j in range(self.rows):
                pygame.draw.rect(self.screen, white, (self.grid_squares[i][j].x, self.grid_squares[i][j].y, self.grid_squares[i][j].width, self.grid_squares[i][j].width), 1)

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.start_flag or self.end_flag:
                    self._start_end()
            elif self.barrier_flag and pygame.mouse.get_pressed()[0]:
                self._barrier()

    def astar(self):
        for coordinate in self.barrier_i_j_unique:
            self.grid[coordinate[0]][coordinate[1]] = 1

        start_node = Node(None, (self.start_i, self.start_j))
        start_node.f = start_node.g = start_node.h = 0
        end_node = Node(None, (self.end_i, self.end_j))
        end_node.f = end_node.g = end_node.h = 0

        self.open_list.append(start_node)

        while len(self.open_list) > 0:
            current_node = self.open_list[0]
            current_index = 0
            for index, item in enumerate(self.open_list):
                if item.f < current_node.f:
                    current_node = item
                    current_index = index
            self.open_list.pop(current_index)
            self.closed_list.add(current_node)

            if current_node == end_node:
                path = []
                current = current_node
                while current is not None:
                    path.append(current.position)
                    current = current.parent
                return path[::-1]

            children = []
            for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:  # Adjacent squares
                node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

                if node_position[0] > (len(self.grid) - 1) or node_position[0] < 0 or node_position[1] > (len(self.grid[len(self.grid) - 1]) - 1) or node_position[1] < 0:
                    continue
                if self.grid[node_position[0]][node_position[1]] != 0:
                    continue

                new_node = Node(current_node, node_position)
                children.append(new_node)

            for child in children:
                if child in self.closed_list:
                    continue

                child.g = current_node.g + 1
                child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
                child.f = child.g + child.h

                for open_node in self.open_list:
                    if child == open_node and child.g > open_node.g:
                        continue

                self.open_list.append(child)


    def _barrier(self):
        pos = pygame.mouse.get_pos()
        for i in range(self.columns):
            for j in range(self.rows):
                if self.grid_squares[i][j].rect.collidepoint(pos):
                    self.barrier_i_j_nonunique.append((i, j))
                    for coordinate in self.barrier_i_j_nonunique:
                        if coordinate not in self.barrier_i_j_unique:
                            if (i, j) != (self.start_i, self.start_j):
                                if (i, j) != (self.end_i, self.end_j):
                                    self.barrier_i_j_unique.append((i, j))
                                    self.draw_barrier(i, j)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_q:
            pygame.quit()
            sys.exit()
        if event.key == pygame.K_SPACE:
            self.barrier_flag = False
            self.go_flag = True

    def _start_end(self):
        pos = pygame.mouse.get_pos()
        for i in range(self.columns):
            for j in range(self.rows):
                if self.start_flag:
                    if self.grid_squares[i][j].rect.collidepoint(pos):
                        self.start_i = i
                        self.start_j = j
                        self.start_point()
                        self.start_flag = False
                        self.end_flag = True
                elif self.end_flag:
                    if self.grid_squares[i][j].rect.collidepoint(pos):
                        self.end_i = i
                        self.end_j = j
                        self.end_point()
                        self.end_flag = False
                        self.barrier_flag = True

    def start_point(self):
        pygame.draw.rect(self.screen, green,
                          (self.grid_squares[self.start_i][self.start_j].x, self.grid_squares[self.start_i][self.start_j].y, self.grid_squares[self.start_i][self.start_j].width, self.grid_squares[self.start_i][self.start_j].width), 0)
    def end_point(self):
        pygame.draw.rect(self.screen, red,
                          (self.grid_squares[self.end_i][self.end_j].x, self.grid_squares[self.end_i][self.end_j].y, self.grid_squares[self.end_i][self.end_j].width, self.grid_squares[self.end_i][self.end_j].width), 0)

    def draw_barrier(self, i, j):
        pygame.draw.rect(self.screen, white, (self.grid_squares[i][j].x, self.grid_squares[i][j].y, self.grid_squares[i][j].width, self.grid_squares[i][j].width), 0)

if __name__ == "__main__":
    pf = PathFind()
    pf.run_program()


