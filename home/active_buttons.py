from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import StringProperty, BooleanProperty, NumericProperty
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDLabel

from kivymd.uix.behaviors import RectangularRippleBehavior, BackgroundColorBehavior

from custom_ui.customswitch import CustomSwitch


class DeviceListItem(MDBoxLayout, RectangularRippleBehavior, ButtonBehavior, BackgroundColorBehavior):
    text = StringProperty("Default Text")
    id = StringProperty('Default Text')
    switch_active = BooleanProperty(False)
    last_brightness = NumericProperty(0.8) 
    last_color_temperature = NumericProperty(6500) 

    def __init__(self, store, **kwargs):
        self.text = kwargs.pop("text", "Default Text")
        self.id = kwargs.pop("id", "Default Text")
        self.switch_active = kwargs.pop("state", False)
        self.last_brightness = kwargs.pop("last_brightness", 0.8)  
        self.last_color_temperature = kwargs.pop("last_color_temperature", 6500) 

        super().__init__(**kwargs)

        self.orientation = 'horizontal'
        self.size_hint = (.8, None)
        self.radius = [10, 10, 10, 10]
        self.height = 40
        self.padding = 10
        self.on_press = self.toggle_switch
        self.store = store

        with self.canvas.before:
            Color(.9, .9, 1, .2)
            self.rect = RoundedRectangle(
                pos=self.pos,
                size=(self.size[0], self.size[1]),
                radius=[10, 10, 10, 10])
        self.bind(size=self.update_rect, pos=self.update_rect)

        self.icon = MDIconButton(
            icon='lightbulb',
            theme_icon_color='Custom',
            icon_color=(0.82, 0.90, 0.99, 1),
            size_hint_x=None,
            width=50,
            pos_hint={'center_x': .5, 'center_y': .5},
            on_press=self.toggle_switch
        )

        self.label = MDLabel(
            text=self.text,
            halign='left',
            pos_hint={'center_x': .5, 'center_y': .4},
            text_color=(0.82, 0.90, 0.99, 1),
        )
        self.label.font_size = '14sp'

        self.switch = CustomSwitch(
            id=self.id,
            size_hint=(None, None),
            track_color_active=(.227, .274, .862, 1),
            pos_hint={'center_x': .5, 'center_y': .5}
        )
        self.switch.active = self.switch_active
        self.switch.height = dp(18)
        self.switch.width = dp(36)
        self.switch.bind(active=self.toggle_button_theme)

        self.add_widget(self.icon)
        self.add_widget(self.label)
        self.add_widget(self.switch)

    def format_text(self, text):
        words = text.split(" ")
        formatted_text = "\n".join(words)
        return formatted_text

    def toggle_button_theme(self, instance, value):
        self.switch_active = value
        print(f"Switch ID: {instance.id}, Active: {value}")

    def toggle_switch(self, *args):
        self.switch_active = not self.switch_active
        self.switch.active = self.switch_active

    
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = (self.size[0], self.size[1])

