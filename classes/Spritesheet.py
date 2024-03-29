import pygame

class Spritesheet():
    def __init__(self, imagefile) -> None:
        self.spritesheet = pygame.image.load(imagefile)

    def source_rect(self, rect):
        rect = pygame.Rect(rect)
        image = pygame.Surface(rect.size, pygame.SRCALPHA)
        image.blit(self.spritesheet, (0, 0), rect)
        return image
    
    def source_rects(self, rects):
        return [self.source_rect(rect) for rect in rects]