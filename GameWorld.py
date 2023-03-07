import pygame
from GameObject import GameObject
from Environment import Environment
from Player import Player
from Button import Button
from MenuHandler import MenuHandler

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class GameWorld(metaclass=Singleton):
    def __init__(self):
        pygame.init()
        self.screen_width = 1920
        self.screen_height = 1080
        self._screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Drone Lander")
        self._clock = pygame.time.Clock()
        self._font = pygame.font.SysFont(None, 48)
        self.grenades = 0
        self.player = Player(self)
        self.gameObjects = pygame.sprite.Group(self.player)
        self.newGameObjects = pygame.sprite.Group()
        self.gameObjects.add(Environment("Ground", (1000, 1055), self))
        self.gameObjects.add(Environment("TreeTrunk", (1200, 800), self))
        self.gameObjects.add(Environment("TreeCrown", (1200, 400), self))
        self.gameObjects.add(Environment("AmmoDump(Shells)", (500, 955), self))
        self.buttons = []
        self.mixer = pygame.mixer
        MenuHandler(self).startMenu()
        self.difficulty = 0
        self.gameState = "MENU"

    def startGame(self):
        self.gameState = "PLAY"
        self.buttons.clear()
        self.gameObjects.add(Player(self))
        self.gameObjects.add(Environment("Ground", 0, 850))
        self.gameObjects.add(Environment("TreeTrunk", 1000, 400))
        self.gameObjects.add(Environment("TreeCrown", 850, 80))
        self.gameObjects.add(Environment("AmmoDump(Shells)", 500, 700))
        # self.gameObjects.add(Environment("DetonationDecal", 0, 850))

    def run(self):
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

        for go in self.newGameObjects:
            self.gameObjects.add(go)
        
        self.newGameObjects.empty()

        self.gameObjects.update()
        self.collisionCheck()

        for button in self.buttons:
            button.update(event_list)

    def collisionCheck(self):
        for go1 in self.gameObjects:
            for go2 in self.gameObjects:
                if not go1 is go2:
                    if go1.rect.colliderect(go2.rect):
                        go1.onCollision(go2)

    def draw(self):
        # Clear the screen
        self._screen.fill((63, 153, 249))

        message = self._font.render("Grenades: " + str(self.grenades), True, (0, 0, 0))
        self.gameObjects.draw(self._screen)

        if self.gameState == "PLAY":
            self._screen.blit(message, (100, 100))

        for button in self.buttons:
            button.draw(self._screen)

        pygame.display.flip()
    
    def instantiate(self, object):
        self.newGameObjects.add(object)
        
game = GameWorld()
game.run()