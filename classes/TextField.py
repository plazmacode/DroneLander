import pygame

class TextField():
    def __init__(self, color, position, text, font_size, tag) -> None:
        self.base_color = color
        self.color = color
        self.border_color = (34, 42, 50)
        self.position = position
        self.tag = tag
        self._font = pygame.font.Font("./fonts/PixeloidSans-Bold.ttf", 28)
        if tag == "title":
            self._font = pygame.font.Font("./fonts/PixeloidSans-Bold.ttf", 80)
        if tag == "lore":
            self._font = pygame.font.Font("./fonts/PixeloidSans-Bold.ttf", 16)
        self.surface = self._font.render(str(text), True, (255, 255, 255))
        self.update_score_event = pygame.USEREVENT + 1
        self.update_endmessage_event = pygame.USEREVENT + 2
        self.background_surface = pygame.Surface((self.surface.get_width() + 20, self.surface.get_height() + 10))
        if tag != "lore":
            pygame.draw.rect(self.background_surface, self.border_color, [0, 0, self.surface.get_width() + 20, self.surface.get_height() + 10])
            pygame.draw.rect(self.background_surface, self.color, [5, 5, self.surface.get_width() + 10, self.surface.get_height() + 0])
        else:
            pygame.draw.rect(self.background_surface, self.color, [0, 0, self.surface.get_width() + 20, self.surface.get_height() + 10])

    # Only called once text events actually update our surface.
    # Increases performance
    def redraw_surface(self):
        self.background_surface = pygame.Surface((self.surface.get_width() + 20, self.surface.get_height() + 10))
        if self.tag != "lore":
            pygame.draw.rect(self.background_surface, self.border_color, [0, 0, self.surface.get_width() + 20, self.surface.get_height() + 10])
            pygame.draw.rect(self.background_surface, self.color, [5, 5, self.surface.get_width() + 10, self.surface.get_height() + 0])
        else:
            pygame.draw.rect(self.background_surface, self.color, [0, 0, self.surface.get_width() + 20, self.surface.get_height() + 10])

    def update(self, event_list):
        for event in event_list:
            if event.type == self.update_score_event and self.tag == "score":
                from classes.GameWorld import GameWorld
                self.surface = self._font.render("Score: " + str(GameWorld().score), True, (255, 255, 255))
                self.redraw_surface()
            if event.type == self.update_endmessage_event and self.tag == "endmessage":
                from classes.GameWorld import GameWorld
                self.surface = self._font.render(GameWorld().endscreen_string, True, (255, 255, 255))
                self.redraw_surface()
            if self.tag == "level":
                from classes.LevelLoader import LevelLoader
                self.surface= self._font.render("Level: " + str(LevelLoader().current_level), True, (255, 255 , 255))
                self.redraw_surface()

    def draw(self, screen):
        if self.tag != "title":
            screen.blit(self.background_surface, (self.position[0] - 10 - self.surface.get_width() / 2, self.position[1] - 5 - self.surface.get_height() / 2))
        # center text
        x = self.position[0] - self.surface.get_width() // 2
        y = self.position[1] - self.surface.get_height() // 2

        screen.blit(self.surface, (x, y))