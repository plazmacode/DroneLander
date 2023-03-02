import pygame
from GameObject import GameObject

class GameWorld:
    def __init__(self):
        pygame.init()
        self._screen_width = 800
        self._screen_height = 600
        self._screen = pygame.display.set_mode((self._screen_width, self._screen_height))
        pygame.display.set_caption("Template")
        self._clock = pygame.time.Clock()
        self._font = pygame.font.SysFont(None, 48)
        self.gameObject = GameObject()
        self.gameObjects = [self.gameObject]
        self.gameObjects.append(self.gameObject)

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
        
        # for i in len(self.gameObjects):
        #     self.gameObjects[i].update()

    def draw(self):
        # Clear the screen
        self._screen.fill((0, 0, 0))

        for i in self.gameObjects:
            i.draw(self._screen)

        pygame.display.flip()


if __name__ == "__main__":
    game = GameWorld()
    game.run()