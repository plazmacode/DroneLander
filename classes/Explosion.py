import pygame
from classes.GameObject import GameObject

class Explosion(GameObject):
    def __init__(self, position, size) -> None:
        """
        __init__ override for loading the explosion effect

        :param position: The position the explosion appears at
        :param size: How large the displayed explosion is
        """
        super().__init__()   # Brings sprite, rect etc. fields from parent class
        pygame.sprite.Sprite.__init__(self)   # Initializes the visuals of this object
        self.tag = "Explosion"

        # Set visuals
        # The positions of each sprite, on the sprite sheet used to animate the effect
        rects = (
            ( 0,  0, 32, 32), (32,  0, 32, 32), (64,  0, 32, 32), (96,  0, 32, 32),
            ( 0, 32, 32, 32), (32, 32, 32, 32), (64, 32, 32, 32), (96, 32, 32, 32),
            ( 0, 64, 32, 32), (32, 64, 32, 32), (64, 64, 32, 32), (96, 64, 32, 32),
            ( 0, 96, 32, 32), (32, 96, 32, 32), (64, 96, 32, 32), (96, 96, 32, 32)
            )
        self.scale = size
        self.images = self.load_images("./images/explosion-spritesheet.png", rects, (self.scale, self.scale))
        self.currentImage = 0
        self.image = self.images[self.currentImage]
        self.rect = self.images[self.currentImage].get_rect(center = position)

        # Set audio
        self.explosion_sound = pygame.mixer.Sound("./sounds/explosion.wav")
        from classes.MenuHandler import MenuHandler
        if MenuHandler().sound_enabled:
            pygame.mixer.Sound.play(self.explosion_sound)

    # Runs the animation
    def update(self):
        self.animate()

    def animate(self):
        # Runs through the images collection one at a time, killing itself when done
        self.currentImage += 1
        if self.currentImage > len(self.images) -1:
            self.currentImage = 0
            self.kill()
        self.image = self.images[self.currentImage]