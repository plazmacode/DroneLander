import pygame

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class ButtonActions(metaclass=Singleton):
    def __init__(self) -> None:
        pass

    def run(self, action, button):
        """
        :param action: name of the action to be executed
        :param button: the button which called run()

        """
        from classes.MenuHandler import MenuHandler
        from classes.GameWorld import GameWorld
        if action == "play":
            GameWorld().start_game()

        if action == "options":
            MenuHandler().options_menu()

        if action == "quit":
            # send quit event
            quit_event = pygame.event.Event(pygame.QUIT)
            pygame.event.post(quit_event)
            
        if action == "mainMenu":
            MenuHandler().start_menu()

        if action == "changeDifficulty":
            if GameWorld().difficulty == 0:
                button.surface = button._font.render(str("Difficulty: Hard"), True, (255, 255, 255))
                GameWorld().difficulty = 1
                GameWorld().difficulty = 1
            elif GameWorld().difficulty == 1:
                button.surface = button._font.render(str("Difficulty: Easy"), True, (255, 255, 255))
                GameWorld().difficulty = 0
                GameWorld().difficulty = 0

        if action == "restartLevel":
            GameWorld().start_game()

        if action == "toggleSound":
            MenuHandler().toggle_sound()
            button.surface = button._font.render(str(MenuHandler().get_sound()), True, (255, 255, 255))

        if action == "toggleMusic":
            MenuHandler().toggle_music()
            if MenuHandler().music:
                button.surface = button._font.render(str("Music is ON"), True, (255, 255, 255))
            else:
                button.surface = button._font.render(str("Music is OFF"), True, (255, 255, 255))
