import pygame
from classes.GameObject import GameObject
from classes.Player import Player

class Jammer(GameObject):
    def __init__(self, centerInput) -> None:
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("./images/HUH.png").convert_alpha()  
        self.rect = self.image.get_rect(center = centerInput)
        self.tag = "Jammer"
        self.attack_range = 500
        self.attack_cooldown = 1500
        self.current_attack_time = 0
        self.attacking = False

    def update(self):
        self.attack()
    
    def attack(self):
        from classes.GameWorld import GameWorld


        distance = pygame.math.Vector2(self.rect.x - GameWorld().camera_x, self.rect.y).distance_to(Player().rect.center)
        if distance <= self.attack_range:
            if self.attacking == False:
                self.attack_start = pygame.time.get_ticks()
                self.attacking = True
            self.current_attack_time = (pygame.time.get_ticks()-self.attack_start)
        else:
            Player().can_input = True
            self.attacking = False
            self.current_attack_time = 0

        if self.current_attack_time >= self.attack_cooldown:
            Player().can_input = False

        GameWorld().jamming = self.attacking
        
    def draw(self, screen):
        from classes.GameWorld import GameWorld
        screen.blit(self.image, pygame.Rect(self.rect.x - GameWorld().camera_x, self.rect.y, self.rect.width, self.rect.height))

        
        #jammer debug circle
        surface = pygame.Surface((GameWorld().screen_width, GameWorld().screen_height), pygame.SRCALPHA)
        pygame.draw.circle(surface, (255, 0, 0, 50), (self.rect.x - GameWorld().camera_x, self.rect.y), 500)
        screen.blit(surface, (0, 0))

    def on_collision(self, other):
        if other.tag == "Explosion":
            self.kill()
