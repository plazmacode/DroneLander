import pygame
from GameObject import GameObject

class Grenade(GameObject):
    def __init__(self) -> None:
        super().__init__()
        self.image = pygame.image.load("grenade.png").convert_alpha
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.y += 1

    def draw(self, screen):
        screen.blit(self.image, self.rect)