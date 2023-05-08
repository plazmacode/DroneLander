import pygame
from classes.GameObject import GameObject

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]
    
# Jam class improved with profilehooks to run a profile on the GameWorld draw() method
# The blit method had a cumulative time of 26.3, while Jam was 15.5
# After optimisation the cumulative was 25 and, while Jam was 8.1
# Code was optimised by loading images as transparent, instead of redrawing them to a surface each frame
class Marker(metaclass=Singleton):
    # used for creating noise on the screen
    # draws noise images over the screen with transparency
    def __init__(self) -> None:
        self.image = pygame.image.load("./images/marker.png")
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * 5, self.image.get_height() * 5)).convert_alpha()
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
                self.marker_on_objective()
            else:
                self.marker_on_land()

    def marker_on_objective(self):
        from classes.GameWorld import GameWorld
        self.main_objective = GameWorld().main_objective_object
        self.set_marker_to_target(self.main_objective)
    
    def set_marker_to_target(self, target):
        from classes.GameWorld import GameWorld
        #marker left
        if target.rect.x < 0:
            self.image = self.image_right
            self.rect = (100, GameWorld().screen_height / 2 - self.image.get_height() / 2)
        #marker right
        elif target.rect.x > GameWorld().screen_width:
            self.image = self.image_left
            self.rect = (GameWorld().screen_width - 100, GameWorld().screen_height / 2 - self.image.get_height() / 2)
        else:
            # move marker to main_objective on screen
            self.image = self.base_image
            self.rect = (target.rect.x + target.rect.width / 2 - self.image.get_width() / 2, target.rect.y - 80)

    def marker_on_land(self):
        from classes.GameWorld import GameWorld
        self.brick = GameWorld().brick

        self.set_marker_to_target(self.brick)        

    def draw(self, screen):
        screen.blit(self.image, self.rect)