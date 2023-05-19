import pygame
from classes.Button import Button
from classes.TextField import TextField
from classes.GameWorld import GameWorld
from classes.Singleton import Singleton
from classes.HighscoreManager import HighscoreManager
from classes.LevelLoader import LevelLoader

button_color = (34, 42, 104)
hover_color = (56, 55, 144)

class MenuHandler(metaclass=Singleton):
    """
    Handles switching between menus
    """
    def __init__(self) -> None:
        self._screen_width = GameWorld().screen_width
        self._screen_height = GameWorld().screen_height
        self.sound_enabled = True
        self.music_enabled = True
        self.lore = False
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
        GameWorld().text_fields.clear()
        GameWorld().game_objects = pygame.sprite.Group()


        """
        On the 22nd of February 2014, the Russian puppet Yanukovych was officially removed as Ukrainian president.
        Immediately following this, Russia invaded Ukraine annexing the territory of Crimea and sent unmarked troops into Luhansk and Donetsk.
        On the 24th of February 2022, Russia escalated this invasion to full scale war, trying to topple the democratically elected Ukrainian government.
        Today, Russia is still trying to subjugate Ukraine using war, destroying Ukrainian cities and killing Ukrainian citizens.

        This game is a statement of support for Ukraine and showcases a small aspect of the war. 
        Consumer drones are used to drop grenades, by making the smallest possible modifications.
        On some, a built-in auxiliary light feature is rewired to control a custom release mechanism instead.
        In the Ukrainian war, ‘Auxiliary Light On’ usually means ‘Bombs away’.


        """
        GameWorld().tutorial_text = pygame.sprite.Group()
        if self.lore:
            GameWorld().text_fields.append(TextField(button_color, (self._screen_width / 2, 820), "On the 22nd of February 2014, the Russian puppet Yanukovych was officially removed as Ukrainian president.", 48, "lore"))
            GameWorld().text_fields.append(TextField(button_color, (self._screen_width / 2, 848), "Immediately following this, Russia invaded Ukraine annexing the territory of Crimea and sent unmarked troops into Luhansk and Donetsk.", 48, "lore"))
            GameWorld().text_fields.append(TextField(button_color, (self._screen_width / 2, 872), "On the 24th of February 2022, Russia escalated this invasion to full scale war, trying to topple the democratically elected Ukrainian government.", 48, "lore"))
            GameWorld().text_fields.append(TextField(button_color, (self._screen_width / 2, 900), "Today, Russia is still trying to subjugate Ukraine using war, destroying Ukrainian cities and killing Ukrainian citizens.", 48, "lore"))

            GameWorld().text_fields.append(TextField(button_color, (self._screen_width / 2, 938), "On the 24th of February 2022, Russia escalated this invasion to full scale war, trying to topple the democratically elected Ukrainian government.", 48, "lore"))
            GameWorld().text_fields.append(TextField(button_color, (self._screen_width / 2, 962), "Consumer drones are used to drop grenades, by making the smallest possible modifications.", 48, "lore"))
            GameWorld().text_fields.append(TextField(button_color, (self._screen_width / 2, 986), "On some, a built-in auxiliary light feature is rewired to control a custom release mechanism instead.", 48, "lore"))
            GameWorld().text_fields.append(TextField(button_color, (self._screen_width / 2, 1010), "In the Ukrainian war, ‘Auxiliary Light On’ usually means ‘Bombs away’.", 48, "lore"))
        GameWorld().text_fields.append(TextField(button_color, (self._screen_width / 2, 200), "Auxiliary Light On", 48, "title"))
        GameWorld().buttons.append(Button(button_color, hover_color, pygame.Rect(self._screen_width / 2 -150, 300, 300, 80), "PLAY", "play"))
        GameWorld().buttons.append(Button(button_color, hover_color, pygame.Rect(self._screen_width / 2 -150, 420, 300, 80), "SELECT LEVEL", "select"))
        GameWorld().buttons.append(Button(button_color, hover_color, pygame.Rect(self._screen_width / 2 -150, 540, 300, 80), "OPTIONS", "options"))
        GameWorld().buttons.append(Button(button_color, hover_color, pygame.Rect(self._screen_width / 2 -150, 660, 300, 80), "QUIT", "quit"))
        GameWorld().buttons.append(Button(button_color, hover_color, pygame.Rect(self._screen_width / 2 + 450, 200, 40, 40), "?", "lore"))
        GameWorld().game_state = "MENU" #this is an enum trust me
    
    def select_level(self):
        GameWorld().buttons.clear()
        GameWorld().text_fields.clear()
        GameWorld().buttons.append(Button(button_color, hover_color, pygame.Rect(self._screen_width / 2 - 280, 300, 80, 80), "1", "loadLevel1"))
        GameWorld().buttons.append(Button(button_color, hover_color, pygame.Rect(self._screen_width / 2 - 160, 300, 80, 80), "2", "loadLevel2"))
        GameWorld().buttons.append(Button(button_color, hover_color, pygame.Rect(self._screen_width / 2 - 40, 300, 80, 80), "3", "loadLevel3"))
        GameWorld().buttons.append(Button(button_color, hover_color, pygame.Rect(self._screen_width / 2 + 80, 300, 80, 80), "4", "loadLevel4"))
        GameWorld().buttons.append(Button(button_color, hover_color, pygame.Rect(self._screen_width / 2 + 200, 300, 80, 80), "5", "loadLevel5"))
        GameWorld().buttons.append(Button(button_color, hover_color, pygame.Rect(self._screen_width / 2 - 280, 400, 80, 80), "6", "loadLevel6"))
        GameWorld().buttons.append(Button(button_color, hover_color, pygame.Rect(self._screen_width / 2 - 160, 400, 80, 80), "7", "loadLevel7"))
        GameWorld().buttons.append(Button(button_color, hover_color, pygame.Rect(self._screen_width / 2 - 40, 400, 80, 80), "8", "loadLevel8"))
        GameWorld().buttons.append(Button(button_color, hover_color, pygame.Rect(self._screen_width / 2 + 80, 400, 80, 80), "9", "loadLevel9"))
        GameWorld().buttons.append(Button(button_color, hover_color, pygame.Rect(self._screen_width / 2 + 200, 400, 80, 80), "10", "loadLevel10"))
        GameWorld().buttons.append(Button(button_color, hover_color, pygame.Rect(self._screen_width / 2 -150, 660, 300, 80), "BACK", "mainMenu"))
        GameWorld().text_fields.append(TextField(button_color, (self._screen_width / 2, 100), "                        ", 48, "LevelSelectHighscore"))


    def end_menu(self):
        """
        End screen menu
        """
        GameWorld().buttons.clear()
        GameWorld().text_fields.clear()

        # Show NEXT LEVEL button if objective completed
        if GameWorld().main_objective_completed:
            GameWorld().buttons.append(Button(button_color, hover_color, pygame.Rect(self._screen_width / 2 -150, 180, 300, 80), "NEXT LEVEL", "nextLevel"))
            GameWorld().buttons.append(Button(button_color, hover_color, pygame.Rect(self._screen_width / 2 -150, 300, 300, 80), "PLAY AGAIN", "restartLevel"))
        else:
            GameWorld().buttons.append(Button(button_color, hover_color, pygame.Rect(self._screen_width / 2 -150, 300, 300, 80), "PLAY AGAIN", "restartLevel"))
        GameWorld().buttons.append(Button(button_color, hover_color, pygame.Rect(self._screen_width / 2 -150, 420, 300, 80), "OPTIONS", "options"))
        GameWorld().buttons.append(Button(button_color, hover_color, pygame.Rect(self._screen_width / 2 -150, 540, 300, 80), "MAIN MENU", "mainMenu"))
        GameWorld().buttons.append(Button(button_color, hover_color, pygame.Rect(self._screen_width / 2 -150, 780, 300, 80), "QUIT", "quit"))
        GameWorld().game_state = "ENDMENU"

    def options_menu(self):
        """
        Options menu
        """
        GameWorld().buttons.clear()
        GameWorld().text_fields.clear()

        GameWorld().buttons.append(Button(button_color, hover_color, pygame.Rect(self._screen_width / 2 -150, 300, 300, 80), self.get_difficulty(), "changeDifficulty"))
        GameWorld().buttons.append(Button(button_color, hover_color, pygame.Rect(self._screen_width / 2 -150, 420, 300, 80), self.get_sound(), "toggleSound"))
        GameWorld().buttons.append(Button(button_color, hover_color, pygame.Rect(self._screen_width / 2 -150, 540, 300, 80), self.get_music(), "toggleMusic"))
        if GameWorld().game_state == "MENU":
            GameWorld().buttons.append(Button(button_color, hover_color, pygame.Rect(self._screen_width / 2 -150, 660, 300, 80), "BACK", "mainMenu"))
        else:
            GameWorld().buttons.append(Button(button_color, hover_color, pygame.Rect(self._screen_width / 2 -150, 660, 300, 80), "BACK", "endMenu"))

    def score_screen(self):
        """
        Score screen
        """
        HighscoreManager().updateScore(GameWorld().score, LevelLoader().current_level)
        GameWorld().buttons.clear()
        GameWorld().text_fields.clear()

        GameWorld().buttons.append(Button(button_color, hover_color, pygame.Rect(self._screen_width / 2 -150, 660, 300, 80), "CONTINUE", "endMenu"))
        GameWorld().text_fields.append(TextField(button_color, (self._screen_width / 2, 100), "Highscore: " + str(HighscoreManager().getScore(LevelLoader().current_level)), 48, "highscore"))
        GameWorld().text_fields.append(TextField(button_color, (self._screen_width / 2, 200), "Score: " + str(GameWorld().score), 48, "score"))
        GameWorld().text_fields.append(TextField(button_color, (self._screen_width / 2, 400), GameWorld().endscreen_string, 48, "endmessage"))
        GameWorld().game_state = "SCORESCREEN"

    def get_sound(self):
        if self.sound_enabled:
            return "SOUND IS: ON"
        else:
            return "SOUND IS: OFF"
        
    def get_music(self):
        if self.music_enabled:
            return "MUSIC IS: ON"
        else:
            return "MUSIC IS: OFF"

    def get_difficulty(self):
        if GameWorld().difficulty == 0:
            return "DIFFICULTY: EASY"
        elif GameWorld().difficulty == 1:
            return "DIFFICULTY: MEDIUM"
        elif GameWorld().difficulty == 2:
            return "DIFFICULTY: HARD"


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
        if self.music_enabled == True:
            self.music_enabled = False
            GameWorld().mixer.music.set_volume(0)
        elif self.music_enabled == False:
            self.music_enabled = True
            GameWorld().mixer.music.set_volume(0.2)

    def toggle_lore(self):
        """
        Toggles lore text
        """
        if self.lore == True:
            self.lore = False

        elif self.lore == False:
            self.lore = True
        self.start_menu()

