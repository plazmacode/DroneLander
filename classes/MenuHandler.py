import pygame
from classes.Button import Button
from classes.GameWorld import GameWorld

button_color = (34, 42, 104)
hover_color = (24, 32, 94)

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class MenuHandler(metaclass=Singleton):
    """
    Handles switching between menus
    """
    def __init__(self) -> None:
        self._screen_width = GameWorld().screen_width
        self._screen_height = GameWorld().screen_height
        self.sound_enabled = True
        self.music = True
        self.music_initialized = False

    def start_menu(self):
        """
        Start menu
        """
        if self.music_initialized == False:
            self.music_initialized = True
            GameWorld().mixer.init()
            GameWorld().mixer.music.load(".\sounds\DroneLander8Bit.wav")
            GameWorld().mixer.music.set_volume(0.2)
            GameWorld().mixer.music.play(-1)
        GameWorld().buttons.clear()
        GameWorld().game_objects = pygame.sprite.Group()
        GameWorld().buttons.append(Button(button_color, hover_color, pygame.Rect(self._screen_width / 2 -150, 300, 300, 80), "PLAY", "play"))
        GameWorld().buttons.append(Button(button_color, hover_color, pygame.Rect(self._screen_width / 2 -150, 420, 300, 80), "OPTIONS", "options"))
        GameWorld().buttons.append(Button(button_color, hover_color, pygame.Rect(self._screen_width / 2 -150, 540, 300, 80), "QUIT", "quit"))
        GameWorld().game_state = "MENU" #this is an enum trust me

    def end_menu(self):
        """
        End screen menu
        """
        GameWorld().buttons.clear()
        GameWorld().buttons.append(Button(button_color, hover_color, pygame.Rect(self._screen_width / 2 -150, 300, 300, 80), "RESTART", "restartLevel"))
        GameWorld().buttons.append(Button(button_color, hover_color, pygame.Rect(self._screen_width / 2 -150, 420, 300, 80), "OPTIONS", "options"))
        GameWorld().buttons.append(Button(button_color, hover_color, pygame.Rect(self._screen_width / 2 -150, 540, 300, 80), "MAIN MENU", "mainMenu"))
        GameWorld().buttons.append(Button(button_color, hover_color, pygame.Rect(self._screen_width / 2 -150, 660, 300, 80), "QUIT", "quit"))
        GameWorld().game_state = "ENDMENU"

    def options_menu(self):
        """
        Options menu
        """
        GameWorld().buttons.clear()
        GameWorld().buttons.append(Button(button_color, hover_color, pygame.Rect(self._screen_width / 2 -150, 300, 300, 80), "Difficulty: Easy", "changeDifficulty"))
        GameWorld().buttons.append(Button(button_color, hover_color, pygame.Rect(self._screen_width / 2 -150, 420, 300, 80), self.get_sound(), "toggleSound"))
        GameWorld().buttons.append(Button(button_color, hover_color, pygame.Rect(self._screen_width / 2 -150, 540, 300, 80), "Music is ON", "toggleMusic"))
        GameWorld().buttons.append(Button(button_color, hover_color, pygame.Rect(self._screen_width / 2 -150, 660, 300, 80), "BACK", "mainMenu"))

    def get_sound(self):
        if self.sound_enabled:
            return "Sound is ON"
        else:
            return "Sound is OFF"

    def toggle_sound(self):
        """
        Toggles sound effects on and off
        """
        if self.sound_enabled == True:
            self.sound_enabled = False
        elif self.sound_enabled == False:
            self.sound_enabled = True

    def toggle_music(self):
        """
        Toggles music on and off
        """
        if self.music == True:
            self.music = False
            GameWorld().mixer.music.set_volume(0)
        elif self.music == False:
            self.music = True
            GameWorld().mixer.music.set_volume(0.2)
