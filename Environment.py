import pygame
from GameObject import GameObject

class Environment(GameObject):
    def __init__(self, name, x, y) -> None:
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(name + ".png").convert_alpha()       
        self.rect = self.image.get_rect()
        self.rect.move_ip(x, y)

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.image, self.rect)