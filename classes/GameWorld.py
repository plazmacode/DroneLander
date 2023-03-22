import pygame
import math
from classes.Jam import Jam
from classes.Parallax import Parallax
from classes.LevelLoader import LevelLoader
from profilehooks import profile

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
        self.background_image = pygame.image.load("./images/Sky.png")
        self.background_image = pygame.transform.scale(self.background_image, (1920, 1080)).convert()
        self.field_image = pygame.image.load("./images/Field.png")
        self.field_image = pygame.transform.scale(self.field_image, (1920, 600)).convert_alpha()
        self.background_rect = self.background_image.get_rect()
        self.grenades = 0
        self.difficulty = 0
        self.game_objects = pygame.sprite.Group()
        self.new_game_objects = pygame.sprite.Group()
        self.tutorial_text = pygame.sprite.Group()
        self.buttons = []
        self.mixer = pygame.mixer
        self.jamming = False
        self.game_state = "MENU"
        self.score = 0

        self.too_high = False
        self.death_timer = 3
        self.outside_level = False
        self.ol_death_timer = 3
        
        self.objectives_compeleted = 0
        self.main_objective_completed = False

        self.level_time = 0
        self.level_start_time = 0

    # obsolete?
    def start_game(self):
        """
        Creates the selected level and starts the game
        """
        LevelLoader().load_level(0)

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
    
    @profile
    def update(self, event_list):
        """
        Main update
        """

        for go in self.new_game_objects:
            self.game_objects.add(go)

        self.new_game_objects.empty()

        self.game_objects.update()
        self.collision_check()

        self.tutorial_text.update()

        Jam().update()
        Parallax().update()

        for button in self.buttons:
            button.update(event_list)

    def move_camera(self, x):
        """
        Moves everything except Player in x-axis according to Player movement
        """
        for go in self.game_objects:
            if go.tag != "Player":
                go.rect.move_ip(-x, 0)
            if go.tag == "Jammer":
                go.surface_rect.move_ip(-x, 0)

        for text in self.tutorial_text:
            text.rect.move_ip(-x, 0)

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
                    if go1.collision and go2.collision:
                        if go1.mask.overlap(go2.mask, (go2.rect.x - go1.rect.x, go2.rect.y - go1.rect.y)):
                            go1.on_collision(go2)

    def get_final_score(self):
        """
        Adds score based on time spent to complete level
        """
        self.score += math.ceil(2000 - self.level_time / 1000 * 20)
        
        update_score_event = pygame.event.Event(pygame.USEREVENT + 1)
        pygame.event.post(update_score_event)
    
    @profile
    def draw(self):
        """
        Main draw
        """
        # draw background with parallax (also clears screen)
        Parallax().draw(self._screen)

        grenade_text = self._font.render("Grenades: " + str(self.grenades), True, (0, 0, 0))
        too_high_text = self._font.render("GET DOWN! " + str(int(self.death_timer + 1)), True, (0, 0, 0))
        outside_level_text = self._font.render("RETURN TO THE BATTLEFIELD! " + str(int(self.ol_death_timer + 1)), True, (0, 0, 0))
        # endscreen_text = self._font.render(self.endscreen_string, True, (0, 0, 0))
        # score_text = self._font.render("Score: " + str(self.score), True, (0, 0, 0))

        # DEBUG
        # attack_text = self._font.render("WE JAMMING: " + str(self.jamming), True, (0, 0, 0)) 
        # objective_text = self._font.render("MAIN OBJECTIVE COMPLETED: " + str(self.main_objective_completed), True, (0, 0, 0)) 
        # player_angle_text = self._font.render("ANGLE: " + str(Player().angle), True, (0, 0, 0)) 
        # player_directionx_text = self._font.render("Direction.x: " + str(Player().direction.x), True, (0, 0, 0)) 
        # player_directiony_text = self._font.render("Direction.y: " + str(Player().direction.y), True, (0, 0, 0))
        # player_velocityx_text = self._font.render("Velocity.x: " + str(Player().velocity.x), True, (0, 0, 0)) 
        # player_velocityy_text = self._font.render("Velocity.y: " + str(Player().velocity.y), True, (0, 0, 0))

        # only update level time when playing
        if self.game_state == "PLAY":
            self.level_time = pygame.time.get_ticks() - self.level_start_time
        
        timer_text = self._font.render("Time: " + str(self.level_time / 1000), True, (0, 0, 0))

        for game_object in self.game_objects:
            game_object.draw(self._screen)

        # if self.game_state == "SCORESCREEN":
        #     self._screen.blit(endscreen_text, ((self.screen_width - endscreen_text.get_width()) // 2, 500))
        
        if self.game_state == "MENU":
            self._screen.blit(self.field_image, (0, 500))

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
            # self._screen.blit(player_directionx_text, (100, 200))
            # self._screen.blit(player_directiony_text, (100, 300))
            # self._screen.blit(player_velocityx_text, (100, 400))
            # self._screen.blit(player_velocityy_text, (100, 500))

        for text in self.tutorial_text:
            text.draw(self._screen)

        if self.too_high == True:
            self._screen.blit(too_high_text, (self.screen_width / 2 - too_high_text.get_width() / 2, self.screen_height / 2 - too_high_text.get_height() / 2))
        if self.outside_level == True:
            self._screen.blit(outside_level_text, (self.screen_width / 2 - outside_level_text.get_width() / 2, self.screen_height / 2 - outside_level_text.get_height() / 2 - 100))

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