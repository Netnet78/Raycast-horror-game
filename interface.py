import pygame
from pygame.locals import *
import sys

B_RED = (125, 22, 22)
M_RED = (107, 19, 16)
L_RED = (69, 15, 16)
BLACK = (5, 5, 10)
WHITE = (255,255,255)
GRAY = (25,25,25)
FONT_SIZE = 18

class StartupScreen:
    pygame.init()
    pygame.font.init()
    def __init__(self, window, width, height):
        self.title = "Welcome to the Game"
        self.subtitle = "Press Space to Start"
        self.window = window
        self.font = pygame.font.SysFont("Arial", 24)
        self.width = width
        self.height = height

    def draw(self):
        self.window.fill(BLACK)
        title_text = self.font.render(self.title, True, WHITE)
        subtitle_text = self.font.render(self.subtitle, True, WHITE)
        self.window.blit(title_text, (self.width // 2 - title_text.get_width() // 2, self.height // 2 - title_text.get_height() // 2))
        self.window.blit(subtitle_text, (self.width // 2 - subtitle_text.get_width() // 2, self.height // 2 - subtitle_text.get_height() // 2 + FONT_SIZE))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Start the game here
                    print("Game started!")
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        