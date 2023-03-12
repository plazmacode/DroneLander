import pygame
from GameObject import GameObject
from Explosion import Explosion

class Environment(GameObject):
    def __init__(self, name, centerInput) -> None:
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.tag = "Obstacle"

        self.image = pygame.image.load(name + ".png").convert_alpha()   
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * 10, self.image.get_height() * 10))    
        self.rect = self.image.get_rect(center = centerInput)
        # self.rect.move_ip(x, y)

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_b] and self.name == "AmmoDump(Shells)":
            self.image = pygame.image.load("DetonationDecal.png").convert_alpha()   
            self.image = pygame.transform.scale(self.image, (self.image.get_width() * 10, self.image.get_height() * 10))  
            self.rect = self.image.get_rect(center = (self.x, self.y + 100))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def onCollision(self, other):
        if other.tag == "Explosion":
            if self.name == "AmmoDump(Shells)":
                self.name = "DetonationDecal"
                from GameWorld import GameWorld
                GameWorld().instantiate(Explosion(self.rect.center, 600))

                self.image = pygame.image.load(self.name + ".png").convert_alpha()   
                self.image = pygame.transform.scale(self.image, (self.image.get_width() * 10, self.image.get_height() * 10))  
                self.rect = self.image.get_rect(center = (self.rect.centerx, self.rect.centery + 100))