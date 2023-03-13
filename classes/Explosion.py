import pygame
from classes.GameObject import GameObject

class Explosion(GameObject):
    def __init__(self, centerInput, size) -> None:
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        rects = (
            (0,  0, 32, 32), (32,  0, 32, 32), (64,  0, 32, 32), (96,  0, 32, 32),
            (0, 32, 32, 32), (32, 32, 32, 32), (64, 32, 32, 32), (96, 32, 32, 32),
            (0, 64, 32, 32), (32, 64, 32, 32), (64, 64, 32, 32), (96, 64, 32, 32),
            (0, 96, 32, 32), (32, 96, 32, 32), (64, 96, 32, 32), (96, 96, 32, 32)
            )
        self.scale = size
        self.images = self.load_images("./images/explosion-spritesheet.png", rects, (self.scale, self.scale))
        self.currentImage = 0
        self.image = self.images[self.currentImage]
        self.rect = self.images[self.currentImage].get_rect(center = centerInput)
        # self.rect.move_ip(x, y - 64)

        # self.rect = self.image.get_rect(center = (x, y))


        self.tag = "Explosion"

    def update(self):
        self.animate()

    def animate(self):
        self.currentImage += 1
        if self.currentImage > len(self.images) -1:
            self.currentImage = 0
            self.kill()
        self.image = self.images[self.currentImage]