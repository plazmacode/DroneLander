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
        self.text = text
        self._font = pygame.font.Font("./fonts/PixeloidSans-Bold.ttf", 22)
        self.text_surface = self._font.render(str(text), True, (255, 255, 255))
        self.action = action
        self.old_mouse_state = pygame.MOUSEBUTTONUP
        self.button_surface = pygame.Surface((self.rect.width, self.rect.height))
        self.new_color = color
        self.border_color = (34, 42, 50)
        pygame.draw.rect(self.button_surface, self.border_color, [0, 0, self.rect.width, self.rect.height])
        pygame.draw.rect(self.button_surface, self.color, [5, 5, self.rect.width -10, self.rect.height -10])


    def redraw(self):
        """
        param text_change: bool
        """
        if self.new_color != self.color:            
            self.color = self.new_color
            
            lineData = [int(s) for s in self.text.split() if s.isdigit()]
            if len(lineData) != 0:
                from classes.GameWorld import GameWorld
                if self.color == self.hover_color:
                    GameWorld().level_select = lineData[0]
                else:
                    GameWorld().level_select = 0
                level_select_event = pygame.event.Event(pygame.USEREVENT + 3)
                pygame.event.post(level_select_event)

            pygame.draw.rect(self.button_surface, self.border_color, [0, 0, self.rect.width, self.rect.height])
            pygame.draw.rect(self.button_surface, self.color, [5, 5, self.rect.width -10, self.rect.height -10])

    def update(self, event_list):
        from classes.GameWorld import GameWorld
        #keyboard controls

        # if mouse position inside button rectangle
        mouse = pygame.mouse
        if self.rect.collidepoint(mouse.get_pos()[0], mouse.get_pos()[1]):
            # set hover color on button
            self.new_color = self.hover_color
            self.redraw()
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
            self.new_color = self.base_color
            self.redraw()

    def draw(self, screen):
        # draw button rectangle
        screen.blit(self.button_surface, (self.rect.x, self.rect.y))
        # center text
        x = self.rect.x + (self.rect.width - self.text_surface.get_width()) // 2
        y = self.rect.y + (self.rect.height - self.text_surface.get_height()) // 2
        # draw button text
        screen.blit(self.text_surface, (x, y))