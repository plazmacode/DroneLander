import pygame

class TextField():
    def __init__(self, color, rect, text, font_size) -> None:
        self.base_color = color
        self.color = color
        self.rect = rect
        self._font = pygame.font.SysFont(None, font_size)
        self.surface = self._font.render(str(text), True, (255, 255, 255))

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, [self.rect.x, self.rect.y, self.rect.width, self.rect.height])
        #center text
        x = self.rect.x + (self.rect.width - self.surface.get_width()) // 2
        y = self.rect.y + (self.rect.height - self.surface.get_height()) // 2
        screen.blit(self.surface, (x, y))