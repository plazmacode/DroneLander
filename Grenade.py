import pygame
from GameObject import GameObject

class Grenade(GameObject):
    def __init__(self, x, y) -> None:
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Grenade.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * 10, self.image.get_height() * 10))  
        self.rect = self.image.get_rect()
        self.rect.move_ip(x, y)

    def update(self):
        self.rect.y += 1

    def draw(self, screen):
        screen.blit(self.image, self.rect)