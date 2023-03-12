import pygame
from GameObject import GameObject
from Environment import Environment
from Player import Player
from classes.Button import Button

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class GameWorld(metaclass=Singleton):
    def __init__(self):
        pygame.init()
        self._screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN, pygame.RESIZABLE)
        self.screen_width = self._screen.get_width()
        self.screen_height = self._screen.get_height()
        self.screen_ratio_x = self.screen_width / 1920
        self.screen_ratio_y = self.screen_height / 1080
        pygame.display.set_caption("Drone Lander")
        self._clock = pygame.time.Clock()
        self._font = pygame.font.SysFont(None, 48)
        self.grenades = 0
        self.difficulty = 0
        self.game_objects = pygame.sprite.Group()
        self.new_game_objects = pygame.sprite.Group()
        self.buttons = []
        self.mixer = pygame.mixer

        self.game_state = "MENU"

    def start_game(self):
        self.game_state = "PLAY"
        self.buttons.clear()
        self.game_objects.add(Player())
        self.game_objects.add(Environment("Ground", self.scale_pos((1000, 1055))))
        self.game_objects.add(Environment("TreeTrunk", self.scale_pos((1200, 800))))
        self.game_objects.add(Environment("TreeCrown", self.scale_pos((1200, 400))))
        self.game_objects.add(Environment("AmmoDump(Shells)", self.scale_pos((500, 955))))
        # self.gameObjects.add(Environment("DetonationDecal", 0, 850))

    # value is a tuple position where this method returns a tuple that scales to fit the screen
    # assuming the coordinates send to this was from a 1920 by 1080 display
    # this makes the game show correctly on smaller screens
    def scale_pos(self, value):
        return (value[0] * self.screen_ratio_x, value[1] * self.screen_ratio_y)

    def run(self):
        from MenuHandler import MenuHandler
        MenuHandler().start_menu()
        while True:
            # Handle events
            event_list = pygame.event.get()
            for event in event_list:
                if event.type == pygame.QUIT:
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

        message = self._font.render("Grenades: " + str(self.grenades), True, (0, 0, 0))
        self.game_objects.draw(self._screen)

        if self.game_state == "PLAY":
            self._screen.blit(message, (100, 100))

        for button in self.buttons:
            button.draw(self._screen)

        pygame.display.flip()
    
    def instantiate(self, object):
        self.new_game_objects.add(object)
        
# game = GameWorld()
# game.run()