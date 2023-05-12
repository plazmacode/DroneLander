import pygame
from classes.GameObject import GameObject

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]
    
# Marker class for drawing a marker pointing to the target objective
class Marker(metaclass=Singleton):
    def __init__(self) -> None:
        self.image = pygame.image.load("./images/marker.png")
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * 10, self.image.get_height() * 10)).convert_alpha()
        self.base_image = self.image
        self.image_left = pygame.transform.rotate(self.base_image, 90)
        self.image_right = pygame.transform.rotate(self.base_image, -90)

        self.rect = self.image.get_rect()
        self.main_objective : GameObject
        self.brick : GameObject

    def update(self):
        from classes.GameWorld import GameWorld
        #check if main_objective_object is set in GameWorld
        if hasattr(GameWorld(), 'main_objective_object'):
            # main objective not destroyed
            if GameWorld().main_objective_completed is False:
                self.main_objective = GameWorld().main_objective_object
                self.set_marker_to_target(self.main_objective)
            else:
                self.brick = GameWorld().brick
                self.set_marker_to_target(self.brick)

    def set_marker_to_target(self, target):
        """
        sets marker position to target
        """
        from classes.GameWorld import GameWorld
        #marker left
        if target.rect.x < 0:
            self.image = self.image_right
            self.rect = (100, GameWorld().screen_height / 2 - self.image.get_height() / 2)
        #marker right
        elif target.rect.x > GameWorld().screen_width:
            self.image = self.image_left
            self.rect = (GameWorld().screen_width - 100, GameWorld().screen_height / 2 - self.image.get_height() / 2)
        # move marker to main_objective on screen
        else:
            self.image = self.base_image
            self.rect = (target.rect.x + target.rect.width / 2 - self.image.get_width() / 2, target.rect.y - 80)

    def draw(self, screen):
        screen.blit(self.image, self.rect)