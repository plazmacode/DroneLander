import pygame
from classes.Spritesheet import Spritesheet
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
        from classes.GameWorld import GameWorld
        screen.blit(self.image, pygame.Rect(self.rect.x - GameWorld().camera_x, self.rect.y, self.rect.width, self.rect.height))

    def on_collision(self, other):
        pass
    
    # loads a spritesheet to use for animations
    # returns an array of images from the spritesheet
    def loadImages(self, imagefile, rects, scale):
        ss = Spritesheet(imagefile)
        images = []
        images = ss.source_rects(rects)

        # fix image scale
        for i in range(0, len(images)):
            images[i] = pygame.transform.scale(images[i], scale)
        return images