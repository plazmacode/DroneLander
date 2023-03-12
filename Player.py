import pygame
import spritesheet
from GameObject import GameObject
from Grenade import Grenade

class Player(GameObject):
    def __init__(self, gameWorld) -> None:
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Drone(1).png").convert_alpha()
        self.base_image = pygame.image.load("Drone(1).png").convert_alpha()
        self.base_image = pygame.transform.scale(self.image, (125, 50))
        rects = ((0, 0, 20, 8), (20, 0, 20, 8), (40, 0, 20, 8), (60, 0, 20, 8))
        self.base_images = self.loadImages("drone-spritesheet.png", rects, (self.image.get_width() * 10, self.image.get_height() * 10))
        self.currentImage = 0
        self.rect = self.image.get_rect()
        self.rect.center = (100,450)
        self.tag = "Player"
        self.angle = 0
        self.rotation_speed = 4
        self.direciton = pygame.math.Vector2(0,0)
        self.velocity = pygame.math.Vector2(0,0)
        self.keys = pygame.key.get_pressed()
        self.oldKeys = pygame.key.get_pressed()
        self.canAttack = True
        self.gameWorld = gameWorld
        self.loadDifficulty()
        self.gameWorld.grenades = self.grenades

    def update(self):
        self.move()
        self.animate()
    
    def loadDifficulty(self):
        if self.gameWorld.difficulty == 0:
            self.grenades = 10
        if self.gameWorld.difficulty == 1:
            self.grenades = 5


    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def move(self):
        self.inputHandler()

        self.rect.y += 2

        self.angle %= 360
        self.image = pygame.transform.rotate(self.base_images[self.currentImage], self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        self.rect.move_ip(self.direciton.x * self.velocity.x, self.direciton.y * self.velocity.y)
        self.velocity.y -= 0.1
        if self.velocity.y < 0:
            self.velocity.y = 0

        self.velocity.x -= 0.1
        if self.velocity.x < 0:
            self.velocity.x = 0

    def animate(self):
        self.currentImage += 1
        if self.currentImage > len(self.base_images) -1:
            self.currentImage = 0

    def inputHandler(self):
        self.keys = pygame.key.get_pressed()

        if self.keys[pygame.K_a]:
            self.angle += self.rotation_speed
        if self.keys[pygame.K_d]:
            self.angle -= self.rotation_speed
        if self.keys[pygame.K_w]:
            self.thrust()

        if self.canAttack:
            if self.keys[pygame.K_SPACE]:
                self.attack()
        
        if self.oldKeys[pygame.K_SPACE] and not self.keys[pygame.K_SPACE]:
            self.canAttack = True

        self.oldKeys = self.keys

    def thrust(self):

        self.direciton = pygame.math.Vector2(0, -1)
        self.direciton.rotate_ip(-self.angle)

        self.velocity = pygame.math.Vector2(8,8)

    def attack(self):
        if self.grenades > 0:
            g = Grenade(self.rect.x + self.rect.width / 2, self.rect.y, self.direciton, self.velocity, self.gameWorld)
            self.grenades -= 1
            self.gameWorld.grenades = self.grenades
            from GameWorld import GameWorld
            game = GameWorld()
            # game.instantiate(g)
            self.gameWorld.instantiate(g)
            self.canAttack = False

