from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Ellipse, Color
import math

class FiveCircleShape(FloatLayout):
    """
    A widget that creates a shape using 5 circles arranged in a pentagon formation.

    Parameters:
    - circle_size (tuple): Width and height of each circle.
    - colors (list of tuples): List of 5 color tuples for each circle.
    - radius (int): Radius of the circular arrangement.
    """
    def __init__(self, circle_size=(50, 50), colors=None, radius=100, **kwargs):
        super().__init__(**kwargs)

        if colors is None:
            colors = [(1, 0, 0, 1)] * 5  # Default: All circles red

        self.circle_size = circle_size
        self.radius = radius

        with self.canvas.before:
            self.circles = []
            for i in range(5):
                Color(*colors[i])
                circle = Ellipse(size=circle_size)
                self.circles.append(circle)

        self.bind(pos=self.update_circles, size=self.update_circles)
        self.update_circles()  # Ensure it positions correctly at start

    def update_circles(self, *args):
        """Updates circle positions to always stay centered."""
        cx, cy = self.center  # Get the center of the parent layout

        for i, circle in enumerate(self.circles):
            angle = math.radians(i * (360 / 5) - 90)  # -90 so first circle is at the top
            x = cx + self.radius * math.cos(angle) - self.circle_size[0] / 2
            y = cy + self.radius * math.sin(angle) - self.circle_size[1] / 2
            circle.pos = (x, y)
