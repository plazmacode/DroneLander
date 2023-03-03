import pygame
from GameObject import GameObject

class Player(GameObject):
    def __init__(self) -> None:
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("player.png").convert()
        self.base_image = pygame.image.load("player.png").convert()
        self.rect = self.image.get_rect()
        self.rect.center = (100,450)
        self.tag = "Player"
        self.angle = 0
        self.rotation_speed = 4

    def update(self):
        self.move()
        

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def move(self):
        self.rect.y += 1

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.angle += self.rotation_speed
        elif keys[pygame.K_d]:
            self.angle -= self.rotation_speed
        elif keys[pygame.K_w]:
            self.thrust()
        elif keys[pygame.K_SPACE]:
            self.attack(self)
        self.angle %= 360
        self.image = pygame.transform.rotate(self.base_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def thrust(self):
        pass

    def attack(self):
        pass
