import pygame
from ButtonActions import ButtonActions

class Button():
    def __init__(self, color, hoverColor, rect, text, action) -> None:
        self.baseColor = color
        self.color = color
        self.hoverColor = hoverColor
        self.rect = rect
        self._font = pygame.font.SysFont(None, 48)
        self.surface = self._font.render(str(text), True, (255, 255, 255))
        self.action = action
        self.oldMouseState = pygame.MOUSEBUTTONUP

    def update(self, event_list):
        #if mouse position inside button rectangle
        mouse = pygame.mouse
        if self.rect.collidepoint(mouse.get_pos()[0], mouse.get_pos()[1]):
            self.color = self.hoverColor
            for event in event_list:
                if event.type == pygame.MOUSEBUTTONUP and self.oldMouseState == pygame.MOUSEBUTTONDOWN:
                    ButtonActions().run(self.action, self)
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.oldMouseState = pygame.MOUSEBUTTONDOWN

                if event.type == pygame.MOUSEBUTTONUP:
                    self.oldMouseState = pygame.MOUSEBUTTONUP
        else:
            self.color = self.baseColor

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, [self.rect.x, self.rect.y, self.rect.width, self.rect.height])
        #center text
        x = self.rect.x + (self.rect.width - self.surface.get_width()) // 2
        y = self.rect.y + (self.rect.height - self.surface.get_height()) // 2
        screen.blit(self.surface, (x, y))