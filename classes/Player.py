import pygame
from classes.GameObject import GameObject
from classes.Grenade import Grenade

def singleton(class_):
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
    def __init__(self):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        # this is a mess
        self.image = pygame.image.load("./images/Drone(1).png").convert_alpha()
        self.base_image = pygame.image.load("./images/Drone(1).png").convert_alpha()
        self.base_image = pygame.transform.scale(self.image, (125, 50))
        rects = ((0, 0, 20, 8), (20, 0, 20, 8), (40, 0, 20, 8), (60, 0, 20, 8))
        self.base_images = self.load_images("./images/drone-spritesheet.png", rects, (self.image.get_width() * 10, self.image.get_height() * 10))
        self.current_image = 0
        self.rect = self.image.get_rect()
        

    def initialize_values(self):
        self.rect.center = (300, 450)
        self.tag = "Player"
        self.angle = 0
        self.rotation_speed = 4
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
        self.move()
        self.animate()
        self.checkHeight()
        self.move_camera()
    
    def load_difficulty(self):
        from classes.GameWorld import GameWorld
        if GameWorld().difficulty == 0:
            self.grenades = 10
        if GameWorld().difficulty == 1:
            self.grenades = 5

    def draw(self, screen):
        from classes.GameWorld import GameWorld
        screen.blit(self.image, self.rect)

    def on_collision(self, other):
        if other.tag == "Obstacle" or other.tag == "Explosion":
            self.on_death()

    def on_death(self):
        from classes.MenuHandler import MenuHandler
        from classes.GameWorld import GameWorld
        from classes.Explosion import Explosion
        MenuHandler().end_menu()
        self.is_alive = False
        self.kill()
        GameWorld().instantiate(Explosion(self.rect.center, 300))
        GameWorld().get_final_score()

    def move(self):
        self.input_handler()

        # gravity
        self.rect.y += 2

        # lock angle to 360 degrees, prevents angles like 1591 degrees
        self.angle %= 360

        # use the base_images to rotate
        # if we rotate the normal image we get a memory leak which freezes our game within a minute
        self.image = pygame.transform.rotate(self.base_images[self.current_image], self.angle)
        self.rect = self.image.get_rect(center =(self.rect.center))

        self.rect.move_ip(0, self.direction.y * self.velocity.y)
        self.velocity.y -= 0.1
        if self.velocity.y < 0:
            self.velocity.y = 0

        self.velocity.x -= 0.1
        if self.velocity.x < 0:
            self.velocity.x = 0

    def move_camera(self):
        from classes.GameWorld import GameWorld
        # GameWorld().camera_x += self.direciton.x * self.velocity.x
        GameWorld().move_camera(self.direction.x * self.velocity.x)
        # left screen bounds
        if GameWorld().camera_x <= -200:
            GameWorld().camera_x = -200

    def animate(self):
        self.current_image += 1
        if self.current_image > len(self.base_images) -1:
            self.current_image = 0

    # get user input to change angle and attack
    def input_handler(self):
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
        # set player direction upwards locally
        self.direction = pygame.math.Vector2(0, -1)
        self.direction.rotate_ip(-self.angle)

        self.velocity = pygame.math.Vector2(8,8)

    def attack(self):
        if self.grenades > 0:
            from classes.GameWorld import GameWorld
            g = Grenade((self.rect.center[0] + GameWorld().camera_x, self.rect.center[1]), self.direction, self.velocity)
            self.grenades -= 1
            GameWorld().grenades = self.grenades
            GameWorld().instantiate(g)
            self.can_attack = False

    def checkHeight(self):
        from classes.GameWorld import GameWorld
        if self.rect.y < 200 and self.too_high == False:
            self.too_high = True
            self.death_timer = self.reset_timer
        elif self.rect.y >= 200:
            self.too_high = False
            GameWorld().too_high = False

        if self.too_high == True:
            GameWorld().too_high = True
            self.count_death()

    def respawn(self):
        from classes.GameWorld import GameWorld
        GameWorld().camera_x = 0
        self.initialize_values()
        

    def count_death(self):
        if self.death_timer <= 0:
            from classes.GameWorld import GameWorld
            from classes.Explosion import Explosion
            GameWorld().too_high = False
            GameWorld().instantiate(Explosion(self.rect.center, 300))
            self.on_death()

        else:
            from classes.GameWorld import GameWorld
            self.death_timer -= GameWorld().delta_time
            GameWorld().death_timer = self.death_timer