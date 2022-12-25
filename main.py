import threading
import os
import time

from kivy.clock import Clock
from kivy.properties import BooleanProperty
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.behaviors.toggle_behavior import MDToggleButton
from kivymd.uix.button import MDRoundFlatButton

from kivy.core.window import Window

Window.size = (450, 800)  # to see how it looks in portrait mode

kv = """
#: import labels labels
#: import time time 
#: import NoTransition kivy.uix.screenmanager.NoTransition
<CameraClick>:
    Camera:
        id: camera
        resolution: (640,380)
        allow_stretch: True
        keep_ratio: True
        play: True
        
<WaitScreen>:  
    BoxLayout:
        orientation: "vertical"
       
        MDTopAppBar: 
            title: "Würfler image"
            left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]
        
        MDLabel:
            size_hint_y: None
            halign: "center"
            text: "Loading image..."
           
        MDSpinner:
            size_hint: None, None
            size: dp(46), dp(46)
            pos_hint: {'center_x': .5, 'center_y': .5}
            active: True 
        
            
        Widget: 

    

Screen:
    MDNavigationLayout:    
    
        ScreenManager:
            id: screen_manager
            
            Screen: 
                name: "scr-start"
                
                BoxLayout:
                    orientation: "vertical"
                    
                    MDTopAppBar: 
                        title: "Würfler Start"
                        left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]
                    
                    MDLabel: 
                        text: "How many players ?"
                        
                    MDTextField:
                        id: n_players
                        helper_text: "Number of players"
                        input_filter: "int"
                        input_type: "number" 
                    MDRoundFlatButton: 
                        text: "next"
                        on_press: screen_manager.current = "scr-names"           
                    Widget: 
                    
            Screen: 
                name: "scr-names"
                
                BoxLayout:
                    orientation: "vertical"
                    
                    MDTopAppBar: 
                        title: "Würfler Enter Names"
                        left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]
                    
                    MDLabel: 
                        text: "Name of player one"
                       
                    MDTextField:
                        id: player_name
                        helper_text: "name"
                        input_type: "text" 
                    MDRoundFlatButton: 
                        text: "next"
                        on_press: screen_manager.current = "scr-camera"           
                    Widget:
            
            Screen:
                name: "scr-camera"
                
                BoxLayout:
                    orientation: "vertical"
                    
                    MDTopAppBar: 
                        title: f"Würfler Capture for {player_name.text}"
                        left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]
                   
                    AnchorLayout:
                        anchor_x: "center"
                        anchor_y: "bottom" 
                        
                        CameraClick:
                            id: camera
                
                        MDRoundFlatButton:
                            text: 'Capture'
                            height: '48dp'
                            on_press: 
                                camera.capture()
                                screen_manager.transition = NoTransition()
                                screen_manager.current = "scr-await-image"
            
            WaitScreen: 
                name: "scr-await-image"        
                                               
            Screen: 
                name: "scr-show-image"
                
                BoxLayout:
                    orientation: "vertical"
                   
                    MDTopAppBar: 
                        title: "Würfler image"
                        left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]
                       
                    MDLabel: 
                        text: f"The image you just took for {player_name.text}'s score"     
                    
                    Image: 
                        source: f"current-image.png"
                        
                    Widget:    

            Screen:
                name: "scr-rules"
                BoxLayout:
                    orientation: "vertical"
                    
                    MDTopAppBar: 
                        title: "Würfler rules"
                        left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]
                    AnchorLayout:
                        anchor_y: "top"
                        padding: dp(8)
                
                        MDLabel: 
                            halign: "left"
                            valign: "top"
                            size_hint_y: None
                            text: labels.rules
                    Widget:
                    
        MDNavigationDrawer:
            id: nav_drawer
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
                    source: "die.png"

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
                            nav_drawer.set_state("close")
                            screen_manager.current = "scr-start"

                        text: "Start scoring"
                        IconLeftWidget:
                            icon: "electron-framework"

                    OneLineAvatarListItem:
                        on_press:
                            nav_drawer.set_state("close")
                            screen_manager.current = "scr-rules"
                        text: "Rules"
                        IconLeftWidget:
                            icon: 'information'

            Widget:
"""


class CameraClick(AnchorLayout):
    def capture(self):
        """
        Function to capture the images and give them the names
        according to their captured time and date.
        """
        camera = self.ids['camera']
        camera.export_to_png(f"current-image.png")
        print("Captured")


class MyToggleButton(MDRoundFlatButton, MDToggleButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.background_down = self.theme_cls.primary_color


class WaitScreen(Screen):
    image_saved = BooleanProperty(False)

    def __int__(self, **kwargs):
        super(WaitScreen, self).__init__(**kwargs)

    def on_image_saved(self, instance, value):
        if self.image_saved:
            Clock.schedule_once(self.change_screen)

    def change_screen(self, *args):
        self.parent.current = "scr-show-image"  # should work now

    def on_enter(self, *args):
        thread = threading.Thread(target=self.check_file)
        thread.daemon = True
        thread.start()

    def check_file(self):
        while not self.image_saved:
            time.sleep(0.1)
            self.image_saved = os.path.exists("current-image.png")


class Main(MDApp):

    def build(self):
        return Builder.load_string(kv)


if __name__ == "__main__":
    Main().run()
