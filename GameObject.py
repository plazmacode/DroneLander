import pygame
from abc import ABC, abstractclassmethod

class GameObject(pygame.sprite.Sprite, ABC):
    def __init__(self) -> None:
        self.image : pygame.image
        self.rect : pygame.rect
        self.tag = ""
        self.collision = False

    @abstractclassmethod
    def update(self):
        #self.rect.y += 1
        pass

    @abstractclassmethod
    def draw(self, screen):
        #screen.blit(self.image, self.rect)
        pass

    def onCollision(self, other):
        pass