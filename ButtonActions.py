import pygame

class ButtonActions():
    def __init__(self) -> None:
        pass

    def run(self, text, gameworld):
        if text == "PLAY":
            gameworld.gameState = "PLAY"
            gameworld.startGame()

        if text == "QUIT":
            pygame.quit()
