import sys
import subprocess
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.button import MDFabButton

from custom_ui.customgradient import CustomGradient  # Ensure this module exists


class AppPanel(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pos_hint = {'center_x':.5, 'center_y':.5}
        self.text_color = (1,1,1,1)

        self.main_container = FloatLayout(size_hint=(1,1))
        self.add_widget(self.main_container)

        self.update_color(
        color1 = (0.43, 0.54, 0.68754, 0.2),
        color2 = (.85, .85, .9, .3)
        )

        self.youtube = MDFabButton(
            icon = 'youtube',
            style = 'small',
            theme_icon_color = 'Custom',
            icon_color = 'red',
            pos_hint={'center_x':.2, 'center_y':.5},
            on_release=self.launch_youtube
        )

        self.spotify = MDFabButton(
            icon = 'spotify',
            style='small',
            theme_bg_color = 'Custom',
            md_bg_color = 'black',
            theme_icon_color = 'Custom',
            icon_color = 'green',
            pos_hint={'center_x':.5, 'center_y':.5},
            on_release=self.launch_spotify
        )

        self.pandora = MDFabButton(
            icon='pandora',
            style='small',
            theme_icon_color = 'Custom',
            icon_color = 'blue',
            pos_hint={'center_x':.8, 'center_y':.5},
            on_release=self.launch_pandora
        )

        self.main_container.add_widget(self.youtube)
        self.main_container.add_widget(self.spotify)
        self.main_container.add_widget(self.pandora)

    def launch_spotify(self, *args):
        self.spotify_process = subprocess.Popen(["spotify"])

    def launch_youtube(self, *args):
        if sys.platform == "win32":
            subprocess.run(["start", "https://www.youtube.com"], shell=True)
        else: 
            subprocess.run(["xdg-open", "https://www.youtube.com"])

    def launch_pandora(self, *args):
        if sys.platform == "win32":
            subprocess.run(["start", "https://www.pandora.com"], shell=True)
        else: 
            subprocess.run(["xdg-open", "https://www.pandora.com"])

    def update_content_position(self, *args):
        self.main_container.size = (self.width, self.height)
        self.main_container.pos = self.pos
    
    def update_color(self, color1, color2):
        self.canvas.before.clear()
        CustomGradient.enable_gradient(self, color1, color2, radius=9)
