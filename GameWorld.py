import pygame
from GameObject import GameObject
from Player import Player

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class GameWorld(metaclass=Singleton):
    def __init__(self):
        pygame.init()
        self._screen_width = 1920
        self._screen_height = 1080
        self._screen = pygame.display.set_mode((self._screen_width, self._screen_height))
        pygame.display.set_caption("Drone Lander")
        self._clock = pygame.time.Clock()
        self._font = pygame.font.SysFont(None, 48)
        self.grenades = 0
        self.player = Player(self)
        self.gameObjects = pygame.sprite.Group(self.player)
        self.newGameObjects = pygame.sprite.Group()

    def run(self):
        while True:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            self.update()
            self.draw()

            # Limit the frame rate
            self._clock.tick(60)
    
    def update(self):

        for go in self.newGameObjects:
            self.gameObjects.add(go)
        self.newGameObjects.empty()

        self.gameObjects.update()
        self.collisionCheck()

    def collisionCheck(self):
        for go1 in self.gameObjects:
            for go2 in self.gameObjects:
                if not go1 is go2:
                    if go1.rect.colliderect(go2.rect):
                        go1.onCollision(go2)

    def draw(self):
        # Clear the screen
        self._screen.fill((255, 255, 255))

        message = self._font.render("Grenades: " + str(self.grenades), True, (0, 0, 0))
        self.gameObjects.draw(self._screen)

        self._screen.blit(message, (100, 100))

        pygame.display.flip()
    
    def instantiate(self, object):
        self.newGameObjects.add(object)
        
game = GameWorld()
game.run()