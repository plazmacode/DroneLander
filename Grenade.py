import pygame
from GameObject import GameObject
from Explosion import Explosion

class Grenade(GameObject):
    def __init__(self, x, y, vel, accel, gameWorld) -> None:
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Grenade.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (25, 40))
        self.rect = self.image.get_rect()
        self.rect.move_ip(x, y)
        self.velocity = vel
        self.acceleration = accel
        self.gameWorld = gameWorld

    def update(self):
        self.move()

    def move(self):
        #gravity
        self.rect.y += 5

        #use inherited velocity and acceleration to move
        self.rect.move_ip(self.velocity.x * self.acceleration, self.velocity.y * self.acceleration)
        self.acceleration -= 0.1
        if self.acceleration < 0:
            self.acceleration = 0

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
