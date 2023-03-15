import pygame
from classes.GameObject import GameObject
from classes.Player import Player
from classes.Jam import Jam

class Jammer(GameObject):
    def __init__(self, centerInput) -> None:
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("./images/Jammer.png").convert_alpha()  
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * 10, self.image.get_height() * 10))
        self.rect = self.image.get_rect(center = centerInput)
        self.tag = "Jammer"
        self.attack_range = 500
        self.attack_cooldown = 1500
        self.current_attack_time = 0
        self.attacking = False
        self.jam_sound = pygame.mixer.Sound("./sounds/noise2.wav")
        self.is_alive = True

    def update(self):
        self.attack()
    
    def attack(self):
        from classes.GameWorld import GameWorld

        # get distance between jammer and player
        distance = pygame.math.Vector2(self.rect.x - GameWorld().camera_x, self.rect.y).distance_to(Player().rect.center)

        # player inside jammer range
        if distance <= self.attack_range and self.is_alive == True:
            if self.attacking == False:
                self.attack_start = pygame.time.get_ticks()
                self.attacking = True
                Jam().alpha = 128 # DEBUG
                from classes.MenuHandler import MenuHandler
                if Player().is_alive and MenuHandler().sound_enabled:
                    pygame.mixer.Sound.play(self.jam_sound)
            self.current_attack_time = (pygame.time.get_ticks()-self.attack_start)
        # player outside jammer range
        else:
            Player().can_input = True
            self.attacking = False
            self.current_attack_time = 0
            Jam().alpha = 0
        if Player().is_alive == False:
            Jam().alpha = 0
            pygame.mixer.Sound.stop(self.jam_sound)

        # if player has been jammed for attack_cooldown milliseconds
        # disable player input
        if self.current_attack_time >= self.attack_cooldown:
            Player().can_input = False

        # updates jamming bool used for debug
        GameWorld().jamming = self.attacking
        
    def draw(self, screen):
        from classes.GameWorld import GameWorld
        screen.blit(self.image, pygame.Rect(self.rect.x - GameWorld().camera_x, self.rect.y, self.rect.width, self.rect.height))

        
        #jammer debug circle
        surface = pygame.Surface((GameWorld().screen_width, GameWorld().screen_height), pygame.SRCALPHA)
        pygame.draw.circle(surface, (255, 0, 0, 50), (self.rect.center[0] - GameWorld().camera_x, self.rect.center[1]), 500)
        screen.blit(surface, (0, 0))

    def on_collision(self, other):
        from classes.GameWorld import GameWorld
        if other.tag == "Explosion":
            GameWorld().objectives_completed += 1
            GameWorld().score += 1000
            pygame.mixer.Sound.stop(self.jam_sound)
            Jam().alpha = 0
            self.is_alive = False
            self.kill()
            Player().can_input = True
            self.attacking = False
            GameWorld().jamming = self.attacking

            # if the jammer dies after the player, we add the time score bonus
            if Player().is_alive == False:
                GameWorld().get_final_score()
