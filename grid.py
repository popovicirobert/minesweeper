
import pygame
import pygame.font
from colors import Colors
from random import shuffle
from collections import deque
from random import randint

class Grid:

    def __init__(self, GRID_WIDTH, GRID_HEIGHT, GRID_BOMBS, CELL_SIZE):
        self.GRID_WIDTH = GRID_WIDTH
        self.GRID_HEIGHT = GRID_HEIGHT
        self.GRID_BOMBS = GRID_BOMBS

        self.CELL_SIZE = CELL_SIZE
        self.OFFSET = self.CELL_SIZE // 3

        self.REVEAL_LIMIT = 10
        self.NOT_CHECKED = 0
        self.SURE_BOMB = 1
        self.POSSIBLE_BOMB = 2
        self.NO_BOMB = 3
        self.BOMB_HIT = 4

        self.cell = [[None for y in range(GRID_HEIGHT)] for x in range(GRID_WIDTH)]
        self.state = [[None for y in range(GRID_HEIGHT)] for x in range(GRID_WIDTH)]
        self.bomb = [[None for y in range(GRID_HEIGHT)] for x in range(GRID_WIDTH)]
        self.color = [[None for y in range(GRID_HEIGHT)] for x in range(GRID_WIDTH)]
        self.count = [[None for y in range(GRID_HEIGHT)] for x in range(GRID_WIDTH)]
        self.visited = [[None for y in range(GRID_HEIGHT)] for x in range(GRID_WIDTH)]

        self.font = pygame.font.SysFont('Arial', 20)

        self.build_grid()

    def init_grid(self):
        for x in range(self.GRID_WIDTH):
            for y in range(self.GRID_HEIGHT):
                self.cell[x][y] = pygame.Rect(x * self.CELL_SIZE + x - 1,
                                              y * self.CELL_SIZE + y - 1,
                                              self.CELL_SIZE,
                                              self.CELL_SIZE)
                self.state[x][y] = 0
                self.bomb[x][y] = False
                self.color[x][y] = Colors.LIGHT_GREY
                self.count[x][y] = 0
                self.visited[x][y] = False

        self.found_cells = 0
        self.found_bombs = 0

    def place_bombs(self):
        permutation = [value for value in range(0, self.GRID_WIDTH * self.GRID_HEIGHT)]
        shuffle(permutation)

        for index in range(self.GRID_BOMBS):
            x = permutation[index] % self.GRID_WIDTH
            y = permutation[index] // self.GRID_WIDTH
            self.bomb[x][y] = True

    def build_count(self):
        dx = [-1, 0, 1, -1, 1, -1, 0, 1]
        dy = [-1, -1, -1, 0, 0, 1, 1, 1]
        for x in range(self.GRID_WIDTH):
            for y in range(self.GRID_HEIGHT):
                for index in range(8):
                    new_x = x + dx[index]
                    new_y = y + dy[index]
                    if new_x >= 0 and new_y >= 0 and new_x < self.GRID_WIDTH and\
                            new_y < self.GRID_HEIGHT and self.bomb[new_x][new_y] == True:
                        self.count[x][y] += 1


    def build_grid(self):
        self.init_grid()
        self.place_bombs()
        self.build_count()

    def show_grid(self, screen, bomb_hit = False):
        for x in range(self.GRID_WIDTH):
            for y in range(self.GRID_HEIGHT):
                pygame.draw.rect(screen, self.color[x][y], self.cell[x][y])

                if self.state[x][y] == self.SURE_BOMB:
                    self.show_cell(x, y, '!', screen)
                elif self.state[x][y] == self.POSSIBLE_BOMB:
                    self.show_cell(x, y, '?', screen)
                elif self.state[x][y] == self.NOT_CHECKED:
                    self.show_cell(x, y, '', screen)
                elif self.state[x][y] == self.NO_BOMB:
                    self.show_cell(x, y, f'{self.count[x][y]}', screen)

                if bomb_hit == True:
                    if self.state[x][y] == self.POSSIBLE_BOMB:
                        pygame.draw.rect(screen, self.color[x][y], self.cell[x][y])
                        self.show_cell(x, y, '', screen)

                    if self.bomb[x][y] == True:
                        if self.state[x][y] != self.SURE_BOMB:
                            self.show_cell(x, y, 'x', screen)
                    else:
                        if self.state[x][y] == self.SURE_BOMB:
                            self.color[x][y] = Colors.RED
                            pygame.draw.rect(screen, self.color[x][y], self.cell[x][y])
                            self.show_cell(x, y, '!', screen)


    def show_cell(self, x, y, text, screen):
        text_image = self.font.render(text, True, (0, 0, 0))
        screen.blit(text_image, (x * self.CELL_SIZE + x - 1 + self.OFFSET,
                                 y * self.CELL_SIZE + y - 1))

    def find_bomb_free_cells(self, x, y):
        queue = deque()
        queue.append([x, y])

        self.visited[x][y] = True

        current_found_cells = 0
        current_reveal_limit = randint(1, self.REVEAL_LIMIT)

        if self.found_cells == 0:
            current_reveal_limit = self.REVEAL_LIMIT

        while queue:
            x, y = queue.popleft()

            if current_found_cells < current_reveal_limit:

                current_found_cells += 1
                self.state[x][y] = 3

                if x > 0 and self.visited[x - 1][y] == False and self.bomb[x - 1][y] == False:
                    queue.append([x - 1, y])
                    self.visited[x - 1][y] = True

                if y > 0 and self.visited[x][y - 1] == False and self.bomb[x][y - 1] == False:
                    queue.append([x, y - 1])
                    self.visited[x][y - 1] = True

                if x + 1 < self.GRID_WIDTH and self.visited[x + 1][y] == False and self.bomb[x + 1][y] == False:
                    queue.append([x + 1, y])
                    self.visited[x + 1][y] = True

                if y + 1 < self.GRID_HEIGHT and self.visited[x][y + 1] == False and self.bomb[x][y + 1] == False:
                    queue.append([x, y + 1])
                    self.visited[x][y + 1] = True

        self.found_cells += current_found_cells


    def reveal(self, x, y, screen):
        if self.bomb[x][y] == True:
            self.color[x][y] = Colors.RED
            return False

        self.find_bomb_free_cells(x, y)
        return True

    def update_state(self, x, y):
        if self.state[x][y] == self.NOT_CHECKED:
            if self.found_bombs + 1 <= self.GRID_BOMBS:
                self.found_bombs += 1
                self.state[x][y] = (self.state[x][y] + 1) % 3
        else:
            if self.state[x][y] == self.SURE_BOMB:
                self.found_bombs -= 1
            self.state[x][y] = (self.state[x][y] + 1) % 3

    def game_over(self):
        return self.found_bombs == self.GRID_BOMBS and \
               self.found_cells == self.GRID_HEIGHT * self.GRID_WIDTH - self.GRID_BOMBS


