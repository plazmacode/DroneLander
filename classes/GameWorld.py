import pygame
import math
from classes.Jam import Jam
from classes.Marker import Marker
from classes.Parallax import Parallax
from classes.LevelLoader import LevelLoader
from classes.HighscoreManager import HighscoreManager
from classes.ButtonActions import ButtonActions

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

        pygame.display.set_caption("Auxiliary Light On")
        self._clock = pygame.time.Clock()
        self._font = pygame.font.Font("./fonts/PixeloidSans-Bold.ttf", 28)
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
        self.mixer = pygame.mixer
        self.jamming = False
        self.game_state = "MENU"
        self.score = 0
        self.level_select = 0

        #menu
        self.text_fields = []
        self.buttons = []
        self.selected_button = 0

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
        running = True
        MenuHandler().start_menu()
        while running:
            # Handle events
            event_list = pygame.event.get()
            for event in event_list:
                if event.type == pygame.QUIT:
                    # pygame.quit()
                    running = False
            self.update(event_list)
            self.draw()

            # Limit the frame rate
            self.delta_time = self._clock.tick(40) / 1000
        pygame.quit()
        return
    # @profile
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
        Marker().update()
        Parallax().update()

        for event in event_list:
            if event.type == pygame.KEYDOWN and len(self.buttons) > 0:
                """
                menu selection does not loop
                when it was looping the player would accidentally be pressing w and loop around and hit the quit menu
                because w is also the thrust button
                """
                if event.key == pygame.K_s:
                    self.selected_button = min(self.selected_button + 1, len(self.buttons) - 1)
                    print(self.selected_button)
                elif event.key == pygame.K_w:
                    self.selected_button = max(self.selected_button - 1, 0)
                elif event.key == pygame.K_RETURN:
                    ButtonActions().run(self.buttons[self.selected_button].action, self.buttons[self.selected_button])


                

        for i, button in enumerate(self.buttons):
            button.update(event_list)
            if i == self.selected_button:
                button.new_color = button.hover_color
                button.redraw()

        for text_field in self.text_fields:
            text_field.update(event_list)



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
            Marker().draw(self._screen)
            #draw UI
            self._screen.blit(grenade_text, (45, 100))
            # self._screen.blit(score_text, ((self.screen_width - score_text.get_width()) // 2, 150))
            self._screen.blit(timer_text, (45, 43))
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

        for text_field in self.text_fields:
            text_field.draw(self._screen)

        self._screen.blit(self._screen, (0,0))

        # self._screen.blit(self.update_fps(), (10,0))

        pygame.display.flip()
    
    def instantiate(self, object):
        """
        Adds new GameObject to existing list of GameObjects
        """
        self.new_game_objects.add(object)