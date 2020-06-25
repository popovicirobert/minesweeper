
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

        self.SCREEN_HEIGHT = 500
        self.SCREEN_WIDTH = 500

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

        self.EASY_CELL_SIZE = 50
        self.EASY_GRID_WIDTH = 9
        self.EASY_GRID_HEIGHT = 9
        self.EASY_BOMB = 10
        self.EASY_SCREEN_WIDTH = self.EASY_CELL_SIZE * self.EASY_GRID_WIDTH +\
                                 self.EASY_GRID_WIDTH - 1
        self.EASY_SCREEN_HEIGHT = self.EASY_CELL_SIZE * self.EASY_GRID_HEIGHT +\
                                  self.EASY_GRID_HEIGHT - 1 + 100

        self.MEDIUM_CELL_SIZE = 30
        self.MEDIUM_GRID_WIDTH = 16
        self.MEDIUM_GRID_HEIGHT = 16
        self.MEDIUM_BOMB = 40
        self.MEDIUM_SCREEN_WIDTH = self.MEDIUM_CELL_SIZE * self.MEDIUM_GRID_WIDTH +\
                                   self.MEDIUM_GRID_WIDTH - 1
        self.MEDIUM_SCREEN_HEIGHT = self.MEDIUM_CELL_SIZE * self.MEDIUM_GRID_HEIGHT +\
                                    self.MEDIUM_GRID_HEIGHT - 1 + 100

        self.HARD_CELL_SIZE = 30
        self.HARD_GRID_WIDTH = 29
        self.HARD_GRID_HEIGHT = 16
        self.HARD_BOMB = 99
        self.HARD_SCREEN_WIDTH = self.HARD_CELL_SIZE * self.HARD_GRID_WIDTH +\
                                 self.HARD_GRID_WIDTH - 1
        self.HARD_SCREEN_HEIGHT = self.HARD_CELL_SIZE * self.HARD_GRID_HEIGHT +\
                                  self.HARD_GRID_HEIGHT - 1 + 100

        self.menu_active = False

        self.bomb_hit = False

    def update_screen(self):

        if self.game_active == False:
            self.easy_button.draw_button()
            self.medium_button.draw_button()
            self.hard_button.draw_button()
            self.exit_button.draw_button()
        else:
            if self.menu_active == False:
                self.menu_button.draw_button()
                self.flags_button.draw_button()
                self.time_button.draw_button()
                self.grid.show_grid(self.screen, bomb_hit = self.bomb_hit)
            else:
                self.screen.fill(Colors.GREY, self.menu_rect)
                self.menu_resume_button.draw_button()
                self.menu_restart_button.draw_button()
                self.menu_exit_button.draw_button()

        pygame.display.update()

    def check_easy_button(self):
        assert self.game_active == False
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.easy_button.rect.collidepoint(mouse_x, mouse_y):
            self.game_active = True
            self.screen = pygame.display.set_mode((self.EASY_SCREEN_WIDTH,
                                                   self.EASY_SCREEN_HEIGHT))
            self.screen.fill(Colors.GREY)

            self.grid = Grid(self.EASY_GRID_WIDTH, self.EASY_GRID_HEIGHT,
                             self.EASY_BOMB, self.EASY_CELL_SIZE)


    def check_medium_button(self):
        assert self.game_active == False
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.medium_button.rect.collidepoint(mouse_x, mouse_y):
            self.game_active = True
            self.screen = pygame.display.set_mode((self.MEDIUM_SCREEN_WIDTH,
                                                   self.MEDIUM_SCREEN_HEIGHT))
            self.screen.fill(Colors.GREY)

            self.grid = Grid(self.MEDIUM_GRID_WIDTH, self.MEDIUM_GRID_HEIGHT,
                             self.MEDIUM_BOMB, self.MEDIUM_CELL_SIZE)


    def check_hard_button(self):
        assert self.game_active == False
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.hard_button.rect.collidepoint(mouse_x, mouse_y):
            self.game_active = True
            self.screen = pygame.display.set_mode((self.HARD_SCREEN_WIDTH,
                                                   self.HARD_SCREEN_HEIGHT))
            self.screen.fill(Colors.GREY)

            self.grid = Grid(self.HARD_GRID_WIDTH, self.HARD_GRID_HEIGHT,
                             self.HARD_BOMB, self.HARD_CELL_SIZE)


    def check_exit_button(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.exit_button.rect.collidepoint(mouse_x, mouse_y):
            pygame.quit()
            sys.exit()

    def check_menu_button(self):
        if self.game_active == True and self.menu_active == False:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if self.menu_button.rect.collidepoint(mouse_x, mouse_y) == True:
                self.menu_active = True

                self.menu_rect = pygame.Rect(0, 0, 300, 250)
                screen_rect = self.screen.get_rect()
                self.menu_rect.centerx = screen_rect.centerx
                self.menu_rect.y = 20

                self.menu_resume_button = Button(self.screen,
                                                 'Resume',
                                                 screen_rect.centerx,
                                                 40)

                self.menu_restart_button = Button(self.screen,
                                                 'Restart',
                                                 screen_rect.centerx,
                                                 110)

                self.menu_exit_button = Button(self.screen,
                                               'Exit',
                                               screen_rect.centerx,
                                               180)

                self.menu_start_time = pygame.time.get_ticks()



    def check_menu_exit_button(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.menu_exit_button.rect.collidepoint(mouse_x, mouse_y) == True:
            self.game_active = False
            self.menu_active = False
            self.bomb_hit = False

            self.screen = pygame.display.set_mode((self.SCREEN_WIDTH,
                                                   self.SCREEN_HEIGHT))
            self.screen.fill(Colors.GREY)

    def check_menu_resume_button(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.menu_resume_button.rect.collidepoint(mouse_x, mouse_y) == True:
            self.screen.fill(Colors.GREY)
            self.menu_active = False
            self.menu_spent_time += pygame.time.get_ticks() - self.menu_start_time

    def check_menu_restart_button(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.menu_restart_button.rect.collidepoint(mouse_x, mouse_y) == True:
            assert self.game_active == True
            self.menu_active = False
            self.bomb_hit = False
            self.screen.fill(Colors.GREY)
            self.grid = Grid(self.grid.GRID_WIDTH, self.grid.GRID_HEIGHT,
                             self.grid.GRID_BOMBS, self.grid.CELL_SIZE)
            self.flags_button.prep_message(f'{self.grid.found_bombs} / {self.grid.GRID_BOMBS}')

            self.start_time = pygame.time.get_ticks()
            self.menu_spent_time = 0


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

    def display_time(self):
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - self.start_time - self.menu_spent_time) // 1000

        seconds = elapsed_time % 60
        hours = elapsed_time // 3600
        minutes = elapsed_time - hours * 3600 - seconds

        self.time_button.prep_message(f'{hours:02}:{minutes:02}:{seconds:02}')

    def check_events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_active == True:
                    if self.menu_active == False:
                        x, y = self.get_mouse_cell()
                        if x != None and self.grid.state[x][y] != self.grid.NO_BOMB and self.bomb_hit == False:
                            if event.button == pygame.BUTTON_LEFT:
                                self.bomb_hit = (self.grid.reveal(x, y, self.screen) == False)
                            elif event.button == pygame.BUTTON_RIGHT:
                                self.grid.update_state(x, y)
                                self.flags_button.prep_message(f'{self.grid.found_bombs} / {self.grid.GRID_BOMBS}')

                        self.check_menu_button()

                    else:
                        self.check_menu_resume_button()
                        self.check_menu_restart_button()
                        self.check_menu_exit_button()

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
                        X, Y = pygame.display.get_surface().get_size()
                        self.menu_button = Button(self.screen, 'Menu',
                                                  self.screen.get_rect().centerx,
                                                  Y - 75, width = 100)

                        self.flags_button = Button(self.screen, f'0 / {self.grid.GRID_BOMBS}',
                                                   (self.menu_button.rect.x + self.menu_button.width + X) // 2,
                                                   Y - 75, width = 100, button_color = Colors.GREY,
												   highlight_color = Colors.GREY)

                        self.start_time = pygame.time.get_ticks()
                        self.menu_spent_time = 0
                        self.time_button = Button(self.screen, '00:00:00',
                                                  self.menu_button.rect.x // 2,
                                                  Y - 75, width = 150, button_color = Colors.GREY,
												  highlight_color = Colors.GREY)


        if self.game_active == True and self.bomb_hit == False:
            self.color_cells()


    def start(self):

        while True:
            if self.game_active == True and self.bomb_hit == False:
                self.display_time()

            self.check_events()
            self.update_screen()


minesweeper = MineSweeper()
minesweeper.start()
