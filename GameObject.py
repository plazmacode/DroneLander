import pygame
import spritesheet
from abc import ABC, abstractclassmethod

class GameObject(pygame.sprite.Sprite, ABC):
    def __init__(self) -> None:
        self.image : pygame.image
        self.rect : pygame.rect
        self.tag = ""
        self.collision = False
        # self.origin = (self.rect.x / 2, self.rect.y / 2)

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        pass

    def on_collision(self, other):
        pass

    def loadImages(self, imagefile, rects, scale):
        ss = spritesheet.spritesheet(imagefile)
        images = []
        images = ss.source_rects(rects)

        for i in range(0, len(images)):
            images[i] = pygame.transform.scale(images[i], scale)
        return images