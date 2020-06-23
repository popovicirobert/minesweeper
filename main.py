
import pygame
import sys
from grid import Grid
from button import Button
from colors import Colors
from time import sleep

class MineSweeper:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Minesweeper')

        self.SCREEN_HEIGHT = 700
        self.SCREEN_WIDTH = 700

        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.screen.fill(Colors.GREY)
        self.screen_rect = self.screen.get_rect()

        self.game_active = False

        self.easy_button = Button(self.screen, 'Easy game',
                                  self.screen_rect.centerx, 50)

        self.medium_button = Button(self.screen, 'Medium game',
                                    self.screen_rect.centerx, 150)

        self.hard_button = Button(self.screen, 'Hard game',
                                  self.screen_rect.centerx, 250)

        self.exit_button = Button(self.screen, 'Exit',
                                  self.screen_rect.centerx, 350)

        self.CELL_SIZE = 30

        self.EASY_GRID_WIDTH = 9
        self.EASY_GRID_HEIGHT = 9
        self.EASY_BOMB = 10
        self.EASY_SCREEN_WIDTH = self.CELL_SIZE * self.EASY_GRID_WIDTH +\
                                 self.EASY_GRID_WIDTH - 1
        self.EASY_SCREEN_HEIGHT = self.CELL_SIZE * self.EASY_GRID_HEIGHT +\
                                  self.EASY_GRID_HEIGHT - 1

        self.MEDIUM_GRID_WIDTH = 16
        self.MEDIUM_GRID_HEIGHT = 16
        self.MEDIUM_BOMB = 40
        self.MEDIUM_SCREEN_WIDTH = self.CELL_SIZE * self.MEDIUM_GRID_WIDTH +\
                                   self.MEDIUM_GRID_WIDTH - 1
        self.MEDIUM_SCREEN_HEIGHT = self.CELL_SIZE * self.MEDIUM_GRID_HEIGHT +\
                                    self.MEDIUM_GRID_HEIGHT - 1

        self.HARD_GRID_WIDTH = 29
        self.HARD_GRID_HEIGHT = 16
        self.HARD_BOMB = 99
        self.HARD_SCREEN_WIDTH = self.CELL_SIZE * self.HARD_GRID_WIDTH +\
                                 self.HARD_GRID_WIDTH - 1
        self.HARD_SCREEN_HEIGHT = self.CELL_SIZE * self.HARD_GRID_HEIGHT +\
                                  self.HARD_GRID_HEIGHT - 1


    def update_screen(self):

        if self.game_active == False:
            self.easy_button.draw_button()
            self.medium_button.draw_button()
            self.hard_button.draw_button()
            self.exit_button.draw_button()
        else:
            self.grid.show_grid(self.screen)

        pygame.display.update()

    def check_easy_button(self):
        assert self.game_active == False
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.easy_button.rect.collidepoint(mouse_x, mouse_y):
            self.game_active = True
            self.screen = pygame.display.set_mode((self.EASY_SCREEN_WIDTH,
                                                   self.EASY_SCREEN_HEIGHT))
            self.grid = Grid(self.EASY_GRID_WIDTH, self.EASY_GRID_HEIGHT,
                             self.EASY_BOMB, self.CELL_SIZE)

    def check_medium_button(self):
        assert self.game_active == False
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.medium_button.rect.collidepoint(mouse_x, mouse_y):
            self.game_active = True
            self.screen = pygame.display.set_mode((self.MEDIUM_SCREEN_WIDTH,
                                                   self.MEDIUM_SCREEN_HEIGHT))
            self.grid = Grid(self.MEDIUM_GRID_WIDTH, self.MEDIUM_GRID_HEIGHT,
                             self.MEDIUM_BOMB, self.CELL_SIZE)

    def check_hard_button(self):
        assert self.game_active == False
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.hard_button.rect.collidepoint(mouse_x, mouse_y):
            self.game_active = True
            self.screen = pygame.display.set_mode((self.HARD_SCREEN_WIDTH,
                                                   self.HARD_SCREEN_HEIGHT))
            self.grid = Grid(self.HARD_GRID_WIDTH, self.HARD_GRID_HEIGHT,
                             self.HARD_BOMB, self.CELL_SIZE)

    def check_exit_button(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.exit_button.rect.collidepoint(mouse_x, mouse_y):
            pygame.quit()
            sys.exit()

    def color_cells(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for x in range(self.grid.GRID_WIDTH):
            for y in range(self.grid.GRID_HEIGHT):
                if self.grid.cell[x][y].collidepoint(mouse_x, mouse_y) == True:
                    self.grid.color[x][y] = Colors.WHITE
                else:
                    self.grid.color[x][y] = Colors.LIGHT_GREY

    def get_mouse_cell(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for x in range(self.grid.GRID_WIDTH):
            for y in range(self.grid.GRID_HEIGHT):
                if self.grid.cell[x][y].collidepoint(mouse_x, mouse_y) == True:
                    return [x, y]
        return [None, None]

    def check_events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_active == True:
                    x, y = self.get_mouse_cell()
                    if x != None and self.grid.state[x][y] != self.grid.NO_BOMB:
                        if event.button == pygame.BUTTON_LEFT:
                            self.game_active = self.grid.reveal(x, y, self.screen)
                        elif event.button == pygame.BUTTON_RIGHT:
                            self.grid.update_state(x, y)

                    if self.game_active == False or self.grid.game_over():
                        self.grid.show_grid(self.screen, bomb_hit = (self.game_active == False))
                        pygame.display.update()

                        sleep(4)
                        self.game_active = False

                        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH,
                                                               self.SCREEN_HEIGHT))
                        self.screen.fill(Colors.GREY)

                elif event.button == pygame.BUTTON_LEFT:
                    if self.game_active == False:
                        self.check_easy_button()
                    if self.game_active == False:
                        self.check_medium_button()
                    if self.game_active == False:
                        self.check_hard_button()
                    if self.game_active == False:
                        self.check_exit_button()

        if self.game_active == True:
            self.color_cells()


    def start(self):

        while True:

            self.check_events()
            self.update_screen()


minesweeper = MineSweeper()
minesweeper.start()