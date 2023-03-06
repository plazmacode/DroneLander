import pygame
from GameObject import GameObject
from Grenade import Grenade

class Player(GameObject):
    def __init__(self) -> None:
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("player.png").convert_alpha()
        self.base_image = pygame.image.load("player.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (100,450)
        self.tag = "Player"
        self.angle = 0
        self.rotation_speed = 4
        self.velocity = pygame.math.Vector2(0,0)
        self.accel = 0

    
    def update(self):
        self.move()
        

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def move(self):
        self.rect.y += 1

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.angle += self.rotation_speed
        if keys[pygame.K_d]:
            self.angle -= self.rotation_speed
        if keys[pygame.K_w]:
            self.thrust()
        if keys[pygame.K_SPACE]:
            self.attack()
        self.angle %= 360
        self.image = pygame.transform.rotate(self.base_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        self.rect.move_ip(self.velocity.x * self.accel, self.velocity.y * self.accel)
        self.accel -= 0.1
        if self.accel < 0:
            self.accel = 0

    def thrust(self):

        self.velocity = pygame.math.Vector2(0, -1)
        self.velocity.rotate_ip(-self.angle)

        self.accel = 5

    def attack(self):
        from GameWorld import GameWorld
        g = GameWorld()
        g.gameObjects.add(Grenade(self.rect.x + self.rect.width / 2, self.rect.y))
