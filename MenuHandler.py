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
        self.sound = True
        self.music = True
        self.musicInitialized = False

    def startMenu(self):
        if self.musicInitialized == False:
            self.musicInitialized = True
            self.gameWorld.mixer.init()
            self.gameWorld.mixer.music.load("DroneLander8Bit.wav")
            self.gameWorld.mixer.music.set_volume(0.4)
            self.gameWorld.mixer.music.play(-1)
        self.gameWorld.buttons.clear()
        self.gameWorld.buttons.append(Button(buttonColor, hoverColor, pygame.Rect(self._screen_width / 2 -150, 300, 300, 80), "PLAY", self.gameWorld, "play"))
        self.gameWorld.buttons.append(Button(buttonColor, hoverColor, pygame.Rect(self._screen_width / 2 -150, 420, 300, 80), "OPTIONS", self.gameWorld, "options"))
        self.gameWorld.buttons.append(Button(buttonColor, hoverColor, pygame.Rect(self._screen_width / 2 -150, 540, 300, 80), "QUIT", self.gameWorld, "quit"))
        self.gameWorld.gameState = "MENU" #this is an enum trust me

    def optionsMenu(self):
        self.gameWorld.buttons.clear()
        self.gameWorld.buttons.append(Button(buttonColor, hoverColor, pygame.Rect(self._screen_width / 2 -150, 300, 300, 80), "Difficulty: Easy", self.gameWorld, "changeDifficulty"))
        self.gameWorld.buttons.append(Button(buttonColor, hoverColor, pygame.Rect(self._screen_width / 2 -150, 420, 300, 80), "Sound is ON", self.gameWorld, "toggleSound"))
        self.gameWorld.buttons.append(Button(buttonColor, hoverColor, pygame.Rect(self._screen_width / 2 -150, 540, 300, 80), "Music is ON", self.gameWorld, "toggleMusic"))
        self.gameWorld.buttons.append(Button(buttonColor, hoverColor, pygame.Rect(self._screen_width / 2 -150, 660, 300, 80), "BACK", self.gameWorld, "mainMenu"))

    def toggleSound(self):
        if self.sound == True:
            self.sound = False
        elif self.sound == False:
            self.sound = True

    def toggleMusic(self):
        if self.music == True:
            self.music = False
            self.gameWorld.mixer.music.set_volume(0)
        elif self.music == False:
            self.music = True
            self.gameWorld.mixer.music.set_volume(0.4)
