
import pygame.font
from colors import Colors
import pygame

class Button:

    def __init__(self, screen, message, x, y, width = 240, height = 50,
	button_color = Colors.GREEN, highlight_color = Colors.LIGHT_GREY):

        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.initial_button_color = button_color
        self.highlight_color = highlight_color

        self.width, self.height = width, height
        self.button_color = button_color
        self.text_color = Colors.WHITE
        self.font = pygame.font.SysFont(None, 48)

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.centerx = x
        self.rect.y = y

        self.prep_message(message)

    def prep_message(self, message):
        self.message_image = self.font.render(message, True, self.text_color)
        self.message_image_rect = self.message_image.get_rect()
        self.message_image_rect.center = self.rect.center

    def draw_button(self):
        self.highlight_button()
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.message_image, self.message_image_rect)

    def highlight_button(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_x, mouse_y):
            self.button_color = self.highlight_color 
        else:
            self.button_color = self.initial_button_color
