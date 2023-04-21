import pygame
import re

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Set the dimensions of the screen
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

# Initialize Pygame
pygame.init()

# Set the screen size
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

# Set the window title
pygame.display.set_caption("Level Editor")

# Set the font for the UI
font = pygame.font.SysFont(None, 24)

# viewport x position
view_x = 0
view_move_speed = 16
view_x_velocity = 0


# Create a grid to place tiles on
TILE_SIZE = 8
GRID_WIDTH = SCREEN_WIDTH // TILE_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // TILE_SIZE
grid = [[None for y in range(GRID_HEIGHT)] for x in range(GRID_WIDTH)]

# Define the different types of tiles
TILE_TREE = 0
TILE_TREE_TRUNK = 1
TILE_TREE_CROWN = 2
TILE_AMMO = 3
TILE_BRICK = 4
TILE_DEAD_TREE = 5
TILE_CAR = 6
TILE_CAR_DESTROYED = 7
TILE_RUIN = 8
TILE_JAMMER = 9
TILE_RUIN_BACKGROUND = 10
TILE_RUIN_DEBRIS = 11
TILE_RUIN_LEFT = 12
TILE_RUIN_RIGHT = 13

tiles = []

# Load the images
TREE_TRUNK = pygame.image.load('./images/TreeTrunk.png').convert_alpha()
TREE_CROWN = pygame.image.load('./images/TreeCrown.png').convert_alpha()
JAMMER = pygame.image.load('./images/Jammer.png').convert_alpha()
BRICK = pygame.image.load('./images/Brick.png').convert_alpha()
AMMO = pygame.image.load('./images/AmmoDump(Shells).png').convert_alpha()
GROUND = pygame.image.load('./images/Ground.png').convert_alpha()
GROUND_TILE = pygame.transform.scale(GROUND, (GROUND.get_width() * 10, GROUND.get_height() * 10)).convert_alpha()
CAR = pygame.image.load('./images/Truck (Undamaged) Export.png').convert_alpha()
CAR_DESTROYED = pygame.image.load('./images/Truck (Destroyed) Export.png').convert_alpha()
RUIN_BACKGROUND = pygame.image.load('./images/RuinBackground.png').convert_alpha()
RUIN_DEBRIS = pygame.image.load('./images/RuinDebris.png').convert_alpha()
RUIN_LEFT = pygame.image.load('./images/RuinWallLeft.png').convert_alpha()
RUIN_RIGHT = pygame.image.load('./images/RuinWallRight.png').convert_alpha()

def combine_tree_images(trunk_image, crown_image):
  tree_image = pygame.Surface((crown_image.get_width(), trunk_image.get_height() + crown_image.get_height())).convert_alpha()
  tree_image.blit(trunk_image, (15, crown_image.get_height()-3))
  tree_image.blit(crown_image, (0, 0))
  return tree_image

def combine_ruin_images():
  ruin_image = pygame.Surface((RUIN_BACKGROUND.get_width(), RUIN_BACKGROUND.get_height())).convert_alpha()
  ruin_image.blit(RUIN_BACKGROUND, (0, 0))
  ruin_image.blit(RUIN_DEBRIS, (0, 0))
  ruin_image.blit(RUIN_LEFT, (0, 0))
  ruin_image.blit(RUIN_RIGHT, (0, 0))
  return ruin_image

# Scale the tile images and set values
tile_images = {
  TILE_TREE_TRUNK: pygame.transform.scale(TREE_TRUNK, (TREE_TRUNK.get_width() * 10, TREE_TRUNK.get_height() * 10)).convert_alpha(),
  TILE_TREE_CROWN: pygame.transform.scale(TREE_CROWN, (TREE_CROWN.get_width() * 10, TREE_CROWN.get_height() * 10)).convert_alpha(),
  TILE_TREE: pygame.transform.scale(combine_tree_images(TREE_TRUNK, TREE_CROWN), (TREE_CROWN.get_width() * 10, (TREE_TRUNK.get_height() + TREE_CROWN.get_height()) * 10)).convert_alpha(),
  TILE_JAMMER: pygame.transform.scale(JAMMER, (JAMMER.get_width() * 10, JAMMER.get_height() * 10)).convert_alpha(),
  TILE_BRICK: pygame.transform.scale(BRICK, (BRICK.get_width() * 10, BRICK.get_height() * 10)).convert_alpha(),
  TILE_AMMO: pygame.transform.scale(AMMO, (AMMO.get_width() * 10, AMMO.get_height() * 10)).convert_alpha(),
  TILE_CAR: pygame.transform.scale(CAR, (CAR.get_width() * 10, CAR.get_height() * 10)).convert_alpha(),
  TILE_CAR_DESTROYED: pygame.transform.scale(CAR_DESTROYED, (CAR_DESTROYED.get_width() * 10, CAR_DESTROYED.get_height() * 10)).convert_alpha(),
  TILE_RUIN_BACKGROUND: pygame.transform.scale(RUIN_BACKGROUND, (RUIN_BACKGROUND.get_width() * 10, RUIN_BACKGROUND.get_height() * 10)).convert_alpha(),
  TILE_RUIN_DEBRIS: pygame.transform.scale(RUIN_DEBRIS, (RUIN_DEBRIS.get_width() * 10, RUIN_DEBRIS.get_height() * 10)).convert_alpha(),
  TILE_RUIN_LEFT: pygame.transform.scale(RUIN_LEFT, (RUIN_LEFT.get_width() * 10, RUIN_LEFT.get_height() * 10)).convert_alpha(),
  TILE_RUIN_RIGHT: pygame.transform.scale(RUIN_RIGHT, (RUIN_RIGHT.get_width() * 10, RUIN_RIGHT.get_height() * 10)).convert_alpha(),
  TILE_RUIN: pygame.transform.scale(combine_ruin_images(), (RUIN_BACKGROUND.get_width() * 10, (RUIN_BACKGROUND.get_height() * 10))).convert_alpha(),
}

tile_y = {
  TILE_TREE_TRUNK: 800,
  TILE_TREE_CROWN: 405,
  TILE_TREE: 0,
  TILE_JAMMER: 905,
  TILE_BRICK: 1015,
  TILE_AMMO: 955,
  TILE_CAR: 860,
  TILE_CAR_DESTROYED: 890,
  TILE_RUIN_BACKGROUND: 660,
  TILE_RUIN_DEBRIS: 660,
  TILE_RUIN_LEFT: 660,
  TILE_RUIN_RIGHT: 660,
  TILE_RUIN: 0
}

# Set the default tile type
current_tile = TILE_TREE

# Set up the GUI
def draw_gui():
  screen.fill(BLACK)

  # Draw the current tile type
  tile_text = font.render('Current Tile: {}'.format(current_tile), True, WHITE)
  screen.blit(tile_text, (10, 10))

  help_text = font.render('Import with l, Export with c', True, WHITE)
  screen.blit(help_text, (10, 30))

# Set up the main loop
done = False
clock = pygame.time.Clock()

while not done:
  # Handle events
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      done = True
    elif event.type == pygame.KEYDOWN:
      if event.key == pygame.K_ESCAPE:
        done = True
      # Switch the current tile
      if event.key == pygame.K_1:
        current_tile = TILE_TREE
      elif event.key == pygame.K_2:
        current_tile = TILE_TREE_TRUNK
      elif event.key == pygame.K_3:
        current_tile = TILE_TREE_CROWN
      elif event.key == pygame.K_4:
        current_tile = TILE_AMMO
      elif event.key == pygame.K_5:
        current_tile = TILE_BRICK
      elif event.key == pygame.K_6:
        current_tile = TILE_CAR
      elif event.key == pygame.K_7:
        current_tile = TILE_CAR_DESTROYED
      elif event.key == pygame.K_8:
        current_tile = TILE_RUIN
      elif event.key == pygame.K_9:
        current_tile = TILE_JAMMER
      elif event.key == pygame.K_KP1:
        current_tile = TILE_RUIN_BACKGROUND
      elif event.key == pygame.K_KP2:
        current_tile = TILE_RUIN_DEBRIS
      # Move viewport horizontally with arrow keys
      elif event.key == pygame.K_LEFT:
        view_x_velocity = -view_move_speed
      elif event.key == pygame.K_RIGHT:
        view_x_velocity = view_move_speed
      # Export as code
      elif event.key == pygame.K_c:
        export_code()
      # Import from code
      elif event.key == pygame.K_l:
        load_level()
      # Undo
      elif event.key == pygame.K_u:
        undo()
    elif event.type ==pygame.KEYUP:
      # Stop moving the viewport when the key is released
      if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
        view_x_velocity = 0
    elif event.type == pygame.MOUSEBUTTONDOWN:
      # Place the current tile or object on the grid
      pos = (pygame.mouse.get_pos()[0] + view_x, pygame.mouse.get_pos()[1])
      x = pos[0]
      y = pos[1]

      # Adds tiles to tiles list
      if current_tile == TILE_TREE: # TREE multi tile
        new_tile = (tile_images[TILE_TREE_TRUNK], tile_images[TILE_TREE_TRUNK].get_rect(center = (x, 800)), TILE_TREE_TRUNK, (x, 800))
        print(tile_images[TILE_TREE_TRUNK].get_rect(center = (x - view_x, 800)))
        tiles.append(new_tile)
        new_tile = (tile_images[TILE_TREE_CROWN], tile_images[TILE_TREE_CROWN].get_rect(center = (x, 405)), TILE_TREE_CROWN, (x, 405))
        tiles.append(new_tile)
      elif current_tile == TILE_RUIN: # RUIN multi tile
        new_tile = (tile_images[TILE_RUIN_BACKGROUND], tile_images[TILE_RUIN_BACKGROUND].get_rect(center = (x, 660)), TILE_RUIN_BACKGROUND, (x, 660))
        tiles.append(new_tile)
        new_tile = (tile_images[TILE_RUIN_DEBRIS], tile_images[TILE_RUIN_DEBRIS].get_rect(center = (x, 660)), TILE_RUIN_DEBRIS, (x, 660))
        tiles.append(new_tile)
        new_tile = (tile_images[TILE_RUIN_LEFT], tile_images[TILE_RUIN_LEFT].get_rect(center = (x, 660)), TILE_RUIN_LEFT, (x, 660))
        tiles.append(new_tile)
        new_tile = (tile_images[TILE_RUIN_RIGHT], tile_images[TILE_RUIN_RIGHT].get_rect(center = (x, 660)), TILE_RUIN_RIGHT, (x, 660))
        tiles.append(new_tile)
      else:
        if event.button == 1:
          new_tile = (tile_images[current_tile], tile_images[current_tile].get_rect(center = (x, y)), current_tile, (x, y))
          tiles.append(new_tile)
        elif event.button == 3:
          new_tile = (tile_images[current_tile], tile_images[current_tile].get_rect(center = (x, tile_y[current_tile])), current_tile, (x, tile_y[current_tile]))
          tiles.append(new_tile)
    elif event.type == pygame.MOUSEMOTION:
      # Update the position of the tile preview
      pos = (pygame.mouse.get_pos()[0] + view_x, pygame.mouse.get_pos()[1])
      x = pos[0]
      y = pos[1] 
      if current_tile == TILE_TREE:
        preview_tile_rect = tile_images[TILE_TREE].get_rect(center = (x - view_x, 655))
      elif current_tile == TILE_RUIN:
        preview_tile_rect = tile_images[TILE_RUIN].get_rect(center = (x - view_x, 660))
      else:
        preview_tile_rect = tile_images[current_tile].get_rect(center = (x - view_x, y))
  
  view_x += view_x_velocity
  # Draw the GUI
  draw_gui()

  for x in range(2):
    r = GROUND_TILE.get_rect()
    r.y = 1040
    r.x = x*2000
    screen.blit(GROUND_TILE, r)

  for t in tiles:
    # create a copy of the tile's Rect object
    new_rect = t[1].copy()
    
    # add the camera's x-coordinate to the Rect's x-coordinate
    new_rect.x -= view_x
    
    # draw the tile using the modified Rect object
    screen.blit(t[0], new_rect)

  # Draw the tile preview
  if current_tile is TILE_TREE:
    preview_tile_surface = pygame.Surface((tile_images[current_tile].get_width(), tile_images[current_tile].get_height()), pygame.SRCALPHA)
    preview_tile_surface.set_alpha(128)  # set alpha value to 128 for transparency
    preview_tile_surface.blit(tile_images[current_tile], (0, 0))
    screen.blit(preview_tile_surface, preview_tile_rect)
  elif current_tile is not None:
    preview_tile_surface = pygame.Surface((tile_images[current_tile].get_width(), tile_images[current_tile].get_height()), pygame.SRCALPHA)
    preview_tile_surface.set_alpha(128)  # set alpha value to 128 for transparency
    preview_tile_surface.blit(tile_images[current_tile], (0, 0))
    screen.blit(preview_tile_surface, preview_tile_rect)

  # Update the display
  pygame.display.flip()

  # Limit the frame rate
  clock.tick(60)

  OBJECT_TYPES = {
    TILE_TREE_CROWN: "Obstacle",
    TILE_TREE_TRUNK: "Background",
    TILE_JAMMER: "Obstacle",
    TILE_BRICK: "Brick",
    TILE_AMMO: "Obstacle",
    TILE_CAR: "Obstacle",
    TILE_CAR_DESTROYED: "Obstacle",
    TILE_RUIN_BACKGROUND: "Background",
    TILE_RUIN_DEBRIS: "Obstacle",
    TILE_RUIN_LEFT: "Obstacle",
    TILE_RUIN_RIGHT: "Obstacle",
  }

  # Convert between code names from input and code names from this file
  ENVIRONMENT_TYPES = {
    TILE_TREE_CROWN: "TreeCrown",
    TILE_TREE_TRUNK: "TreeTrunk",
    TILE_JAMMER: "Jammer",
    TILE_BRICK: "Brick",
    TILE_AMMO: "AmmoDump(Shells)",
    TILE_CAR: "Truck (Undamaged) Export",
    TILE_CAR_DESTROYED: "Truck (Destroyed) Export",
    TILE_RUIN_BACKGROUND: "RuinBackground",
    TILE_RUIN_DEBRIS: "RuinDebris",
    TILE_RUIN_LEFT: "RuinWallLeft",
    TILE_RUIN_RIGHT: "RuinWallRight",
  }

  def undo():
    tiles.pop()

  def export_code():
    with open("output.txt", "w") as f:
      # Iterate over each tile in the grid
      for t in tiles:
        # Determine the name of the tile based on its index in the TILE_TYPES list
        object_type = OBJECT_TYPES[t[2]]
        environment_type = ENVIRONMENT_TYPES[t[2]]

        f.write(f'GameWorld().game_objects.add(Environment("{environment_type}", ({t[3][0]}, {t[3][1]}), "{object_type}"))\n')


  def load_level():
      # Open the text file and read each line
      with open("input.txt") as f:
          for line in f:
              # Check if the line contains "Environment"
              if "Environment" in line:
                  # Use regular expressions to extract the parameters
                  match = re.search(r'Environment\("(.+)", \((-?\d+), (-?\d+)\), "(.+)"\)', line)
                  if match:
                      param1 = match.group(1)
                      param2 = (int(match.group(2)), int(match.group(3)))
                      environment_type = match.group(4) # Obstacle or Background
                      print(param1, param2, environment_type)
                      # Extract the x and y coordinates from the second parameter
                      x, y = param2
                      # Check if the first parameter matches one of the environment types
                      if param1 in ENVIRONMENT_TYPES.values():
                        # Find the key for the matching environment type
                        key = [k for k, v in ENVIRONMENT_TYPES.items() if v == param1][0]
                        # Create new_tile with x and y coordinates
                        new_tile = (tile_images[key], tile_images[key].get_rect(center=(x, y)), key, (x, y))
                        tiles.append(new_tile)
                        


pygame.quit()