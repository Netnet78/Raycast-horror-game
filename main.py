import pygame
import math
import numpy as np
from pygame.locals import *
import game_map

# Define color
B_RED = (125, 22, 22)
M_RED = (107, 19, 16)
L_RED = (69, 15, 16)
BLACK = (5, 5, 10)
WHITE = (255,255,255)
GRAY = (25,25,25)

# Define the world map
world_map = game_map.world_map

# Define the screen resolution
WIDTH = 1400
HEIGHT = 800

def close():
    """ Close the application """
    pygame.display.quit()
    pygame.quit()

def calculate_wall_height(perp_wall_dist):
    """Calculates the height of the wall based on the perpendicular distance.

    Args:
        perp_wall_dist: The perpendicular distance from the ray to the wall.

    Returns:
        The height of the wall.
    """

    line_height = int(HEIGHT / (perp_wall_dist + 0.00001))
    return line_height

clock = pygame.time.Clock()
def update_game():
    """ Updates the game. """
    pygame.event.pump()
    pygame.display.flip()
    pygame.display.update()
    clock.tick(60)
def main():
    """ Main function to run the game """
    pygame.init()
    
    # Display information
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Autophobia")

    # Initialize player position and direction
    position_x = 5.5  # Initial X position
    position_y = 5.5  # Initial Y position
    direction_x = 1  # Initial direction X
    direction_y = 0  # Initial direction Y
    plane_x = 0  # Camera plane X
    plane_y = 0.66  # Camera plane Y (for FOV)

    # Define movement and rotation speeds
    move_speed = 0.1
    rotation_speed = 0.05

    ## Main loop of the program
    while True:
        # Check the key if the player is quitting or not
        for event in pygame.event.get():
            if event.type == QUIT:
                close()

        # Key binding
        keys = pygame.key.get_pressed()
        if keys[K_ESCAPE]:
            close()
            return
        if keys[K_UP]:
            new_x = position_x + direction_x * move_speed
            new_y = position_y + direction_y * move_speed
            if world_map[int(new_y)][int(new_x)] == 0:
                position_x, position_y = new_x, new_y
        if keys[K_DOWN]:
            new_x = position_x - direction_x * move_speed
            new_y = position_y - direction_y * move_speed
            if world_map[int(new_y)][int(new_x)] == 0:
                position_x, position_y = new_x, new_y
        if keys[K_RIGHT]:
            # Rotate RIGHT
            old_dir_x = direction_x
            direction_x = direction_x * math.cos(rotation_speed) - direction_y * math.sin(rotation_speed)
            direction_y = old_dir_x * math.sin(rotation_speed) + direction_y * math.cos(rotation_speed)
            # Rotate plane
            old_plane_x = plane_x
            plane_x = plane_x * math.cos(rotation_speed) - plane_y * math.sin(rotation_speed)
            plane_y = old_plane_x * math.sin(rotation_speed) + plane_y * math.cos(rotation_speed)
        if keys[K_LEFT]:
            # Rotate LEFT
            old_dir_x = direction_x
            direction_x = direction_x * math.cos(-rotation_speed) - direction_y * math.sin(-rotation_speed)
            direction_y = old_dir_x * math.sin(-rotation_speed) + direction_y * math.cos(-rotation_speed)
            # Rotate plane
            old_plane_x = plane_x
            plane_x = plane_x * math.cos(-rotation_speed) - plane_y * math.sin(-rotation_speed)
            plane_y = old_plane_x * math.sin(-rotation_speed) + plane_y * math.cos(-rotation_speed)

        ## Raycasting Logic
        window.fill((25, 25, 25))  # Clear the screen
        pygame.draw.rect(window, (50,50,50), (0, HEIGHT/2, WIDTH, HEIGHT/2))  # Draw floor

        # Calculate ray direction for each column
        columns = 0
        while columns < WIDTH:
            camera_x = 2.0 * columns / WIDTH - 1.0
            ray_pos_x = position_x
            ray_pos_y = position_y
            ray_dir_x = direction_x + plane_x * camera_x
            ray_dir_y = direction_y + plane_y * camera_x

            # Map coordinates
            map_x = int(ray_pos_x)
            map_y = int(ray_pos_y)

            # Delta distance
            delta_dis_x = math.sqrt(1 + (ray_dir_y / ray_dir_x) ** 2)
            delta_dis_y = math.sqrt(1 + (ray_dir_x / ray_dir_y) ** 2)

            # Step and initial side distance
            step_x, step_y = 0, 0
            side_dis_x, side_dis_y = 0.0, 0.0

            # Initialize side
            hit = 0
            if ray_dir_x < 0:
                step_x = -1
                side_dis_x = (ray_pos_x - map_x) * delta_dis_x
            else:
                step_x = 1
                side_dis_x = (map_x + 1.0 - ray_pos_x) * delta_dis_x

            if ray_dir_y < 0:
                step_y = -1
                side_dis_y = (ray_pos_y - map_y) * delta_dis_y
            else:
                step_y = 1
                side_dis_y = (map_y + 1.0 - ray_pos_y) * delta_dis_y

            # Perform DDA
            side = 0
            while not hit == 1:
                if side_dis_x < side_dis_y:
                    side_dis_x += delta_dis_x
                    map_x += step_x
                    side = 0  # X-axis hit
                else:
                    side_dis_y += delta_dis_y
                    map_y += step_y
                    side = 1  # Y-axis hit
                if map_x < 0 or map_x >= WIDTH or map_y < 0 or map_y >= HEIGHT:
                    break # Map border hit

                # Check for collision
                if world_map[map_y][map_x] > 0:
                    hit = 1

            # Correction of the POV
            if side == 0:
                perp_wall_dist = abs((map_x - ray_pos_x + (1 - step_x) / 2) / ray_dir_x)
            else:
                perp_wall_dist = abs((map_y - ray_pos_y + (1 - step_y) / 2) / ray_dir_y)
            max_view_distance = 300 / (perp_wall_dist + 0.00001)
            if perp_wall_dist > max_view_distance:
                break 
            
            # Calculate the draw start and end
            draw_start = -calculate_wall_height(perp_wall_dist) / 2 + HEIGHT / 2
            if draw_start < 0:
                draw_start = 0
            draw_end = calculate_wall_height(perp_wall_dist) / 2 + HEIGHT / 2
            if draw_end >= HEIGHT:
                draw_end = HEIGHT - 1

            # Choose the color based on the map value
            if 0 <= map_x < len(world_map[0]) and 0 <= map_y < len(world_map):
                color = list(L_RED) if world_map[map_y][map_x] == 1 else list(M_RED)
            else:
                color = [25, 25, 25]  # or some other default color

            # Apply shadow
            if side == 1:
               color = [int(c / 1.6) for c in color]

            # Draw the vertical line
            pygame.draw.line(window, color, (columns, draw_start), (columns, draw_end),3)
            columns += 3

        update_game()

if __name__ == "__main__":
    main()
