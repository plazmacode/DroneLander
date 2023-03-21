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
        self.noise_images = self.load_noise(("./images/noise1small.png", "./images/noise2small.png", "./images/noise3small.png"), 6)
        self.current_noise = 0
        self.alpha = 0
        self.active_jammers = []

    def update(self):                
        # animate noise
        self.current_noise += 1
        if self.current_noise > len(self.noise_images) -1:
            self.current_noise = 0

        if len(self.active_jammers) > 0:
            self.alpha = 128
        else:
            self.alpha = 0


    def remove(self, jammer):
        if jammer in self.active_jammers:
                self.active_jammers.remove(jammer)

    def draw(self, screen):
        # draw noise
        if(self.alpha != 0):
            screen.blit(self.noise_images[self.current_noise], (0, 0))

    def load_noise(self, imagefiles, scale):
        # noise animation frames are saved in separate files, use this to load them into an array
        # afterwards the images can be scaled together
        from classes.GameWorld import GameWorld

        images = []

        for i in range(0, len(imagefiles)):
            images.append(pygame.image.load(imagefiles[i]).convert_alpha())
            images[i] = pygame.transform.scale(images[i], (images[i].get_width() * scale, images[i].get_height() * scale))
            surface = pygame.Surface((GameWorld().screen_width, GameWorld().screen_height), pygame.SRCALPHA)
            surface.blit(images[i], (0,0))
            surface.set_alpha(128)
            images[i] = surface
        return images