import pygame
from GameObject import GameObject

class GameWorld:
    def __init__(self):
        pygame.init()
        self._screen_width = 1920
        self._screen_height = 1080
        self._screen = pygame.display.set_mode((self._screen_width, self._screen_height))
        pygame.display.set_caption("Template")
        self._clock = pygame.time.Clock()
        self._font = pygame.font.SysFont(None, 48)
        self.gameObject = GameObject()
        self.gameObject2 = GameObject()
        self.gameObjects = [self.gameObject]
        self.gameObjects.append(self.gameObject2)

        self.sprite_image = pygame.image.load("grenade.png")
        self.sprite_image = pygame.transform.scale(self.sprite_image, (50, 80))
        self.sprite = pygame.sprite.Sprite()

        self.sprite.rect = self.sprite_image.get_rect()
        self.sprite.rect.x = 100
        self.sprite.rect.y = 100


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
        self._screen.fill((63, 153, 249))

        self._screen.blit(self.sprite_image, self.sprite.rect)

        for i in self.gameObjects:
            i.draw(self._screen)

        pygame.display.flip()


if __name__ == "__main__":
    game = GameWorld()
    game.run()