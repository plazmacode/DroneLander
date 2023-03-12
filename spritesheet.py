import pygame

class spritesheet():
    def __init__(self, imagefile) -> None:
        self.spritesheet = pygame.image.load(imagefile).convert_alpha()

    def source_rect(self, rect):
        rect = pygame.Rect(rect)
        image = pygame.Surface(rect.size, pygame.SRCALPHA).convert_alpha()
        image.blit(self.spritesheet, (0, 0), rect)
        return image
    
    def source_rects(self, rects):
        return [self.source_rect(rect) for rect in rects]