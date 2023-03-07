import pygame
from ButtonActions import ButtonActions

class Button():
    def __init__(self, color, hoverColor, rect, text, gameWorld) -> None:
        self.baseColor = color
        self.color = color
        self.hoverColor = hoverColor
        self.rect = rect
        self._font = pygame.font.SysFont(None, 48)
        self.surface = self._font.render(str(text), True, (255, 255, 255))
        self.text = text
        self.gameWorld = gameWorld

    def update(self):
        #if mouse position inside button rectangle
        mouse = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse[0], mouse[1]):
            self.color = self.hoverColor
            if pygame.mouse.get_pressed()[0]:
                ButtonActions().run(self.text, self.gameWorld)
        else:
            self.color = self.baseColor

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, [self.rect.x, self.rect.y, self.rect.width, self.rect.height])
        #center text
        x = self.rect.x + (self.rect.width - self.surface.get_width()) // 2
        y = self.rect.y + (self.rect.height - self.surface.get_height()) // 2
        screen.blit(self.surface, (x, y))