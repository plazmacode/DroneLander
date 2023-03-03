import pygame

class GameObject(pygame.sprite.Sprite):
    def __init__(self) -> None:
        self.image = pygame.image.load("drone (3).png").convert()
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (2000, 800))

    def update(self):
        #self.rect.y += 1
        pass

    def draw(self, screen):
        screen.blit(self.image, self.rect)