import pygame
from classes.GameObject import GameObject
from classes.Explosion import Explosion

class Grenade(GameObject):
    def __init__(self, centerInput, direction, velocity) -> None:
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("./images/Grenade.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * 10, self.image.get_height() * 10))
        self.rect = self.image.get_rect(center = centerInput)
        # self.rect.move_ip(x, y)
        self.direction = direction
        self.velocity = velocity
        self.tag = "Granade"

    def update(self):
        """
        Grenade update
        """
        self.move()

    def move(self):
        """
        Grenade movement
        """
        #gravity
        self.rect.y += 8

        #use inherited velocity and acceleration to move
        self.rect.move_ip(self.direction.x * self.velocity.x, self.direction.y * self.velocity.y)
        self.velocity.y -= 0.1
        if self.velocity.y < 0:
            self.velocity.y = 0

        self.velocity.x -= 0.05
        if self.velocity.x < 0:
            self.velocity.x = 0
        
        # remove grenades if they are outside the screen
        if self.rect.y > 1200 or self.rect.x > 2000 or self.rect.x < -50:
            self.kill()


    def on_collision(self, other):
        """
        Grenade collision
        """
        if other.tag == "Obstacle":
            self.explode()

    def explode(self):
        """
        Grenade explodes on collision
        """
        from classes.GameWorld import GameWorld
        GameWorld().instantiate(Explosion(self.rect.center, 300))
        self.kill()