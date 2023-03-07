import pygame
from Button import Button

buttonColor = (34, 42, 104)
hoverColor = (24, 32, 94)

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class MenuHandler(metaclass=Singleton):
    def __init__(self, gameWorld) -> None:
        self.gameWorld = gameWorld
        self._screen_width = self.gameWorld.screen_width
        self._screen_height = self.gameWorld.screen_height

    def startMenu(self):
        self.gameWorld.buttons.clear()
        self.gameWorld.buttons.append(Button(buttonColor, hoverColor, pygame.Rect(self._screen_width / 2 -150, 300, 300, 80), "PLAY", self.gameWorld, "play"))
        self.gameWorld.buttons.append(Button(buttonColor, hoverColor, pygame.Rect(self._screen_width / 2 -150, 420, 300, 80), "OPTIONS", self.gameWorld, "options"))
        self.gameWorld.buttons.append(Button(buttonColor, hoverColor, pygame.Rect(self._screen_width / 2 -150, 540, 300, 80), "QUIT", self.gameWorld, "quit"))
        self.gameWorld.gameState = "MENU" #this is an enum trust me

    def optionsMenu(self):
        self.gameWorld.buttons.clear()
        self.gameWorld.buttons.append(Button(buttonColor, hoverColor, pygame.Rect(self._screen_width / 2 -150, 300, 300, 80), "Difficulty: Easy", self.gameWorld, "changeDifficulty"))
        self.gameWorld.buttons.append(Button(buttonColor, hoverColor, pygame.Rect(self._screen_width / 2 -150, 420, 300, 80), "Sound is ON", self.gameWorld, "toggleSound"))
        self.gameWorld.buttons.append(Button(buttonColor, hoverColor, pygame.Rect(self._screen_width / 2 -150, 540, 300, 80), "BACK", self.gameWorld, "mainMenu"))

    def toggleSound(self):
        pass