import pygame
from classes.Spritesheet import Spritesheet
from abc import ABC, abstractclassmethod

class GameObject(pygame.sprite.Sprite, ABC):
    def __init__(self) -> None:
        """
        Base __init__ with fields all game objects are expected to use
        """
        self.image : pygame.image
        self.rect : pygame.rect
        self.tag = ""   # Tag system used for collisions, identifies what collided so the correct response can be run
        self.collision = False
        self.main_objective = False

    # Methods all game objects are expected to define
    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def on_collision(self, other):
        # Tells the game you can return to land now
        if  self.main_objective == True:
            from classes.GameWorld import GameWorld
            GameWorld().main_objective_completed = True
            GameWorld().endscreen_string = "MISSION COMPLETE DRONE LOST"
            update_endmessage_event = pygame.event.Event(pygame.USEREVENT + 2)
            pygame.event.post(update_endmessage_event)
    
    # Loads a spritesheet to use for animations
    # Returns an array of images from the spritesheet
    def load_images(self, imagefile, rects, scale):
        sprite_sheet = Spritesheet(imagefile)
        images = []
        images = sprite_sheet.source_rects(rects)

        # Fix image scale
        for i in range(0, len(images)):
            images[i] = pygame.transform.scale(images[i], scale)
        return images
    
    # Imagefiles is a tuple with strings that hold the path to the images to be loaded
    def load_images2(self, imagefiles, scale):
        images = []

        for i in range(0, len(imagefiles)):
            images.append(pygame.image.load(imagefiles[i]).convert_alpha())
            images[i] = pygame.transform.scale(images[i], (images[i].get_width() * scale, images[i].get_height() * scale))
        return images
