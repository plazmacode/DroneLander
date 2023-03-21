import pygame

class TextField():
    def __init__(self, color, position, text, font_size, tag) -> None:
        self.base_color = color
        self.color = color
        self.position = position
        self.tag = tag
        self._font = pygame.font.SysFont(None, font_size)
        self.surface = self._font.render(str(text), True, (255, 255, 255))
        self.update_score_event = pygame.USEREVENT + 1
        self.update_endmessage_event = pygame.USEREVENT + 2

    def update(self, event_list):
        for event in event_list:
            if event.type == self.update_score_event and self.tag == "score":
                from classes.GameWorld import GameWorld
                self.surface = self._font.render("Score: " + str(GameWorld().score), True, (255, 255, 255))
            if event.type == self.update_endmessage_event and self.tag == "endmessage":
                from classes.GameWorld import GameWorld
                self.surface = self._font.render(GameWorld().endscreen_string, True, (255, 255, 255))
            if self.tag == "level":
                from classes.LevelLoader import LevelLoader
                self.surface= self._font.render("Level: " + str(LevelLoader().current_level), True, (255, 255 , 255))

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, [self.position[0] - 10 - self.surface.get_width() / 2, self.position[1] - 5 - self.surface.get_height() / 2, self.surface.get_width() + 20, self.surface.get_height() + 10])
        # center text
        x = self.position[0] - self.surface.get_width() // 2
        y = self.position[1] - self.surface.get_height() // 2

        screen.blit(self.surface, (x, y))