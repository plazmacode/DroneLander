import pygame

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class ButtonActions(metaclass=Singleton):
    def __init__(self, gameWorld) -> None:
        self.gameWorld = gameWorld

    def run(self, action, gameworld, button):
        from MenuHandler import MenuHandler
        if action == "play":
            self.gameWorld.startGame()

        if action == "options":
            MenuHandler(self.gameWorld).optionsMenu()

        if action == "quit":
            pygame.quit()

        if action == "mainMenu":
            MenuHandler(self.gameWorld).startMenu()

        if action == "changeDifficulty":
            if gameworld.difficulty == 0:
                button.surface = button._font.render(str("Difficulty: Hard"), True, (255, 255, 255))
                gameworld.difficulty = 1
                gameworld.difficulty = 1
            elif gameworld.difficulty == 1:
                button.surface = button._font.render(str("Difficulty: Easy"), True, (255, 255, 255))
                gameworld.difficulty = 0
                gameworld.difficulty = 0


        if action == "toggleSound":
            MenuHandler(self.gameWorld).toggleSound()
