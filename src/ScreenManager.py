from src.GameScreen import GameScreen
from src.MenuScreen import MenuScreen

menuScreen = MenuScreen()
gameScreen = GameScreen()

def change_screen(screen):
    screen.setup()
    screen.update()