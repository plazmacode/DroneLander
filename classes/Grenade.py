import pygame
from classes.GameObject import GameObject
from classes.Explosion import Explosion

class Grenade(GameObject):
    def __init__(self, centerInput, velocity_x, velocity_y) -> None:
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("./images/Grenade.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * 10, self.image.get_height() * 10))
        self.rect = self.image.get_rect(center = centerInput)
        # self.rect.move_ip(x, y)
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.tag = "Granade"
        self.mask = pygame.mask.from_surface(self.image)

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
        self.rect.move_ip(self.velocity_x, self.velocity_y)

        if self.velocity_y < 0:
            self.velocity_y += 0.25
        elif self.velocity_y > 0:
            self.velocity_y -= 0.25

        if self.velocity_x < 0:
            self.velocity_x += 0.1
        elif self.velocity_x > 0:
            self.velocity_x -= 0.1
        
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