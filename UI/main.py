from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivy.core.window import Window
from kivymd.uix.navigationdrawer import MDNavigationDrawer

Window.size = (450, 800)  # to see how it looks in portrait mode


class MyScreen(Screen):
    pass


class StartScreen(Screen):
    pass


class WuerflerNavigationDrawer(MDNavigationDrawer):
    pass


class WuerflerUiApp(MDApp):
    def build(self):
        return MyScreen()


if __name__ == "__main__":
    WuerflerUiApp().run()
