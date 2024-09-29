import numpy as np
import random

# Set the dimensions for the larger map
map_width = 50
map_height = 50

# Generate a random map with weighted values
# 1 and 2 for walls, 0 for paths, 3 for special items
world_map = np.zeros((map_height, map_width), dtype=int)

for i in range(map_height):
    for j in range(map_width):
        # Add walls at the boundaries
        if i == 0 or j == 0 or i == map_height - 1 or j == map_width - 1:
            world_map[i][j] = random.choice([1, 2])  # Boundary walls
        else:
            # Weighted random placement: more paths than walls and obstacles
            world_map[i][j] = random.choices([0, 1, 2, 3], [70, 10, 10, 10])[0]

# Print a portion of the map for reference
def main():
    print(world_map)
    
if __name__ == "__main__":
    main()
