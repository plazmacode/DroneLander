import pygame
from GameObject import GameObject

class Environment(GameObject):
    def __init__(self, name, x, y) -> None:
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.tag = "Obstacle"

        self.x = x
        self.y = y
        self.image = pygame.image.load(name + ".png").convert_alpha()   
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * 10, self.image.get_height() * 10))    
        self.rect = self.image.get_rect()
        self.rect.move_ip(x, y)

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_b] and self.name == "AmmoDump(Shells)":
            self.image = pygame.image.load("DetonationDecal.png").convert_alpha()   
            self.image = pygame.transform.scale(self.image, (self.image.get_width() * 10, self.image.get_height() * 10))  
            self.rect = self.image.get_rect()
            self.rect.move_ip(self.x - 150, self.y + 150)

    def draw(self, screen):
        screen.blit(self.image, self.rect)