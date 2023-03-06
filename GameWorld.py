import pygame
from GameObject import GameObject
from Environment import Environment
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
        self._screen_width = 1600
        self._screen_height = 900
        self._screen = pygame.display.set_mode((self._screen_width, self._screen_height))
        pygame.display.set_caption("Template")
        self._clock = pygame.time.Clock()
        self._font = pygame.font.SysFont(None, 48)
        self.player = Player()
        self.gameObjects = pygame.sprite.Group(self.player)

        self.gameObjects.add(Environment("Ground", 0, 850))
        self.gameObjects.add(Environment("TreeTrunk", 1000, 400))
        self.gameObjects.add(Environment("TreeCrown", 850, 80))
        self.gameObjects.add(Environment("AmmoDump(Shells)", 500, 700))
        # self.gameObjects.add(Environment("DetonationDecal", 0, 850))


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
        for i in self.gameObjects:
            i.update()

    def draw(self):
        # Clear the screen
        self._screen.fill((63, 153, 249))

        message = self._font.render(str(len(self.gameObjects)), True, (255, 255, 255))
        self.gameObjects.draw(self._screen)
        # for i in self.gameObjects:
        #     i.draw(self._screen)


        self._screen.blit(message, (100, 100))

        pygame.display.flip()
        
game = GameWorld()
game.run()
# if __name__ == "__main__":