from kivymd.uix.button import MDIconButton
from kivy.properties import NumericProperty
from kivy.graphics import PushMatrix, Rotate, PopMatrix

class RefreshButton(MDIconButton):
    rotate_value_angle = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.icon='refresh'
        self.style='outlined'
        self.theme_line_color='Custom'
        self.line_color=(0, 0, 0, 0)
        self.theme_icon_color='Custom'
        self.icon_color=(0.85, 0.85, 1, 1)
        self.pos_hint={'center_x': .925, 'center_y': .9}
        self.ripple_effect=False

        # Create the rotation transformation
        with self.canvas.before:
            self.rot = Rotate(angle=self.rotate_value_angle, axis=(0, 0, 1), origin=self.center)
            PushMatrix()
            self.canvas.before.add(self.rot)

        with self.canvas.after:
            PopMatrix()

        # Bind property updates
        self.bind(rotate_value_angle=self.update_rotation)
        self.bind(center=self.update_origin)  # Ensure rotation origin updates on layout changes

    def update_rotation(self, *args):
        """Update the rotation angle dynamically."""
        self.rot.angle = self.rotate_value_angle

    def update_origin(self, *args):
        """Keep the rotation origin at the center of the button."""
        self.rot.origin = self.center