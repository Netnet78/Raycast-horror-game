import pygame
import math
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
    def __init__(self, window):
        self.title = "Autophobia"
        self.subtitle = "Alone in the void"
        self.window = window
        self.font = ("fonts\\HelpMe.ttf", "fonts\\DoubleHomicide.ttf")
        self.header_font = pygame.font.Font(self.font[0], 64)
        self.sec_header_font = pygame.font.Font(self.font[0], 36)
        self.body_font = pygame.font.Font(self.font[1], 48)
        self.width = self.window.get_size()[0]
        self.height = self.window.get_size()[1]
        self.audio = pygame.mixer.Sound("sfx\\music\\Shattered-Mind.mp3")
        self.run = True

    def draw(self):
        """
        Draws the startup screen with the title and subtitle centered on the window.
        :return: Graphics
        """
        self.window.fill(BLACK)
        self.title_text = self.header_font.render(self.title, True, WHITE)
        self.window.blit(self.title_text, (self.width // 2 - self.title_text.get_width() // 2 , 10))
        self.subtitle_text = self.sec_header_font.render(self.subtitle, True, WHITE)
        self.window.blit(self.subtitle_text, (self.width // 2 - self.subtitle_text.get_width() // 2 , 110))
        self.play_button = self.body_font.render("Play", True, WHITE)
        self.window.blit(self.play_button, (self.width // 2 - self.play_button.get_width() // 2 , self.height - 100))
        self.audio.play()
        

    def handle_events(self):
        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    play_button_rect = pygame.Rect(self.width // 2 - self.play_button.get_width() // 2 , self.height - 100, self.play_button.get_width(), self.play_button.get_height())
                    if play_button_rect.collidepoint(mouse_pos):
                        print("Game started!")
                        self.audio.stop()
                        self.run = False  # Stop the loop
                        return  # Exit the function to continue with the main game

            pygame.display.update()
            pygame.display.flip()
    
        