import pygame
from classes.Singleton import Singleton
from classes.LevelLoader import LevelLoader

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

        if action == "endMenu":
            MenuHandler().end_menu()

        if action == "select":
            MenuHandler().select_level()

        if action == "changeDifficulty":
            GameWorld().difficulty += 1

            if GameWorld().difficulty > 2:
                GameWorld().difficulty = 0

            if GameWorld().difficulty == 0:
                button.text_surface = button._font.render(str("DIFFICULTY: EASY"), True, (255, 255, 255))
                button.redraw()
            elif GameWorld().difficulty == 1:
                button.text_surface = button._font.render(str("DIFFICULTY: MEDIUM"), True, (255, 255, 255))
                button.redraw()
            elif GameWorld().difficulty == 2:
                button.text_surface = button._font.render(str("DIFFICULTY: HARD"), True, (255, 255, 255))
                button.redraw()

        if action == "nextLevel":
            LevelLoader().next_level()

        if action == "restartLevel":
            GameWorld().start_game()

        if "loadLevel" in action:
            # if action contains "loadLevel" use the number to load that level
            # loadLevel1, loadLevel2 etc.
            level = int(action.replace("loadLevel", ""))
            LevelLoader().current_level = level
            LevelLoader().load_level(0)

        # toggle sound and update button text
        if action == "toggleSound":
            MenuHandler().toggle_sound()
            button.text_surface = button._font.render(str(MenuHandler().get_sound()), True, (255, 255, 255))
            button.redraw()

        # toggle music and update button text
        if action == "toggleMusic":
            MenuHandler().toggle_music()
            button.text_surface = button._font.render(str(MenuHandler().get_music()), True, (255, 255, 255))
            button.redraw()

        if action == "lore":
            MenuHandler().toggle_lore()