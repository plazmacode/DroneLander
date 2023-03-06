import pygame
import spritesheet
from abc import ABC, abstractclassmethod

class GameObject(pygame.sprite.Sprite, ABC):
    def __init__(self) -> None:
        self.image : pygame.image
        self.rect : pygame.rect
        self.tag = ""
        self.collision = False

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        pass

    def onCollision(self, other):
        pass

    def loadImages(self, imagefile, rects, scale):
        ss = spritesheet.spritesheet(imagefile)
        images = []
        images = ss.sourceRects(rects)

        for i in range(0, len(images)):
            images[i] = pygame.transform.scale(images[i], scale)
        return images