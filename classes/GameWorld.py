import pygame
import math
from classes.Environment import Environment
from classes.Jammer import Jammer
from classes.Player import Player
from classes.Button import Button
from classes.TextField import TextField
from classes.Jam import Jam
from classes.Parallax import Parallax

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

        pygame.display.set_caption("Drone Lander")
        self._clock = pygame.time.Clock()
        self._font = pygame.font.SysFont(None, 48)
        self.endscreen_string = "you suck"
        self.background_image = pygame.image.load("./images/Sky.png").convert_alpha()
        self.background_image = pygame.transform.scale(self.background_image, (1920, 1080))
        self.background_rect = self.background_image.get_rect()
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
        self.main_objective_completed = False

        self.level_time = 0
        self.level_start_time = 0

    def start_game(self):
        """
        Creates the selected level and starts the game
        """
        self.game_state = "PLAY"
        self.buttons.clear()

        self.objectives_completed = 0
        self.main_objective_completed = False

        self.score = 0
        self.level_time = 0
        self.level_start_time = pygame.time.get_ticks()
        self.game_objects = pygame.sprite.Group()

        GameWorld().buttons.append(TextField((34, 42, 104), (self.screen_width / 2, 200), "Score: " + str(GameWorld().score), 48, "score"))

        
        # Resets parallax
        Parallax().reset_position()

        # Easy Level
        if self.difficulty == 0:
            # Place floor, value sets number of tiles placed
            for x in range(5):
                self.game_objects.add(Environment("Ground", (x * 2000, 1055), "Obstacle"))
            # Left bounds "wall"
            self.game_objects.add(Environment("TreeTrunk", (000, 800), "Background"))
            self.game_objects.add(Environment("TreeCrown", (000, 405), "Obstacle"))
            self.game_objects.add(Environment("TreeCrown", (-200, 935), "Obstacle"))

            # Launch brick
            self.game_objects.add(Environment("Brick", (960, 1015), "Brick"))

            # Tree
            self.game_objects.add(Environment("TreeTrunk", (1500, 800), "Background"))
            self.game_objects.add(Environment("TreeCrown", (1500, 405), "Obstacle"))

            # First ammo dump
            self.game_objects.add(Environment("AmmoDump(Shells)", (2200, 955), "Obstacle"))

            # Bush
            self.game_objects.add(Environment("TreeCrown", (2600, 935), "Obstacle"))
            self.game_objects.add(Environment("TreeCrown", (2900, 955), "Obstacle"))

            # Last ammo dump (main objective) + right bounds "wall" 
            self.main_objective_object = Environment("AmmoDump(Shells)", (3800, 955), "Obstacle")
            self.main_objective_object.main_objective = True
            self.game_objects.add(self.main_objective_object)
            self.game_objects.add(Environment("TreeTrunk", (4000, 805), "Background"))
            self.game_objects.add(Environment("TreeCrown", (4000, 400), "Obstacle"))
            self.game_objects.add(Environment("TreeCrown", (4250, 955), "Obstacle"))


        # Hard Level
        if self.difficulty == 1:
            # Place floor, value sets number of tiles placed
            for x in range(5):
                self.game_objects.add(Environment("Ground", (x * 2000, 1055), "Obstacle"))
            # Left bounds "wall"
            self.game_objects.add(Environment("TreeTrunk", (000, 800), "Background"))
            self.game_objects.add(Environment("TreeCrown", (000, 405), "Obstacle"))
            self.game_objects.add(Environment("TreeCrown", (-200, 935), "Obstacle"))

            # Launch brick
            self.game_objects.add(Environment("Brick", (960, 1015), "Brick"))

            # Bush
            self.game_objects.add(Environment("TreeCrown", (500, 935), "Obstacle"))

            # Tree patch
            self.game_objects.add(Environment("TreeTrunk", (1910, 780), "Background"))
            self.game_objects.add(Environment("TreeTrunk", (2330, 780), "Background"))
            self.game_objects.add(Environment("TreeTrunk", (1700, 800), "Background"))
            self.game_objects.add(Environment("TreeCrown", (1700, 395), "Obstacle"))
            self.game_objects.add(Environment("TreeTrunk", (2560, 800), "Background"))
            self.game_objects.add(Environment("TreeCrown", (2560, 405), "Obstacle"))
            self.game_objects.add(Environment("TreeTrunk", (2120, 790), "Background"))
            self.game_objects.add(Environment("TreeCrown", (2120, 405), "Obstacle"))

            # Ammo dump under tree
            self.game_objects.add(Environment("TreeTrunk", (3500, 790), "Background"))
            self.game_objects.add(Environment("TreeCrown", (3500, 405), "Obstacle"))
            self.game_objects.add(Environment("AmmoDump(Shells)", (3500, 955), "Obstacle"))

            # Ammo dump between bushes
            self.game_objects.add(Environment("AmmoDump(Shells)", (4750, 955), "Obstacle"))
            self.game_objects.add(Environment("TreeCrown", (4400, 935), "Obstacle"))
            self.game_objects.add(Environment("TreeCrown", (5100, 935), "Obstacle"))

            # Tree
            self.game_objects.add(Environment("TreeTrunk", (5860, 790), "Background"))
            self.game_objects.add(Environment("TreeCrown", (5860, 405), "Obstacle"))

            # Jammer + right bounds "wall"
            self.game_objects.add(Environment("TreeTrunk", (6860, 790), "Background"))
            self.game_objects.add(Environment("TreeCrown", (6860, 405), "Obstacle"))
            self.game_objects.add(Environment("AmmoDump(Shells)", (6710, 955), "Obstacle"))
            self.game_objects.add(Environment("TreeCrown", (7000, 935), "Obstacle"))
            self.main_objective_object = Jammer((6500, 905))
            self.main_objective_object.main_objective = True
            self.game_objects.add(self.main_objective_object)

        
        self.game_objects.add(Player())
        Player().initialize_values()
        # self.gameObjects.add(Environment("DetonationDecal", 0, 850))

    def update_fps(self):
        fps = str(int(self._clock.get_fps()))
        fps_text = self._font.render(fps, 1, pygame.Color("coral"))
        return fps_text

    def run(self):
        """
        Main program loop
        """
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
        """
        Main update
        """

        for go in self.new_game_objects:
            self.game_objects.add(go)

        self.new_game_objects.empty()

        self.game_objects.update()
        self.collision_check()
        
        Jam().update()
        Parallax().update()

        for button in self.buttons:
            button.update(event_list)

    def move_camera(self, x):
        """
        Moves everything except Player in x-axis according to Player movement
        """
        #it works first try wow
        for go in self.game_objects:
            if go.tag != "Player":
                go.rect.move_ip(-x, 0)

    def collision_check(self):
        """
        Checks collision between GameObjects
        """
        for go1 in self.game_objects:
            for go2 in self.game_objects:
                if not go1 is go2:
                    # if go1.rect.colliderect(go2.rect):
                    #     go1.on_collision(go2)
                    # THE GAME WILL CRASH if a gameobject lacks a mask
                    if go1.mask.overlap(go2.mask, (go2.rect.x - go1.rect.x, go2.rect.y - go1.rect.y)):
                        go1.on_collision(go2)

    def get_final_score(self):
        """
        Adds score based on time spent to complete level
        """
        self.score += math.ceil(2000 - self.level_time / 1000 * 20)
        
        update_score_event = pygame.event.Event(pygame.USEREVENT + 1)
        pygame.event.post(update_score_event)

    def draw(self):
        """
        Main draw
        """
        # Clear the screen
        self._screen.fill((63, 153, 249))
        self._screen.blit(self.background_image, self.background_rect)

        # draw background with parallax
        Parallax().draw(self._screen)

        grenade_text = self._font.render("Grenades: " + str(self.grenades), True, (0, 0, 0))
        too_high_text = self._font.render("GET DOWN! " + str(int(self.death_timer + 1)), True, (0, 0, 0))
        # endscreen_text = self._font.render(self.endscreen_string, True, (0, 0, 0))
        # score_text = self._font.render("Score: " + str(self.score), True, (0, 0, 0))

        # DEBUG
        # attack_text = self._font.render("WE JAMMING: " + str(self.jamming), True, (0, 0, 0)) 
        # objective_text = self._font.render("MAIN OBJECTIVE COMPLETED: " + str(self.main_objective_completed), True, (0, 0, 0)) 
        # player_angle_text = self._font.render("ANGLE: " + str(Player().angle), True, (0, 0, 0)) 

        # only update level time when playing
        if self.game_state == "PLAY":
            self.level_time = pygame.time.get_ticks() - self.level_start_time
        
        timer_text = self._font.render("Time: " + str(self.level_time / 1000), True, (0, 0, 0))

        for game_object in self.game_objects:
            game_object.draw(self._screen)

        # if self.game_state == "SCORESCREEN":
            # self._screen.blit(endscreen_text, ((self.screen_width - endscreen_text.get_width()) // 2, 500))

        if self.game_state == "PLAY" or self.game_state == "SCORESCREEN":
            # draw noise
            Jam().draw(self._screen)

            #draw UI
            self._screen.blit(grenade_text, (100, 100))
            # self._screen.blit(score_text, ((self.screen_width - score_text.get_width()) // 2, 150))
            self._screen.blit(timer_text, (self.screen_width - 200, 50))
            # DEBUG
            # self._screen.blit(attack_text, (100, 200))
            # self._screen.blit(objective_text, (100, 300))
            # self._screen.blit(player_angle_text, (100, 400))

        if self.too_high == True:
            self._screen.blit(too_high_text, (self.screen_width / 2 - too_high_text.get_width() / 2, self.screen_height / 2 - too_high_text.get_height() / 2))

        for button in self.buttons:
            button.draw(self._screen)

        self._screen.blit(self._screen, (0,0))

        self._screen.blit(self.update_fps(), (10,0))

        pygame.display.flip()
    
    def instantiate(self, object):
        """
        Adds new GameObject to existing list of GameObjects
        """
        self.new_game_objects.add(object)