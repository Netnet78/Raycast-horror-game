try:
    import pygame
    import math
    import numpy as np
    from pygame.locals import *
    import game_map
except ImportError as e:
    raise ImportError("Error: missing dependencies.\nError log:" + str(e))

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

    # Initialize camera pitch
    vertical_line = 0.0

    # Define movement, mouse position and rotation speed
    move_speed = 0.05
    rotation_speed = 0.005
    mouse_x = WIDTH // 2
    mouse_y = HEIGHT // 2
    pygame.mouse.set_pos(mouse_x, mouse_y)
    pygame.mouse.set_visible(False)

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
        if keys[K_w]:
            # Move UP
            new_x = position_x + direction_x * move_speed
            new_y = position_y + direction_y * move_speed
            if world_map[int(new_y)][int(new_x)] == 0:
                position_x, position_y = new_x, new_y
        if keys[K_s]:
            # Move DOWN
            new_x = position_x - direction_x * move_speed
            new_y = position_y - direction_y * move_speed
            if world_map[int(new_y)][int(new_x)] == 0:
                position_x, position_y = new_x, new_y
        if keys[K_d]:
            # Move RIGHT
            new_x = position_x - direction_y * move_speed
            new_y = position_y + direction_x * move_speed
            if world_map[int(new_y)][int(new_x)] == 0:
                position_x, position_y = new_x, new_y
        if keys[K_a]:
            # Move LEFT
            new_x = position_x + direction_y * move_speed
            new_y = position_y - direction_x * move_speed
            if world_map[int(new_y)][int(new_x)] == 0:
                position_x, position_y = new_x, new_y
        
        # Handle mouse movement
        mouse_dx, mouse_dy = pygame.mouse.get_rel()
        if pygame.event.Event(MOUSEMOTION):
            rotation = mouse_dx * rotation_speed  # Adjust sensitivity with the multiplier
            old_dir_x = direction_x
            direction_x = direction_x * math.cos(rotation) - direction_y * math.sin(rotation)
            direction_y = old_dir_x * math.sin(rotation) + direction_y * math.cos(rotation)
            # Rotate plane for the camera's projection planes
            old_plane_x = plane_x
            plane_x = plane_x * math.cos(rotation) - plane_y * math.sin(rotation)
            plane_y = old_plane_x * math.sin(rotation) + plane_y * math.cos(rotation)
            # Update camera pitch to look up and down
            vertical_line -= mouse_dy * (rotation_speed * 500)
        
        # Update mouse position
        pygame.mouse.set_pos(mouse_x, mouse_y)
        # Lock the cursor in the middle of the screen
        pygame.event.set_grab(True)

        ## Raycasting Logic
        window.fill(GRAY)  # Clear the screen
        # Draw the floor
        pygame.draw.rect(window, GRAY, (0, HEIGHT // 2 + vertical_line, WIDTH, HEIGHT // 2))
        # Draw the ceiling
        pygame.draw.rect(window, L_RED, (0, 0, WIDTH, HEIGHT // 2 + vertical_line))

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
            delta_dis_x = math.sqrt(1 + (ray_dir_y / (ray_dir_x + 0.000001)) ** 2)
            delta_dis_y = math.sqrt(1 + (ray_dir_x / (ray_dir_y + 0.000001)) ** 2)

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
            
            # Calculate the draw start and end
            draw_start = -calculate_wall_height(perp_wall_dist) / 2 + HEIGHT / 2 + int(vertical_line)
            draw_end = calculate_wall_height(perp_wall_dist) / 2 + HEIGHT / 2 + int(vertical_line)
            
            # Clamp the draw end and draw start to screen boundaries
            draw_start = max(0, draw_start)
            draw_end = min(HEIGHT - 1, draw_end)

            # Choose the color based on the map value
            if 0 <= map_x < len(world_map[0]) and 0 <= map_y < len(world_map):
                color = list(BLACK) if world_map[map_y][map_x] == 1 else list(WHITE)
            else:
                return

            # Apply shadow
            if side == 1:
               color = [int(c / 1.6) for c in color]

            # Draw the vertical line
            pygame.draw.line(window, color, (columns, draw_start), (columns, draw_end),3)

            # Update the column
            columns += 3

        pygame.draw.circle(window, WHITE, (int(mouse_x), int(mouse_y)), 5)

        update_game()
        pygame.display.flip()

if __name__ == "__main__":
    main()
