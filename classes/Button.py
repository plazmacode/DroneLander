import pygame
from classes.ButtonActions import ButtonActions

class Button():
    def __init__(self, color, hover_color, rect, text, action) -> None:
        """
            Base __init__ with fields all buttons are expected to use

        """
        self.base_color = color
        self.color = color
        self.hover_color = hover_color
        self.rect = rect
        self._font = pygame.font.SysFont(None, 40)
        self.text_surface = self._font.render(str(text), True, (255, 255, 255))
        self.action = action
        self.old_mouse_state = pygame.MOUSEBUTTONUP
        # self.button_surface = pygame.

    def update(self, event_list):
        #if mouse position inside button rectangle
        mouse = pygame.mouse
        if self.rect.collidepoint(mouse.get_pos()[0], mouse.get_pos()[1]):
            # set hover color on button
            self.color = self.hover_color
            for event in event_list:
                # When mouse released after mouse pressed
                if event.type == pygame.MOUSEBUTTONUP and self.old_mouse_state == pygame.MOUSEBUTTONDOWN:
                    # run ButtonActions with this buttons action
                    ButtonActions().run(self.action, self)
                    
                # update old mouse state
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.old_mouse_state = pygame.MOUSEBUTTONDOWN

                if event.type == pygame.MOUSEBUTTONUP:
                    self.old_mouse_state = pygame.MOUSEBUTTONUP
        else:
            # set color to base color when not hovering
            self.color = self.base_color

    def draw(self, screen):
        # draw button rectangle
        pygame.draw.rect(screen, self.color, [self.rect.x, self.rect.y, self.rect.width, self.rect.height])
        # center text
        x = self.rect.x + (self.rect.width - self.text_surface.get_width()) // 2
        y = self.rect.y + (self.rect.height - self.text_surface.get_height()) // 2
        # draw button text
        screen.blit(self.text_surface, (x, y))