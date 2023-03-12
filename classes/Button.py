import pygame
from ButtonActions import ButtonActions

class Button():
    def __init__(self, color, hover_color, rect, text, action) -> None:
        self.base_color = color
        self.color = color
        self.hover_color = hover_color
        self.rect = rect
        self._font = pygame.font.SysFont(None, 48)
        self.surface = self._font.render(str(text), True, (255, 255, 255))
        self.action = action
        self.old_mouse_state = pygame.MOUSEBUTTONUP

    def update(self, event_list):
        #if mouse position inside button rectangle
        mouse = pygame.mouse
        if self.rect.collidepoint(mouse.get_pos()[0], mouse.get_pos()[1]):
            self.color = self.hover_color
            for event in event_list:
                if event.type == pygame.MOUSEBUTTONUP and self.old_mouse_state == pygame.MOUSEBUTTONDOWN:
                    ButtonActions().run(self.action, self)
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.old_mouse_state = pygame.MOUSEBUTTONDOWN

                if event.type == pygame.MOUSEBUTTONUP:
                    self.old_mouse_state = pygame.MOUSEBUTTONUP
        else:
            self.color = self.base_color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, [self.rect.x, self.rect.y, self.rect.width, self.rect.height])
        #center text
        x = self.rect.x + (self.rect.width - self.surface.get_width()) // 2
        y = self.rect.y + (self.rect.height - self.surface.get_height()) // 2
        screen.blit(self.surface, (x, y))