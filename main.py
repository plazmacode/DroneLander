# main.py
from GameWorld import GameWorld

# Only run the game if it is executed as the main script.
# If this is imported as a module nothing is executed
if __name__ == "__main__":
    game = GameWorld()
    game.run()