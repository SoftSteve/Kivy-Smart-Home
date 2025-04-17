from kivy.uix.textinput import TextInput
from kivy.animation import Animation
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle
from custom_ui.customgradient import CustomGradient


"""
    A customizable text input field with an icon.

    Parameters:
    - text_input_icon (str): The name of the icon. (e.g., 'magnify', 'home')
    - text_input_icon_color (tuple): The RGBA color of the icon. (e.g., (1, 0, 0, 1) for red)
    - text_input_font_size (int/float): The font size of the text input. (e.g., 20)
    - text_input_hint_text (str): Placeholder text for the text input. (e.g., "Search...")
    - text_color (tuple, optional): The RGBA color of the text in the input field. Default is (.25, .25, .25, 1).
    - background_start (tuple, optional): RGBA color for the start of the gradient background. Default is (1, 1, 1, .2).
    - background_end (tuple, optional): RGBA color for the end of the gradient background. Default is (.9, .9, .9, .2).
    - gradient_radius (int, optional): Radius of the gradient corners. Default is 1.
    - border (bool, optional): Whether to enable a border around the background. Default is True.
    - border_color (tuple, optional): RGBA color of the border. Default is (0, 0, 0, 1).
    - pos_hint (dict, optional): Position hint for the widget. Default is {'center_x': .5, 'center_y': .5}.
    - size_hint (tuple, optional): Size hint for the widget. Default is (0.8, None) for horizontal orientation.
"""

class CustomTextInput(MDBoxLayout):
    def __init__(
            self, 
            *args, 
            text_input_icon, 
            text_input_icon_color, 
            text_input_font_size  = 18,
            text_input_hint_text,
            text_color = [.25, .25, .25, 1], 
            background_start=(1,1,1,.2), 
            background_end=(.9,.9,.9, .2), 
            gradient_radius=1, 
            border=True, 
            border_color=(0,0,0,1),
            pos_hint={'center_x': .5, 'center_y': .5},
            size_hint = (0.8, None),
            **kwargs):
        super().__init__(*args, **kwargs)
        self.orientation = 'horizontal'
        self.size_hint = size_hint
        self.pos_hint = pos_hint

        CustomGradient.enable_gradient(
            self, 
            background_start, 
            background_end, 
            radius=gradient_radius, 
            border=border, 
            border_color=border_color
        )

        self.text_search = TextInput(
            text='',
            size_hint=(1, None), 
            pos_hint={'center_x': 0.5},
            multiline=False,
            font_size=f'{text_input_font_size}sp',
            background_color=[0,0,0,0],
            foreground_color=text_color,
            hint_text=text_input_hint_text,
            cursor_color=(0, 0, 0, 1),
            font_name = 'fonts/ttf/Roboto-Regular.ttf'
        )
        self.text_search.bind(font_size=self.update_height)

        self.icon = MDIconButton(
            icon=text_input_icon,
            theme_bg_color='Custom',
            md_bg_color=(0, 0, 0, 0),
            theme_icon_color='Custom',
            icon_color=text_input_icon_color,
            halign='right',
            size_hint=(None, None),
            ripple_effect = False,
            on_press = self.animate_press
        )
        self.icon.on_enter = lambda *args: None
        self.icon.on_leave = lambda *args: None


        self.add_widget(self.icon)
        self.add_widget(self.text_search)

        self.update_height()

    def update_height(self, *args):
        padding = 20

        if self.text_search.font_size <= 15:
            padding = 15
        else: 
            padding = 20

        self.text_search.height = self.text_search.font_size + padding
        self.height = self.text_search.height

        self.icon_size = self.text_search.font_size + padding
        self.icon.size = (self.icon_size, self.icon_size)
        self.icon_small = self.text_search.font_size * .5 + padding
    
    def animate_press(self,instance, *args):
        anim_small = Animation(font_size = self.icon_small, duration=.1)
        anim_small.start(self.icon)

    def limit_text(self, instance, value):
        if len(value) > 25:
            instance.text = value[:25]