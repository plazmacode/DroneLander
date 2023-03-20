import pygame
from classes.Environment import Environment
from classes.TutorialText import TutorialText
from classes.Player import Player
from classes.Jammer import Jammer
from classes.TextField import TextField
from classes.Parallax import Parallax
from classes.Singleton import Singleton


class LevelLoader(metaclass=Singleton):
    """
    Handles loading of levels
    """
    def __init__(self) -> None:
        self.current_level = 1
        self.max_levels = 2
        self.grenade_count = 0

    def next_level(self):
        """
        increments current level and loads that level
        current_level is important for the function of the "play again" and "next level" buttons
        """
        self.current_level += 1
        self.load_level(self.current_level)

    def load_level(self, value):
        """
        Loads a given level

        param value: number of level to be loaded

        supports loading the max level and a default to load the current level
        """
        from classes.GameWorld import GameWorld
        self.clear_level()
        match value:
            case 0:
                # loads current level
                self.load_level(self.current_level)
            case 1:
                self.load_level1()
            case 2:
                self.load_level2()
            case _ if value > self.max_levels:
                # if we are at max levels
                # remember to update
                self.load_level(self.current_level)
            case _:
                # python uses "_" for default case
                # default case laods current level
                self.load_level(self.current_level)
            
        GameWorld().game_objects.add(Player())
        Player().initialize_values()

    def clear_level(self):
        """
        clears the game_objects, and other lists.
        Resets score, objective, timer etc. to reset level
        """
        from classes.GameWorld import GameWorld
        GameWorld().game_state = "PLAY"
        GameWorld().buttons.clear()

        GameWorld().objectives_completed = 0
        GameWorld().main_objective_completed = False

        GameWorld().score = 0
        GameWorld().level_time = 0
        GameWorld().level_start_time = pygame.time.get_ticks()
        GameWorld().game_objects = pygame.sprite.Group()
        GameWorld().tutorial_text = pygame.sprite.Group()

        GameWorld().buttons.append(TextField((34, 42, 104), (GameWorld().screen_width / 2, 200), "Score: " + str(GameWorld().score), 48, "score"))
        
        # Resets parallax
        Parallax().reset_position()

    def load_level1(self):
        from classes.GameWorld import GameWorld

        self.grenade_count = 2

        # Place floor, value sets number of tiles placed
        for x in range(5):
            GameWorld().game_objects.add(Environment("Ground", (x * 2000, 1055), "Obstacle"))
        # Left bounds "wall"
        GameWorld().game_objects.add(Environment("TreeTrunk", (000, 800), "Background"))
        GameWorld().game_objects.add(Environment("TreeCrown", (000, 405), "Obstacle"))
        GameWorld().game_objects.add(Environment("TreeCrown", (-200, 935), "Obstacle"))

        # Launch brick
        GameWorld().game_objects.add(Environment("Brick", (960, 1015), "Brick"))

        # Tutorial Text
        GameWorld().tutorial_text.add(TutorialText("Press W to thrust, Press A or D to rotate", (600, 800)))
        GameWorld().tutorial_text.add(TutorialText("Press SPACE to release grenades", (600, 850)))
        GameWorld().tutorial_text.add(TutorialText("Destroy side objective to earn score", (1800, 800)))
        GameWorld().tutorial_text.add(TutorialText("This is the main objective, destroy it and fly back", (3500, 800)))
        GameWorld().tutorial_text.add(TutorialText("Height limit above this text", (600, 250)))

        # See TutorialText.py 
        GameWorld().tutorial_text.add(TutorialText("Main objective completed land here", (600, 1000)))

        # Tree
        GameWorld().game_objects.add(Environment("TreeTrunk", (1500, 800), "Background"))
        GameWorld().game_objects.add(Environment("TreeCrown", (1500, 405), "Obstacle"))

        # First ammo dump
        GameWorld().game_objects.add(Environment("AmmoDump(Shells)", (2200, 955), "Obstacle"))

        # Bush
        GameWorld().game_objects.add(Environment("TreeCrown", (2600, 935), "Obstacle"))
        GameWorld().game_objects.add(Environment("TreeCrown", (2900, 955), "Obstacle"))

        # Last ammo dump (main objective) + right bounds "wall" 
        GameWorld().main_objective_object = Environment("AmmoDump(Shells)", (3800, 955), "Obstacle")
        GameWorld().main_objective_object.main_objective = True
        GameWorld().game_objects.add(GameWorld().main_objective_object)
        GameWorld().game_objects.add(Environment("TreeTrunk", (4000, 805), "Background"))
        GameWorld().game_objects.add(Environment("TreeCrown", (4000, 400), "Obstacle"))
        GameWorld().game_objects.add(Environment("TreeCrown", (4250, 955), "Obstacle"))

    def load_level2(self):
        from classes.GameWorld import GameWorld
        # Place floor, value sets number of tiles placed

        self.grenade_count = 4

        for x in range(5):
            GameWorld().game_objects.add(Environment("Ground", (x * 2000, 1055), "Obstacle"))
        # Left bounds "wall"
        GameWorld().game_objects.add(Environment("TreeTrunk", (000, 800), "Background"))
        GameWorld().game_objects.add(Environment("TreeCrown", (000, 405), "Obstacle"))
        GameWorld().game_objects.add(Environment("TreeCrown", (-200, 935), "Obstacle"))

        # Launch brick
        GameWorld().game_objects.add(Environment("Brick", (960, 1015), "Brick"))

        # Bush
        GameWorld().game_objects.add(Environment("TreeCrown", (500, 935), "Obstacle"))

        # Tree patch
        GameWorld().game_objects.add(Environment("TreeTrunk", (1910, 780), "Background"))
        GameWorld().game_objects.add(Environment("TreeTrunk", (2330, 780), "Background"))
        GameWorld().game_objects.add(Environment("TreeTrunk", (1700, 800), "Background"))
        GameWorld().game_objects.add(Environment("TreeCrown", (1700, 395), "Obstacle"))
        GameWorld().game_objects.add(Environment("TreeTrunk", (2560, 800), "Background"))
        GameWorld().game_objects.add(Environment("TreeCrown", (2560, 405), "Obstacle"))
        GameWorld().game_objects.add(Environment("TreeTrunk", (2120, 790), "Background"))
        GameWorld().game_objects.add(Environment("TreeCrown", (2120, 405), "Obstacle"))

        # Ammo dump under tree
        GameWorld().game_objects.add(Environment("TreeTrunk", (3500, 790), "Background"))
        GameWorld().game_objects.add(Environment("TreeCrown", (3500, 405), "Obstacle"))
        GameWorld().game_objects.add(Environment("AmmoDump(Shells)", (3500, 955), "Obstacle"))

        # Ammo dump between bushes
        GameWorld().game_objects.add(Environment("AmmoDump(Shells)", (4750, 955), "Obstacle"))
        GameWorld().game_objects.add(Environment("TreeCrown", (4400, 935), "Obstacle"))
        GameWorld().game_objects.add(Environment("TreeCrown", (5100, 935), "Obstacle"))

        # Tree
        GameWorld().game_objects.add(Environment("TreeTrunk", (5860, 790), "Background"))
        GameWorld().game_objects.add(Environment("TreeCrown", (5860, 405), "Obstacle"))

        # Jammer + right bounds "wall"
        GameWorld().game_objects.add(Environment("TreeTrunk", (6860, 790), "Background"))
        GameWorld().game_objects.add(Environment("TreeCrown", (6860, 405), "Obstacle"))
        GameWorld().game_objects.add(Environment("AmmoDump(Shells)", (6710, 955), "Obstacle"))
        GameWorld().game_objects.add(Environment("TreeCrown", (7000, 935), "Obstacle"))
        GameWorld().main_objective_object = Jammer((6500, 905))
        GameWorld().main_objective_object.main_objective = True
        GameWorld().game_objects.add(GameWorld().main_objective_object)