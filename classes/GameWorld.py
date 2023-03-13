import pygame
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

    def start_game(self):
        self.game_state = "PLAY"
        self.buttons.clear()
        self.game_objects.add(Player())
        self.game_objects.add(Environment("./images/Ground", (1000, 1055)))
        self.game_objects.add(Environment("./images/TreeTrunk", (1200, 800)))
        self.game_objects.add(Environment("./images/TreeCrown", (1200, 400)))
        self.game_objects.add(Environment("./images/AmmoDump(Shells)", (500, 955)))
        self.game_objects.add(Jammer((1500, 1000)))
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
            self._clock.tick(60)
    
    def update(self, event_list):

        for go in self.new_game_objects:
            self.game_objects.add(go)

        self.new_game_objects.empty()

        self.game_objects.update()
        self.collision_check()
        
        Jam().update()

        for button in self.buttons:
            button.update(event_list)

    def collision_check(self):
        for go1 in self.game_objects:
            for go2 in self.game_objects:
                if not go1 is go2:
                    if go1.rect.colliderect(go2.rect):
                        go1.on_collision(go2)

    def draw(self):
        # Clear the screen
        self._screen.fill((63, 153, 249))

        grenadeText = self._font.render("Grenades: " + str(self.grenades), True, (0, 0, 0))
        attackText = self._font.render("WE JAMMING: " + str(self.jamming), True, (0, 0, 0))

        for game_object in self.game_objects:
            game_object.draw(self._screen)

        if self.game_state == "PLAY":
            # draw noise
            Jam().draw(self._screen)

            #draw UI
            self._screen.blit(grenadeText, (100, 100))
            self._screen.blit(attackText, (100, 200))

        for button in self.buttons:
            button.draw(self._screen)

        self._screen.blit(self._screen, (0,0))

        pygame.display.flip()
    
    def instantiate(self, object):
        self.new_game_objects.add(object)