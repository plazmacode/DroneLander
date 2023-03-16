import pygame
from classes.GameObject import GameObject
from classes.Grenade import Grenade

def singleton(class_):
    """
    Player singleton
    """
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance

# cannot use metaclass singleton on Player, because it inherits from GameObject, therefore we do this
# we use a decorator instead
@singleton
class Player(GameObject):
    """
    Player Class
    """
    def __init__(self):
        """
        Player init
        """
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        # this is a mess
        self.image = pygame.image.load("./images/Drone(1).png").convert_alpha()
        self.base_image = pygame.image.load("./images/Drone(1).png").convert_alpha()
        self.base_image = pygame.transform.scale(self.image, (125, 50))
        rects = ((0, 0, 20, 8), (20, 0, 20, 8), (40, 0, 20, 8), (60, 0, 20, 8))
        self.base_images = self.load_images("./images/drone-spritesheet.png", rects, (self.image.get_width() * 10, self.image.get_height() * 10))
        self.mask = pygame.mask.from_surface(self.base_images[0])
        self.current_image = 0
        self.rect = self.image.get_rect()
        self.tag = "Player"
        self.rotation_speed = 4

        # we have 5 sounds. they are all annoying :)
        # sound 4 and 5 loops the best because they are synthesized
        # number 5 is best because mixer.Sound.play("sound", -1) doesn't loop instantly
        self.servo_sound = pygame.mixer.Sound("./sounds/drone5.wav")
        self.servo_sound.set_volume(0.4)
        self.servo_duration = self.servo_sound.get_length() * 1000
        self.playing_sound = False
        self.servo_channel = pygame.mixer.Channel(2)
        self.servo_start_time = 0

        self.release_sound = pygame.mixer.Sound("./sounds/release.wav")
        
    #initialize values that are shared between first instantiation and when respawning
    def initialize_values(self):
        """
        Set initial values for Player
        """
        self.rect.center = (960, 450)
        self.angle = 0
        self.direction = pygame.math.Vector2(0,0)
        self.velocity = pygame.math.Vector2(0,0)
        self.keys = pygame.key.get_pressed()
        self.oldKeys = pygame.key.get_pressed()
        self.can_attack = True
        self.can_input = True
        self.load_difficulty()
        from classes.GameWorld import GameWorld
        GameWorld().grenades = self.grenades
        self.too_high = False
        self.death_timer = 3
        self.reset_timer = 3
        self.is_alive = True

    def update(self):
        """
        Player update
        """
        self.move()
        self.animate()
        self.checkHeight()
        self.move_camera()
        self.play_sound()
    
    def play_sound(self):
        # loop code 1
        # if self.servo_channel.get_busy() == False:
        #     self.servo_channel.play(self.servo_sound)

        # loop code 2
        # if self.servo_channel.get_busy() == False:
        #     self.servo_channel.play(self.servo_sound, -1)

        # loop code 3
        # use the files duration to manually check if it looped
        # we can manually adjust duration to perfect the loop
        # we cannot make this loop perfectly, instead we play the sound overlapping
        # it's a feature now
        from classes.MenuHandler import MenuHandler
        if self.playing_sound == False:
            self.playing_sound = True
            if Player().is_alive and MenuHandler().sound_enabled:
                pygame.mixer.Sound.play(self.servo_sound)
            self.servo_start_time = pygame.time.get_ticks()
        else:
            if pygame.time.get_ticks() >= self.servo_start_time + self.servo_duration - 225:
                self.playing_sound = False

    def load_difficulty(self):
        """
        Adjusts values that are difficulty dependent
        """
        from classes.GameWorld import GameWorld
        if GameWorld().difficulty == 0:
            self.grenades = 10
        if GameWorld().difficulty == 1:
            self.grenades = 5

    def draw(self, screen):
        """
        Player draw
        """
        screen.blit(self.image, self.rect)

    def on_collision(self, other):
        """
        Player collision
        """
        if other.tag == "Obstacle" or other.tag == "Explosion":
            self.on_death()

    def on_death(self):
        """
        Functionality relating to Player death
        """
        from classes.MenuHandler import MenuHandler
        from classes.GameWorld import GameWorld
        from classes.Explosion import Explosion
        MenuHandler().end_menu()
        self.is_alive = False
        self.kill()
        # stop servo sound from playing/looping
        self.servo_sound.stop()
        GameWorld().instantiate(Explosion(self.rect.center, 300))
        # get final score to add time bonus
        GameWorld().get_final_score()

    def move(self):
        """
        Player movement
        """
        self.input_handler()

        # gravity
        self.rect.y += 2

        # lock angle to 360 degrees, prevents angles like 1591 degrees
        self.angle %= 360

        # use the base_images to rotate
        # if we rotate the normal image we get a memory leak which freezes our game within a minute
        self.image = pygame.transform.rotate(self.base_images[self.current_image], self.angle)
        self.rect = self.image.get_rect(center =(self.rect.center))

        # update mask for pixel collision
        self.mask = pygame.mask.from_surface(self.image) 


        self.rect.move_ip(0, self.direction.y * self.velocity.y)
        self.velocity.y -= 0.1
        if self.velocity.y < 0:
            self.velocity.y = 0

        self.velocity.x -= 0.1
        if self.velocity.x < 0:
            self.velocity.x = 0

    def move_camera(self):
        """
        Camera movement
        """
        from classes.GameWorld import GameWorld
        #call move_camera() with our x velocity to change the camera position
        GameWorld().move_camera(self.direction.x * self.velocity.x)
        # left screen bounds
        if GameWorld().camera_x <= -200:
            GameWorld().camera_x = -200

    def animate(self):
        """
        Player animation
        """
        self.current_image += 1
        if self.current_image > len(self.base_images) -1:
            self.current_image = 0

    # get user input to change angle and attack
    def input_handler(self):
        """
        Player input
        """
        if self.can_input:
            self.keys = pygame.key.get_pressed()

            if self.keys[pygame.K_a]:
                self.angle += self.rotation_speed
            if self.keys[pygame.K_d]:
                self.angle -= self.rotation_speed
            if self.keys[pygame.K_w]:
                self.thrust()

            if self.can_attack:
                if self.keys[pygame.K_SPACE]:
                    self.attack()
            
            if self.oldKeys[pygame.K_SPACE] and not self.keys[pygame.K_SPACE]:
                self.can_attack = True

            self.oldKeys = self.keys

    def thrust(self):
        """
        Moves Player upwards locally
        """
        self.direction = pygame.math.Vector2(0, -1)
        self.direction.rotate_ip(-self.angle)

        self.velocity = pygame.math.Vector2(8,8)

    def attack(self):
        """
        Throws granade from Player
        """
        if self.grenades > 0:
            from classes.GameWorld import GameWorld
            g = Grenade((self.rect.center[0] + GameWorld().camera_x, self.rect.center[1]), self.direction, self.velocity)
            self.grenades -= 1
            GameWorld().grenades = self.grenades
            GameWorld().instantiate(g)
            self.can_attack = False
            pygame.mixer.Sound.play(self.release_sound)
            

    def checkHeight(self):
        """
        Check to see if Player is too high up
        """
        # Start a new countdown if the Player gets too high up
        from classes.GameWorld import GameWorld
        if self.rect.y < 200 and self.too_high == False:
            self.too_high = True
            self.death_timer = self.reset_timer
        elif self.rect.y >= 200:
            self.too_high = False
            GameWorld().too_high = False

        # Runs the countdown as long as the Player is too high up
        if self.too_high == True:
            GameWorld().too_high = True
            self.count_death()     

    def count_death(self):
        """
        Counts down and kills Player when too high up for too long
        """
        # Kills the Player when the timer hits 0
        if self.death_timer <= 0:
            from classes.GameWorld import GameWorld
            from classes.Explosion import Explosion
            GameWorld().too_high = False
            GameWorld().instantiate(Explosion(self.rect.center, 300))
            self.on_death()

        # Counts down as long as timer is above 0
        else:
            from classes.GameWorld import GameWorld
            self.death_timer -= GameWorld().delta_time
            GameWorld().death_timer = self.death_timer