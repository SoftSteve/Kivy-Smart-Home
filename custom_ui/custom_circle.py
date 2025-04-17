from custom_ui.customgradient import CustomGradient
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Ellipse, Color
from kivy.core.window import Window
from kivy.app import App

class ColorCircle(FloatLayout):
    """
    A customizable circular gradient widget using CustomGradient.

    Parameters:
    - circle_width (int): Width of the circle.
    - circle_height (int): Height of the circle.
    - circle_color_main (tuple): The primary color of the circle in (R, G, B, A) format.
    - circle_color_fade (tuple): The secondary faded color for the gradient effect.
    - circle_radius (int): Radius for the gradient effect.

    Example Usage:
        circle = ColorCircle(circle_width=120, circle_height=120, 
                             circle_color_main=(1, 0, 0, 1), circle_color_fade=(1, 1, 1, 0.2))
    """
    def __init__(self, circle_width=100, circle_height=100, 
                 circle_color_main=(0, 1, 0, 1), circle_color_fade=(1, 1, 1, 0.2), 
                 circle_radius=75, **kwargs):
        super().__init__(**kwargs)

        self.gradient = CustomGradient(circle_color_main, circle_color_fade, radius=circle_radius)

        with self.canvas.before:
            Color(1, 1, 1, 1)  
            self.circle = Ellipse(texture=self.gradient.texture, size=(circle_width, circle_height), pos=self.center)

        self.bind(pos=self.update_circle, size=self.update_circle)

    def update_circle(self, *args):
        self.circle.pos = (self.center_x - self.circle.size[0] / 2, 
                           self.center_y - self.circle.size[1] / 2)