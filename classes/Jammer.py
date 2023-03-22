import pygame
from classes.GameObject import GameObject
from classes.Player import Player
from classes.Jam import Jam

class Jammer(GameObject):
    def __init__(self, centerInput, range) -> None:
        """
        The jammer is the higher difficulty enemy in this game, besides trees.
        Therefore it is a boss!
        If you REALLY would like a boss, then imagine it as a person you're KILLING you MONSTER! :)
        """
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("./images/Jammer.png") 
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * 10, self.image.get_height() * 10)).convert_alpha() 
        self.rect = self.image.get_rect(center=centerInput)
        self.tag = "Jammer"
        self.attack_range = range
        self.attack_cooldown = 1500 # time before the player input is jammed
        self.current_attack_time = 0
        self.attacking = False
        self.jam_sound = pygame.mixer.Sound("./sounds/noise2.wav")
        self.is_alive = True
        self.mask = pygame.mask.from_surface(self.image)

        # Create a surface to hold the jammer image and jammer radius
        self.surface = pygame.Surface((range * 2, range * 2), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(centerInput[0] - 250, centerInput[1] -250))
        
        # Draw the jammer  circle onto the surface
        pygame.draw.circle(self.surface, (255, 0, 0, 50), (range, range), range)
        
        # Draw the jammer image onto the surface
        self.surface.blit(self.image, (range - self.image.get_width() / 2, range - self.image.get_height() / 2))

        # set the surface_rect to move the surface
        # set the rect again to fix collision with jammer tower.
        self.surface_rect = self.surface.get_rect(center = centerInput)
        self.rect = self.image.get_rect(center=centerInput)

    def update(self):
        self.attack()
    
    def attack(self):
        from classes.GameWorld import GameWorld

        # get distance between jammer and player
        distance = pygame.math.Vector2(self.surface_rect.center).distance_to(Player().rect.center)

        # player inside jammer range
        if distance <= self.attack_range and self.is_alive == True:
            if self.attacking == False:
                self.attack_start = pygame.time.get_ticks()
                self.attacking = True
                Jam().active_jammers.append(self)
                from classes.MenuHandler import MenuHandler
                if Player().is_alive and MenuHandler().sound_enabled:
                    pygame.mixer.Sound.play(self.jam_sound)
            self.current_attack_time = (pygame.time.get_ticks()-self.attack_start)
        # player outside jammer range
        else:
            Player().can_input = True
            self.attacking = False
            self.current_attack_time = 0
            Jam().remove(self)
            pygame.mixer.Sound.stop(self.jam_sound)
        if Player().is_alive == False:
            Jam().remove(self)
            pygame.mixer.Sound.stop(self.jam_sound)

        # if player has been jammed for attack_cooldown milliseconds
        # disable player input
        if self.current_attack_time >= self.attack_cooldown:
            Player().can_input = False

        # updates jamming bool used for debug
        GameWorld().jamming = self.attacking
        
    def draw(self, screen):
        screen.blit(self.surface, self.surface_rect)

    def on_collision(self, other):
        from classes.GameWorld import GameWorld
        if other.tag == "Explosion":
            # add score and objectives completed
            GameWorld().objectives_completed += 1
            GameWorld().score += 1000
            update_score_event = pygame.event.Event(pygame.USEREVENT + 1)
            pygame.event.post(update_score_event)

            # reset jammer values to stop jamming effect
            pygame.mixer.Sound.stop(self.jam_sound)
            Jam().remove(self)
            self.is_alive = False
            self.kill()
            Player().can_input = True
            self.attacking = False
            GameWorld().jamming = self.attacking

            # Checks if this was the main objective
            super().on_collision(other)
