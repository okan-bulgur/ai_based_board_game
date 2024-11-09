from MenuScreen import MenuScreen
from src import ScreenManager as sm

if __name__ == '__main__':
    menuScreen = MenuScreen()
    sm.change_screen(menuScreen)