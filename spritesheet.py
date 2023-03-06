import pygame

class spritesheet():
    def __init__(self, imagefile) -> None:
        self.spritesheet = pygame.image.load(imagefile).convert_alpha()

    def sourceRect(self, rect):
        rect = pygame.Rect(rect)
        image = pygame.Surface(rect.size, pygame.SRCALPHA).convert_alpha()
        image.blit(self.spritesheet, (0, 0), rect)
        return image
    
    def sourceRects(self, rects):
        return [self.sourceRect(rect) for rect in rects]