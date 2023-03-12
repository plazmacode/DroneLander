import pygame
from classes.GameObject import GameObject
from classes.Grenade import Grenade

class Player(GameObject):
    def __init__(self) -> None:
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        # this is a mess
        self.image = pygame.image.load("./images/Drone(1).png").convert_alpha()
        self.base_image = pygame.image.load("./images/Drone(1).png").convert_alpha()
        self.base_image = pygame.transform.scale(self.image, (125, 50))
        rects = ((0, 0, 20, 8), (20, 0, 20, 8), (40, 0, 20, 8), (60, 0, 20, 8))
        self.base_images = self.loadImages("./images/drone-spritesheet.png", rects, (self.image.get_width() * 10, self.image.get_height() * 10))
        self.current_image = 0
        self.rect = self.image.get_rect()
        self.rect.center = (100, 450)
        self.tag = "Player"
        self.angle = 0
        self.rotation_speed = 4
        self.direciton = pygame.math.Vector2(0,0)
        self.velocity = pygame.math.Vector2(0,0)
        self.keys = pygame.key.get_pressed()
        self.oldKeys = pygame.key.get_pressed()
        self.can_attack = True
        self.load_difficulty()
        from classes.GameWorld import GameWorld
        GameWorld().grenades = self.grenades

    def update(self):
        self.move()
        self.animate()
    
    def load_difficulty(self):
        from classes.GameWorld import GameWorld
        if GameWorld().difficulty == 0:
            self.grenades = 10
        if GameWorld().difficulty == 1:
            self.grenades = 5

    def move(self):
        self.input_handler()

        # gravity
        self.rect.y += 2

        # lock angle to 360 degrees, prevents angles like 1591 degrees
        self.angle %= 360

        # use the base_images to rotate
        # if we rotate the normal image we get a memory leak which freezes our game within a minute
        self.image = pygame.transform.rotate(self.base_images[self.current_image], self.angle)
        self.rect = self.image.get_rect(center =(self.rect.center))

        # move our player
        self.rect.move_ip(self.direciton.x * self.velocity.x, self.direciton.y * self.velocity.y)

        #decrease our velocity over time until 0
        self.velocity.y -= 0.1
        if self.velocity.y < 0:
            self.velocity.y = 0

        self.velocity.x -= 0.1
        if self.velocity.x < 0:
            self.velocity.x = 0

    # animate our sequence of images from base_images by using current_image
    def animate(self):
        self.current_image += 1
        if self.current_image > len(self.base_images) -1:
            self.current_image = 0

    # get user input to change angle and attack
    def input_handler(self):
        self.keys = pygame.key.get_pressed()

        if self.keys[pygame.K_a]:
            self.angle += self.rotation_speed
        if self.keys[pygame.K_d]:
            self.angle -= self.rotation_speed
        if self.keys[pygame.K_w]:
            self.thrust()

        if self.can_attack:
            if self.keys[pygame.K_SPACE]:
                self.attack()
        
        if self.oldKeys[pygame.K_SPACE] and not self.keys[pygame.K_SPACE]:
            self.can_attack = True

        self.oldKeys = self.keys

    def thrust(self):
        # set player direction upwards locally
        self.direciton = pygame.math.Vector2(0, -1)
        self.direciton.rotate_ip(-self.angle)

        self.velocity = pygame.math.Vector2(8,8)

    def attack(self):
        if self.grenades > 0:
            from classes.GameWorld import GameWorld
            g = Grenade(self.rect.center, self.direciton, self.velocity)
            self.grenades -= 1
            GameWorld().grenades = self.grenades
            GameWorld().instantiate(g)
            self.can_attack = False

