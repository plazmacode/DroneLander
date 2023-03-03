import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Lunar Lander")

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)

# Define fonts
font = pygame.font.SysFont(None, 48)

# Load images
lander_image = pygame.image.load("lander.png").convert()
terrain_image = pygame.image.load("terrain.png").convert()

class LunarLander(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = lander_image
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width // 2, 50)
        self.velocity = 0
        self.acceleration = 0.1
        self.angle = 0
        self.rotate_speed = 5

    def update(self):
        self.velocity += self.acceleration
        self.rect.y += self.velocity
        self.rotate()
        
    def rotate(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.angle += self.rotate_speed
        elif keys[pygame.K_RIGHT]:
            self.angle -= self.rotate_speed
        self.angle %= 360
        self.image = pygame.transform.rotate(lander_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def thrust(self):
        angle_radians = math.radians(self.angle)
        thrust_vector = pygame.math.Vector2(0, -3)
        thrust_vector.rotate_ip(-self.angle)
        self.velocity += thrust_vector.y
        self.acceleration += thrust_vector.y / 100

# Define the Terrain class
class Terrain(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = terrain_image
        self.rect = pygame.Rect(x, y, width, height)

# Create the terrain
terrain_list = []
for i in range(10):
    x = random.randint(0, screen_width - 100)
    y = random.randint(screen_height - 200, screen_height - 50)
    width = random.randint(50, 100)
    height = random.randint(50, 100)
    terrain = Terrain(x, y, width, height)
    terrain_list.append(terrain)

# Define the game loop
def game_loop():
    game_over = False
    game_win = False

    # Create the Lunar Lander sprite
    lander = LunarLander()
    lander_group = pygame.sprite.Group(lander)

    # Create the Terrain sprites
    terrain_group = pygame.sprite.Group()
    for terrain in terrain_list:
        terrain_group.add(terrain)

    # Create the clock
    clock = pygame.time.Clock()

    while not game_over and not game_win:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    lander.thrust()

        # Update the game state
        lander.update()

        # Check for collisions
        if pygame.sprite.spritecollide(lander, terrain_group, False):
            game_over = True
        elif lander.rect.bottom >= screen_height - 10:
            game_win = True

        # Draw the screen
        screen.fill(black)
        terrain_group.draw(screen)
        lander_group.draw(screen)

        # Update the display
        pygame.display.flip()

        # Wait for the next frame
        clock.tick(60)

    # End the game
    if game_over:
        message = font.render("You crashed!", True, white)
    elif game_win:
        message = font.render("You landed safely!", True, white)

    screen.blit(message, (screen_width // 2 - message.get_width() // 2, screen_height // 2 - message.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(2000)

# Start the game loop
game_loop()

# Quit Pygame
