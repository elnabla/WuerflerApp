
from kivymd.app import MDApp
from kivy.lang import Builder

from kivy.core.window import Window

Window.size = (450, 800)  # to see how it looks in portrait mode

kv = """
#: import labels labels
Screen:
    MDNavigationLayout:    
    
        ScreenManager:
            id: screen_manager
            camera: camera
            
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
                        
                        Camera:
                            id: camera
                            play: True
                
                        MDRoundFlatButton:
                            text: 'Capture'
                            height: '48dp'
                            on_press: 
                                camera.export_to_png("captured_image.png")
                                # has to be done after export, after button press
                                captured_image.reload() 
                                screen_manager.current = "scr-show-image" 
                                               
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
                        # image is loaded at startup of program. So useless to reload in the image class itself
                        id: captured_image
                        source: "captured_image.png"          
                        
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


class Main(MDApp):

    def build(self):
        return Builder.load_string(kv)


if __name__ == "__main__":
    Main().run()
