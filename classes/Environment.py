import pygame
from classes.GameObject import GameObject
from classes.Explosion import Explosion

class Environment(GameObject):
    def __init__(self, name, position, tag_input) -> None:
        """
        __init__ override for loading environment objects into the game 

        :param name: Name of the sprite this object should use, saves adding file path and extension every time
        :param position: Position where the object is placed
        :param tag_input: The tag used for this object when handling collisions
        """
        super().__init__()   # Brings sprite, rect etc. fields from parent class
        pygame.sprite.Sprite.__init__(self)   # Initializes the visuals of this object
        
        # Grab values from arguments
        self.name = name
        self.tag = tag_input

        self.image = pygame.image.load("./images/" + name + ".png").convert_alpha()   # Extend the name to find actual file location
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * 10, self.image.get_height() * 10))   # Pixel art is drawn at actual pixel size, scaled up here to be poperly visible
        self.rect = self.image.get_rect(center = position)   # Centers the image on input position, instead of the top left corner
        self.mask = pygame.mask.from_surface(self.image)

    # Poor use currently, only contains functionality for the ammo dumps, that could be separated out into a child class or simmilar instead
    def on_collision(self, other):
        """
        Collision behaviour specific to environment objects

        :param other: Not manually specified, lets the this object know what instance it colloded with. Used to extract tags
        """
        # If an ammo dump touches an explosion, it is destroyed leaving a blast decal
        if other.tag == "Explosion":
            if self.name == "AmmoDump(Shells)":
                # Plays a larger explosion for the ammo dump itself
                from classes.GameWorld import GameWorld
                GameWorld().instantiate(Explosion(self.rect.center, 600))

                # Replaces itself with and moves the blast decal
                ### Very fragile implementation, should be improved
                self.name = "DetonationDecal"
                GameWorld().score += 200
                self.image = pygame.image.load("./images/" + self.name + ".png").convert_alpha()   
                self.image = pygame.transform.scale(self.image, (self.image.get_width() * 10, self.image.get_height() * 10))  
                self.rect = self.image.get_rect(center = (self.rect.centerx, self.rect.centery + 100))
    
    
    ### ENVIRONMENT OBJECTS HAVE NO CURRENT FUNCTIONALITY RELYING ON UPDATE
    ### WAS PURELY USED FOR DEBUGGING
    ### SHOULD BE EMPTIED AND READDED IF UPDATE FUNCTIONALITY BECOMES NEEDED
    # def update(self):
    #     """
    #     update override for environment objects, used for debugging
    #     """
    #     keys = pygame.key.get_pressed()

    #     if keys[pygame.K_b] and self.name == "AmmoDump(Shells)":
    #         self.image = pygame.image.load("./images/DetonationDecal.png").convert_alpha()   
    #         self.image = pygame.transform.scale(self.image, (self.image.get_width() * 10, self.image.get_height() * 10))  
    #         self.rect = self.image.get_rect(center = (self.x, self.y + 100))