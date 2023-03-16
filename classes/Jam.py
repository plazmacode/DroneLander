import pygame

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Jam(metaclass=Singleton):
    # used for creating noise on the screen
    # draws noise images over the screen with transparency
    def __init__(self) -> None:
        self.noise_images = self.load_noise(("./images/noise1.png", "./images/noise2.png", "./images/noise3.png"), 3)
        self.current_noise = 0
        self.alpha = 0

    def update(self):                
        # animate noise
        self.current_noise += 1
        if self.current_noise > len(self.noise_images) -1:
            self.current_noise = 0


    def draw(self, screen):
        # draw noise
        from classes.GameWorld import GameWorld
        surface = pygame.Surface((GameWorld().screen_width, GameWorld().screen_height), pygame.SRCALPHA)
        surface.blit(self.noise_images[self.current_noise], (0, 0))
        surface.set_alpha(self.alpha)
        screen.blit(surface, (0, 0))

    def load_noise(self, imagefiles, scale):
        # noise animation frames are saved in separate files, use this to load them into an array
        # afterwards the images can be scaled together
        images = []

        for i in range(0, len(imagefiles)):
            images.append(pygame.image.load(imagefiles[i]).convert_alpha())
            images[i] = pygame.transform.scale(images[i], (images[i].get_width() * scale, images[i].get_height() * scale))
        return images