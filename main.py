from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivy.lang import Builder

from kivy.core.window import Window

Window.size = (450, 800)  # to see how it looks in portrait mode


class MyScreen(Screen):
    pass


class WuerflerUiApp(MDApp):
    def build(self):
        return MyScreen()


if __name__ == "__main__":
    WuerflerUiApp().run()
