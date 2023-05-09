import pygame

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class HighscoreManager(metaclass=Singleton):
    """
    Class for making and mainting the highscore txt file
    """
    def __init__(self) -> None:
        try: # Creates a highscore file only if one does not exist yet
            with open("highscores.txt", "x") as hs:
                from classes.LevelLoader import LevelLoader
                for x in range(LevelLoader().max_levels):
                    hs.write(f'Level: {x + 1}, Highscore: 0\n')

                hs.close()

        except:
            pass
    
    def updateScore(self, score, level):
        """
        Takes a level and score, comparing against the existing score and replaces it if needed
        level: The target level for the update
        score: The score achived on this call
        """
        with open("highscores.txt") as hs:
            content = []   # Copies the txt file to temporary memory with an array
            for line in hs:
                content.append(line)

            hs.close()


            lineData = [int(s) for s in content[level - 1].split() if s.isdigit()]   # Exposes the score part of the string as an integer (as an array element because we're too stupid to do it directly)

            if (lineData[0] < score):   # Compare current score with input score
                with open("highscores.txt", "w") as hs:
                    for x in range(len(content)):   # Rebuilds the entire score text file as it was, changing only the line of the targeted level
                        if (x + 1 == level):
                            hs.write(f'Level: {x + 1}, Highscore: {score}\n')
                        else: 
                            hs.write(content[x])

                    hs.close()

    def getScore(self, level):
        with open("highscores.txt") as hs:
            content = []   # Copies the txt file to temporary memory with an array
            for line in hs:
                content.append(line)

            hs.close()

            lineData = [int(s) for s in content[level - 1].split() if s.isdigit()]   # Exposes the score part of the string as an integer (as an array element because we're too stupid to do it directly)

            return lineData[0]