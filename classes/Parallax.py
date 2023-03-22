import pygame
from classes.Singleton import Singleton
# from profilehooks import profile

class Parallax(metaclass = Singleton):
    def __init__(self) -> None:
        self.background_image = pygame.image.load("./images/Sky.png").convert_alpha()
        self.background_image = pygame.transform.scale(self.background_image, (1920, 1080))
        self.layer1 = pygame.image.load("./images/background1.png")
        self.layer2 = pygame.image.load("./images/background2.png")
        self.layer3 = pygame.image.load("./images/background3.png")

        scaleing = 0.83

        self.layer1 = pygame.transform.scale(self.layer1, (self.layer1.get_width() * scaleing, self.layer1.get_height() * scaleing)).convert_alpha()
        self.layer2 = pygame.transform.scale(self.layer2, (self.layer2.get_width() * scaleing, self.layer2.get_height() * scaleing)).convert_alpha()
        self.layer3 = pygame.transform.scale(self.layer3, (self.layer3.get_width() * scaleing, self.layer3.get_height() * scaleing)).convert_alpha()

        self.layer1_scroll = 0
        self.layer2_scroll = 0
        self.layer3_scroll = 0

        self.cloud_speed = 1
        self.layer1_scroll_speed = 0.2
        self.layer2_scroll_speed = 0.4
        self.layer3_scroll_speed = 0.8

        self.layer1_height = 0
        self.layer2_height = 450
        self.layer3_height = 702

        self.tiles = 3

    def reset_position(self):
        self.layer1_scroll = 0
        self.layer2_scroll = 0
        self.layer3_scroll = 0

    def update(self):
        """
        moves the clouds
        """
        self.layer1_scroll -= self.cloud_speed

    def move_parallax(self, x):
        """
        moves the parallax by using player movement

        param x: player x movement
        """
        self.layer1_scroll -= self.layer1_scroll_speed * x
        self.layer2_scroll -= self.layer2_scroll_speed * x
        self.layer3_scroll -= self.layer3_scroll_speed * x

        if self.layer1_scroll > self.layer1.get_width():
            self.layer1_scroll -= self.layer1.get_width()

        if self.layer2_scroll > self.layer2.get_width():
            self.layer2_scroll -= self.layer2.get_width()

        if self.layer3_scroll > self.layer3.get_width():
            self.layer3_scroll -= self.layer3.get_width()
        
        if self.layer1_scroll < -self.layer1.get_width():
            self.layer1_scroll += self.layer1.get_width()

        if self.layer2_scroll < -self.layer2.get_width():
            self.layer2_scroll += self.layer2.get_width()

        if self.layer3_scroll < -self.layer3.get_width():
            self.layer3_scroll += self.layer3.get_width()

    # @profile
    def draw(self, screen):
        from classes.GameWorld import GameWorld
        screen.blit(self.background_image, (0, 0))
        for i in range (0, self.tiles):
            if GameWorld().game_state == "MENU":

                # screen.blit(self.layer1, (-self.layer1.get_width() + self.layer1.get_width() * i + self.layer1_scroll, self.layer1_height))
                screen.blit(self.layer2, (-self.layer2.get_width() + self.layer2.get_width() * i + self.layer2_scroll, self.layer2_height))
                screen.blit(self.layer3, (-self.layer3.get_width() + self.layer3.get_width() * i + self.layer3_scroll, self.layer3_height))
            else:
                screen.blit(self.layer1, (-self.layer1.get_width() + self.layer1.get_width() * i + self.layer1_scroll, self.layer1_height))
                screen.blit(self.layer2, (-self.layer2.get_width() + self.layer2.get_width() * i + self.layer2_scroll, self.layer2_height))
                screen.blit(self.layer3, (-self.layer3.get_width() + self.layer3.get_width() * i + self.layer3_scroll, self.layer3_height))