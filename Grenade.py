import pygame
from GameObject import GameObject

class Grenade(GameObject):
    def __init__(self, x, y, vel, accel) -> None:
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Grenade.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (25, 40))
        self.rect = self.image.get_rect()
        self.rect.move_ip(x, y)
        self.velocity = vel
        self.acceleration = accel

    def update(self):
        #gravity
        self.rect.y += 5

        #use inherited velocity and acceleration to move
        self.rect.move_ip(self.velocity.x * self.acceleration, self.velocity.y * self.acceleration)
        self.acceleration -= 0.1
        if self.acceleration < 0:
            self.acceleration = 0

        if self.rect.y > 1080:
            self.explode()

    def explode(self):
        self.kill()

    def draw(self, screen):
        screen.blit(self.image, self.rect)
