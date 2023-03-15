import pygame
import math
from classes.GameObject import GameObject
from classes.Environment import Environment
from classes.Jammer import Jammer
from classes.Player import Player
from classes.Button import Button
from classes.Jam import Jam

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class GameWorld(metaclass=Singleton):
    def __init__(self):
        pygame.init()
        self._screen = pygame.display.set_mode((1920, 1080))
        self.screen_width = self._screen.get_width()
        self.screen_height = self._screen.get_height()
        self.camera_x = 0
        pygame.display.set_caption("Drone Lander")
        self._clock = pygame.time.Clock()
        self._font = pygame.font.SysFont(None, 48)
        self.grenades = 0
        self.difficulty = 0
        self.game_objects = pygame.sprite.Group()
        self.new_game_objects = pygame.sprite.Group()
        self.buttons = []
        self.mixer = pygame.mixer
        self.jamming = False
        self.game_state = "MENU"
        self.score = 0
        self.too_high = False
        self.death_timer = 3
        self.objectives_compeleted = 0
        self.level_time = 0
        self.level_start_time = 0

    def start_game(self):
        self.game_state = "PLAY"
        self.buttons.clear()
        self.objectives_completed = 0
        self.score = 0
        self.level_time = 0
        self.level_start_time = pygame.time.get_ticks()
        self.game_objects = pygame.sprite.Group()

        # Easy Level
        if self.difficulty == 0:
            # Place floor, value sets number of tiles placed
            for x in range(5):
                self.game_objects.add(Environment("./images/Ground", (x * 2000, 1055), "Obstacle"))
            # Left bounds "wall"
            self.game_objects.add(Environment("./images/TreeTrunk", (000, 800), "Background"))
            self.game_objects.add(Environment("./images/TreeCrown", (000, 405), "Obstacle"))
            self.game_objects.add(Environment("./images/TreeCrown", (-200, 935), "Obstacle"))

            # Tree
            self.game_objects.add(Environment("./images/TreeTrunk", (1500, 800), "Background"))
            self.game_objects.add(Environment("./images/TreeCrown", (1500, 405), "Obstacle"))

            # First ammo dump
            self.game_objects.add(Environment("./images/AmmoDump(Shells)", (2200, 955), "Obstacle"))

            # Bush
            self.game_objects.add(Environment("./images/TreeCrown", (2600, 935), "Obstacle"))
            self.game_objects.add(Environment("./images/TreeCrown", (2900, 955), "Obstacle"))

            # Last ammo dump + right bounds "wall"
            self.game_objects.add(Environment("./images/AmmoDump(Shells)", (3800, 955), "Obstacle"))
            self.game_objects.add(Environment("./images/TreeTrunk", (4000, 805), "Background"))
            self.game_objects.add(Environment("./images/TreeCrown", (4000, 400), "Obstacle"))
            self.game_objects.add(Environment("./images/TreeCrown", (4250, 955), "Obstacle"))



        # Hard Level
        if self.difficulty == 1:
            # Place floor, value sets number of tiles placed
            for x in range(5):
                self.game_objects.add(Environment("./images/Ground", (x * 2000, 1055), "Obstacle"))
            # Left bounds "wall"
            self.game_objects.add(Environment("./images/TreeTrunk", (000, 800), "Background"))
            self.game_objects.add(Environment("./images/TreeCrown", (000, 405), "Obstacle"))
            self.game_objects.add(Environment("./images/TreeCrown", (-200, 935), "Obstacle"))

            # Bush
            self.game_objects.add(Environment("./images/TreeCrown", (800, 935), "Obstacle"))

            # Tree patch
            self.game_objects.add(Environment("./images/TreeTrunk", (1910, 780), "Background"))
            self.game_objects.add(Environment("./images/TreeTrunk", (2330, 780), "Background"))
            self.game_objects.add(Environment("./images/TreeTrunk", (1700, 800), "Background"))
            self.game_objects.add(Environment("./images/TreeCrown", (1700, 395), "Obstacle"))
            self.game_objects.add(Environment("./images/TreeTrunk", (2560, 800), "Background"))
            self.game_objects.add(Environment("./images/TreeCrown", (2560, 405), "Obstacle"))
            self.game_objects.add(Environment("./images/TreeTrunk", (2120, 790), "Background"))
            self.game_objects.add(Environment("./images/TreeCrown", (2120, 405), "Obstacle"))

            # Ammo dump under tree
            self.game_objects.add(Environment("./images/TreeTrunk", (3500, 790), "Background"))
            self.game_objects.add(Environment("./images/TreeCrown", (3500, 405), "Obstacle"))
            self.game_objects.add(Environment("./images/AmmoDump(Shells)", (3500, 955), "Obstacle"))

            # Ammo dump between bushes
            self.game_objects.add(Environment("./images/AmmoDump(Shells)", (4750, 955), "Obstacle"))
            self.game_objects.add(Environment("./images/TreeCrown", (4400, 935), "Obstacle"))
            self.game_objects.add(Environment("./images/TreeCrown", (5100, 935), "Obstacle"))

            # Tree
            self.game_objects.add(Environment("./images/TreeTrunk", (5860, 790), "Background"))
            self.game_objects.add(Environment("./images/TreeCrown", (5860, 405), "Obstacle"))

            # Jammer + right bounds "wall"
            self.game_objects.add(Environment("./images/TreeTrunk", (6860, 790), "Background"))
            self.game_objects.add(Environment("./images/TreeCrown", (6860, 405), "Obstacle"))
            self.game_objects.add(Environment("./images/AmmoDump(Shells)", (6710, 955), "Obstacle"))
            self.game_objects.add(Environment("./images/TreeCrown", (7000, 935), "Obstacle"))
            self.game_objects.add(Jammer((6500, 905)))

        
        self.game_objects.add(Player())
        Player().initialize_values()
        # self.gameObjects.add(Environment("DetonationDecal", 0, 850))

    def run(self):
        from classes.MenuHandler import MenuHandler
        MenuHandler().start_menu()
        while True:
            # Handle events
            event_list = pygame.event.get()
            for event in event_list:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        return

            self.update(event_list)
            self.draw()

            # Limit the frame rate
            self.delta_time = self._clock.tick(60) / 1000
    
    def update(self, event_list):

        for go in self.new_game_objects:
            self.game_objects.add(go)

        self.new_game_objects.empty()

        self.game_objects.update()
        self.collision_check()
        
        Jam().update()

        for button in self.buttons:
            button.update(event_list)

    def move_camera(self, x):
        #it works first try wow
        for go in self.game_objects:
            if go.tag != "Player":
                go.rect.move_ip(-x, 0)

    def collision_check(self):
        for go1 in self.game_objects:
            for go2 in self.game_objects:
                if not go1 is go2:
                    if go1.rect.colliderect(go2.rect):
                        go1.on_collision(go2)

    def get_final_score(self):
        if self.objectives_completed > 0:
            self.score += math.ceil(2000 - self.level_time / 1000 * 20)
            print("added timer score for completing objectives")

    def draw(self):
        # Clear the screen
        self._screen.fill((63, 153, 249))

        grenade_text = self._font.render("Grenades: " + str(self.grenades), True, (0, 0, 0))
        too_high_text = self._font.render("DIE " + str(int(self.death_timer + 1)), True, (0, 0, 0))
        attack_text = self._font.render("WE JAMMING: " + str(self.jamming), True, (0, 0, 0))
        score_text = self._font.render("Score: " + str(self.score), True, (0, 0, 0))

        # only update level time when playing
        if self.game_state == "PLAY":
            self.level_time = pygame.time.get_ticks() - self.level_start_time
        
        timer_text = self._font.render("Time: " + str(self.level_time / 1000), True, (0, 0, 0))

        for game_object in self.game_objects:
            game_object.draw(self._screen)

        if self.game_state == "PLAY" or self.game_state == "ENDMENU":
            # draw noise
            Jam().draw(self._screen)

            #draw UI
            self._screen.blit(grenade_text, (100, 100))
            self._screen.blit(attack_text, (100, 200))
            self._screen.blit(score_text, ((self.screen_width - score_text.get_width()) // 2, 50))
            self._screen.blit(timer_text, (self.screen_width - 200, 50))

        if self.too_high == True:
            self._screen.blit(too_high_text, (self.screen_width / 2 - too_high_text.get_width() / 2, self.screen_height / 2 - too_high_text.get_height() / 2))

        for button in self.buttons:
            button.draw(self._screen)

        self._screen.blit(self._screen, (0,0))

        pygame.display.flip()
    
    def instantiate(self, object):
        self.new_game_objects.add(object)