from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.behaviors import RectangularRippleBehavior
from kivymd.uix.behaviors import BackgroundColorBehavior
from kivymd.uix.floatlayout import MDFloatLayout
from custom_ui.customgradient import CustomGradient

from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.behaviors import RectangularRippleBehavior
from kivymd.uix.behaviors import BackgroundColorBehavior
from kivy.properties import BooleanProperty


#Call CustomNavContent
''' self.nav_content = CustomNavContent(
            buttons=[
                {
                    'icon': 'home',
                    'text': 'Home',
                    'icon_color': (1, 1, 1, 1),
                    'text_color': (1, 1, 1, 1),
                    'font_size': 18,
                    'ripple_effect': True,
                    'size_hint': (0.3, 0.5),
                    'pos_hint': {'center_x': 0.2, 'center_y': 0.5},
                    'callback': self.show_home
                },'''

class CustomNavBar(GridLayout):
    """
    A fully customizable navigation bar.

    Parameters:
    - nav_content (CustomNavContent): Reference to the navigation content.
    - buttons (list): List of dictionaries containing button details.
    - nav_bg_color (tuple): RGBA background color of the navbar.
    - border_color (tuple): RGBA color for the navbar border.
    - button_size_hint (tuple): Size hint for the buttons.
    - button_pos_hint (dict): Position hint for the buttons.
    - pos_hint (dict): Position hint of the navbar.
    - size_hint (tuple): Size hint of the navbar.
    """

    def __init__(self, nav_content, buttons, nav_bg_color, border_color=None,
                 button_size_hint=(.5, .5), button_pos_hint={'center_x': .5, 'center_y': .5},
                 pos_hint={'center_x': .5}, size_hint=(1, .2), **kwargs):
        super().__init__(**kwargs)
        self.pos_hint = pos_hint
        self.size_hint = size_hint
        self.rows = 1
        self.nav_content = nav_content  

        CustomGradient.enable_gradient(self, nav_bg_color, border_color or nav_bg_color)

        for button in buttons:
            nav_button = CustomNavButton(
                icon=button['icon'],
                icon_color=button.get('icon_color', (1, 1, 1, 1)),
                text=button['text'],
                text_color=button.get('text_color', (1, 1, 1, 1)),
                font_size=button.get('font_size', 14),
                ripple_effect=button.get('ripple_effect', True),
                size_hint=button.get('size_hint', button_size_hint),
                pos_hint=button.get('pos_hint', button_pos_hint),
                callback=button['callback']
            )
            self.add_widget(nav_button)


    """
    A fully customizable button for the navigation bar.

    Parameters:
    - icon (str): The icon name.
    - text (str): The button label.
    - callback (function): The function to execute on press.
    - icon_color (tuple): Icon color in RGBA.
    - text_color (tuple): Text color in RGBA.
    - font_size (int/float): Font size for the label.
    - ripple_effect (bool): Enable or disable the ripple effect.
    - size_hint (tuple): Size hint for button layout.
    - pos_hint (dict): Position hint for button layout.
    """
class CustomNavButton(MDFloatLayout, RectangularRippleBehavior, ButtonBehavior, BackgroundColorBehavior):
    def __init__(self, icon, text, callback, icon_color=(1, 1, 1, 1), text_color=(1, 1, 1, 1),
                 font_size=14, icon_size=24, size_hint=(.5, .5), 
                 pos_hint={'center_x': .5, 'center_y': .5},
                 bg_color1=(0,0,0,0), bg_color2=(0,0,0,0), border=False, border_color = (0,0,0,0),
                   **kwargs):
        super().__init__(**kwargs)
        self.callback = callback
        self.font_size = font_size
        self.icon_size = icon_size

        CustomGradient.enable_gradient(self, bg_color1, bg_color2, border=border, border_color=border_color)

        self.icon = MDIconButton(
            icon=icon,
            theme_icon_color='Custom',
            icon_color=icon_color,
            pos_hint={'center_x': .5, 'center_y': .6},
            ripple_effect=False
        )

        self.label = MDLabel(
            text=text,
            theme_text_color="Custom",
            text_color=text_color,
            halign='center',
            pos_hint={'center_x': .5, 'center_y': .25}
        )

        self.add_widget(self.icon)
        self.add_widget(self.label)

        self.icon.bind(on_release=self.on_press)

        self.bind(size=self.update_sizes)

    def on_press(self,*args):

        if self.callback:
            self.callback(self) 

    def update_sizes(self, *args):
        self.icon.font_size = self.height * 0.3 
        self.label.font_size = self.height * 0.2  


class CustomNavContent(BoxLayout):
    """
    The main container holding the content area and navigation bar.

    Parameters:
    - buttons (list): List of button dictionaries.
    - bg_color (tuple): Background color of the content area.
    - border_color (tuple): Border color for the content area.
    - pos_hint (dict): Position hint of the container.
    - size_hint (tuple): Size hint of the container.
    """

    def __init__(self, buttons, bg_color=(0.9, 0.9, 0.9, 0.2), nav_bg_color = (0.25,0.25,0.25,1), border_color=None, 
                 pos_hint={'center_x': .5, 'center_y': .5}, size_hint=(1, 1), **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.pos_hint = pos_hint
        self.size_hint = size_hint

        self.content_area = FloatLayout(size_hint=(1, .675), pos_hint={'center_x': .5})
        CustomGradient.enable_gradient(self.content_area, bg_color, border_color or bg_color)

        self.nav_bar = CustomNavBar(nav_content=self, buttons=buttons, nav_bg_color=nav_bg_color)  
        self.add_widget(self.nav_bar)
        self.add_widget(self.content_area)
        

    def update_content(self, widget):
        self.content_area.clear_widgets()
        self.content_area.add_widget(widget)