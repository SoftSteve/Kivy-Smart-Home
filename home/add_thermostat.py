from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton, MDButton, MDButtonText

class AddThermostatScreen(FloatLayout):
    content_id = StringProperty('Initial')
    current_content = BooleanProperty(True)

    def __init__(self, callback, **kwargs):
        super().__init__(**kwargs)

        self.size_hint = (1,1)
        self.pos_hint = {'center_x':.5, 'center_y':.5}
        self.callback = callback

        self.add_device_lbl = MDLabel(
            text = 'Add Thermostat',
            theme_text_color = 'Custom',
            text_color = (0.9, 0.9, 0.9, .8),
            size_hint = (1,1),
            font_size = self.width * 0.05,
            pos_hint = {'center_x':.5, 'center_y': .55},
            halign = 'center'
        )
        self.add_widget(self.add_device_lbl)
        self.bind(size=self.update_label)

        self.plus_icon = MDIconButton(
            icon = 'home-plus', 
            style = 'outlined',
            theme_icon_color = 'Custom',
            icon_color = (0.9, 0.9, 0.9, .8),
            width = self.width * 0.15, 
            height = self.height * 0.15,
            font_size = self.width * 0.1,
            pos_hint = {'center_x':.5, 'center_y':.4},
            on_press = self.callback
        )
        self.add_widget(self.plus_icon)
    
    def update_label(self, *args):
        self.add_device_lbl.font_size = self.width * 0.06
        self.plus_icon.width = self.width * 0.13
        self.plus_icon.height = self.width * 0.13
        self.plus_icon.font_size = self.width * 0.08
        self.plus_icon.halign = 'center'