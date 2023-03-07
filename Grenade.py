import pygame
from GameObject import GameObject
from Explosion import Explosion

class Grenade(GameObject):
    def __init__(self, x, y, direction, velocity, gameWorld) -> None:
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Grenade.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * 10, self.image.get_height() * 10))
        self.rect = self.image.get_rect()
        self.rect.move_ip(x, y)
        self.direction = direction
        self.velocity = velocity
        self.gameWorld = gameWorld

    def update(self):
        self.move()

    def move(self):
        #gravity
        self.rect.y += 8

        #use inherited velocity and acceleration to move
        self.rect.move_ip(self.direction.x * self.velocity.x, self.direction.y * self.velocity.y)
        self.velocity.y -= 0.1
        if self.velocity.y < 0:
            self.velocity.y = 0

        self.velocity.x -= 0.05
        if self.velocity.x < 0:
            self.velocity.x = 0

        if self.rect.y > 1080:
            self.explode()

    def onCollision(self, other):
        if other.tag is "Obstacle":
            self.explode()

    def explode(self):
        self.gameWorld.instantiate(Explosion(self.rect.x, self.rect.y))
        self.kill()

    def draw(self, screen):
        screen.blit(self.image, self.rect)
