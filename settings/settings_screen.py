from kivy.uix.floatlayout import FloatLayout 
from .settings_panel import SettingsControlPanel

class SettingScreen(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.control_panel = SettingsControlPanel(
            size_hint=(.75, 1),
            pos_hint = {'x': 0.225, 'y': 0.025}
        )
        self.add_widget(self.control_panel) 

