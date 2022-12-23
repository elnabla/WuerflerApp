import time

from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.behaviors.toggle_behavior import MDToggleButton
from kivymd.uix.button import MDRoundFlatButton

kv = """
#: import labels labels

<CameraClick>:
    orientation: 'vertical'
    Label: 
        height: "1dp"
        valign: "top"
    Camera:
        id: camera
        resolution: (100,100)
        allow_stretch: True
        keep_ratio: True
        play: True
    MDRoundFlatButton:
        text: 'Capture'
        size_hint_y: None
        halign: "center"
        height: '48dp'
        on_press: root.capture()

Screen:
    BoxLayout:
        orientation: 'vertical'
        MDTopAppBar:
            title: "Würfler"
            left_action_items: [["menu", lambda x: nav_draw.set_state()]]
        Widget:
    MDNavigationLayout:    
        ScreenManager:
            id: screen_manager
            Screen:
                name: "scr-score"

                CameraClick:

            Screen:
                name: "scr-rules"

                MDBoxLayout: 
                    adaptive_height: True
                    adaptive_witdh: True
                    orientation: "vertical"

                    MDLabel:
                        text: "Würfler rules"
                        halign: "center"
                        valign: "top"
                    MDLabel: 
                        halign: "left"
                        valign: "top"
                        text: labels.rules




        MDNavigationDrawer:
            id: nav_draw
            orientation: "vertical"
            padding: "8dp"
            spacing: "8dp"

            AnchorLayout:
                anchor_x: "left"
                size_hint_y: None
                height: avatar.height

                Image:
                    id: avatar
                    size_hint: None, None
                    size: "56dp", "56dp"
                    source: "data/logo/kivy-icon-256.png"

            MDLabel:
                text: "Würfler"
                font_style: "Button"
                size_hint_y: None
                height: self.texture_size[1]

            MDLabel:
                text: "made by banban"
                font_style: "Caption"
                size_hint_y: None
                height: self.texture_size[1]

            ScrollView:
                MDList:
                    OneLineAvatarListItem:
                        on_press:
                            nav_draw.set_state("close")
                            screen_manager.current = "scr-score"

                        text: "Scoring"
                        IconLeftWidget:
                            icon: "electron-framework"

                    OneLineAvatarListItem:
                        on_press:
                            nav_draw.set_state("close")
                            screen_manager.current = "scr-rules"
                        text: "Rules"
                        IconLeftWidget:
                            icon: 'information'

            Widget:
"""


class CameraClick(BoxLayout):
    def capture(self):
        """
        Function to capture the images and give them the names
        according to their captured time and date.
        """
        camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        camera.export_to_png("IMG_{}.png".format(timestr))
        print("Captured")


class MyToggleButton(MDRoundFlatButton, MDToggleButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.background_down = self.theme_cls.primary_color


class CameraClick(BoxLayout):
    def capture(self):
        """
        Function to capture the images and give them the names
        according to their captured time and date.
        """
        camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        camera.export_to_png("IMG_{}.png".format(timestr))
        print("Captured")


class Main(MDApp):

    def build(self):
        return Builder.load_string(kv)


Main().run()
