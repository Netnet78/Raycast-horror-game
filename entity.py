import pygame
from pygame.locals import *

pygame.init()
pygame.mixer.init()

WIDTH = 1400
HEIGHT = 800

# Sound effects
normal_walking_sound = pygame.mixer.Sound("sfx\\sounds\\walking.mp3")
normal_walking_sound.set_volume(1)

# Channel of sound effects
walking_channel = pygame.mixer.Channel(1)
walking_channel.set_volume(1)

# Variable to store player movements
# Initialize player position and direction
position_x = 5.5  # Initial X position
position_y = 5.5  # Initial Y position
direction_x = 1  # Initial direction X
direction_y = 0  # Initial direction Y
plane_x = 0  # Camera plane X
plane_y = 0.66  # Camera plane Y (for FOV)

# Initialize camera pitch
vertical_line = 0.0

# Define movement, mouse position and rotation speed
move_speed = 0.025
rotation_speed = 0.005
mouse_x = WIDTH // 2
mouse_y = HEIGHT // 2

# Function to handle walking sounds



if __name__ == "__main__":
    handle_walking_sounds()
