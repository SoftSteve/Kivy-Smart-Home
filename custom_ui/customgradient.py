from kivy.graphics.texture import Texture
import numpy as np
from kivy.graphics import RoundedRectangle, Color, Line


from kivy.graphics.texture import Texture
import numpy as np
from kivy.graphics import RoundedRectangle, Color, Line

'''***AI CREATED THIS***'''

class CustomGradient:
    def __init__(self, *colors, width=255, height=255, radius=0, border=False,
                 border_color=(0, 0, 0, 0), border_width=1, direction="horizontal"):
        self.colors = colors
        self.width = width
        self.height = height
        self.radius = radius  # Can be a number or a 4-element list/tuple: (tl, tr, br, bl)
        self.border = border
        self.border_color = border_color
        self.border_width = border_width
        self.direction = direction  # "horizontal" or "vertical"
        self.texture = self._create_gradient_texture()

    def _create_gradient_texture(self):
        num_colors = len(self.colors)
        # Create an empty RGBA array for the gradient.
        data = np.zeros((self.height, self.width, 4), dtype=np.uint8)

        if self.direction == "horizontal":
            # Create horizontal gradient.
            for i in range(self.width):
                t = i / (self.width - 1)
                index = int(t * (num_colors - 1))
                next_index = min(index + 1, num_colors - 1)
                ratio = (t * (num_colors - 1)) - index

                r = int(255 * ((1 - ratio) * self.colors[index][0] + ratio * self.colors[next_index][0]))
                g = int(255 * ((1 - ratio) * self.colors[index][1] + ratio * self.colors[next_index][1]))
                b = int(255 * ((1 - ratio) * self.colors[index][2] + ratio * self.colors[next_index][2]))
                a = int(255 * ((1 - ratio) * self.colors[index][3] + ratio * self.colors[next_index][3]))
                data[:, i] = [r, g, b, a]  # Fill the entire column.
        elif self.direction == "vertical":
            # Create vertical gradient.
            for j in range(self.height):
                t = j / (self.height - 1)
                index = int(t * (num_colors - 1))
                next_index = min(index + 1, num_colors - 1)
                ratio = (t * (num_colors - 1)) - index

                r = int(255 * ((1 - ratio) * self.colors[index][0] + ratio * self.colors[next_index][0]))
                g = int(255 * ((1 - ratio) * self.colors[index][1] + ratio * self.colors[next_index][1]))
                b = int(255 * ((1 - ratio) * self.colors[index][2] + ratio * self.colors[next_index][2]))
                a = int(255 * ((1 - ratio) * self.colors[index][3] + ratio * self.colors[next_index][3]))
                data[j, :] = [r, g, b, a]  # Fill the entire row.

        texture = Texture.create(size=(self.width, self.height), colorfmt='rgba')
        texture.blit_buffer(data.tobytes(), colorfmt='rgba', bufferfmt='ubyte')
        return texture

    def _get_kivy_radius(self):
        """
        For RoundedRectangle texture fill:
        - If a 4-value radius is provided, convert it into a list of (rx, ry) pairs for each corner.
        - Otherwise, return a single-value list.
        """
        if isinstance(self.radius, (list, tuple)):
            if len(self.radius) == 4:
                return [(self.radius[0], self.radius[0]),
                        (self.radius[1], self.radius[1]),
                        (self.radius[2], self.radius[2]),
                        (self.radius[3], self.radius[3])]
            elif len(self.radius) >= 1:
                return [self.radius[0]]
        return [self.radius]

    def _get_kivy_border_radius(self):
        """
        For the border drawing via Line, return a flat list.
        """
        if isinstance(self.radius, (list, tuple)):
            if len(self.radius) == 4:
                return list(self.radius)
            elif len(self.radius) >= 1:
                return [self.radius[0]]
        return [self.radius]

    def apply_to_widget(self, widget):
        with widget.canvas.before:
            Color(1, 1, 1, 1)
            widget.rect = RoundedRectangle(texture=self.texture,
                                           size=widget.size,
                                           pos=widget.pos,
                                           radius=self._get_kivy_radius())
            if self.border:
                Color(*self.border_color)
                widget.border_rect = Line(rounded_rectangle=[*widget.pos,
                                                             *widget.size,
                                                             *self._get_kivy_border_radius()],
                                          width=self.border_width)

        widget.bind(pos=self._update_shapes, size=self._update_shapes)
        self._update_shapes(widget)

    def _update_shapes(self, widget, *args):
        if hasattr(widget, "update_content_position"):
            widget.update_content_position()
        widget.rect.size = widget.size
        widget.rect.pos = widget.pos
        if hasattr(widget, "update_content_position"):
            widget.update_content_position()
        if self.border:
            widget.border_rect.rounded_rectangle = [*widget.pos,
                                                     *widget.size,
                                                     *self._get_kivy_border_radius()]
            widget.border_rect.width = self.border_width

    @staticmethod
    def enable_gradient(widget, *colors, radius=0, border=False,
                        border_color=(0, 0, 0, 0), border_width=1, direction="horizontal"):
        gradient = CustomGradient(*colors, radius=radius, border=border,
                                  border_color=border_color, border_width=border_width,
                                  direction=direction)

        def update_rect(*args):
            if hasattr(widget, "update_content_position"):
                widget.update_content_position()
            widget.rect.size = widget.size
            widget.rect.pos = widget.pos
            if hasattr(widget, "update_content_position"):
                widget.update_content_position()
            if gradient.border:
                widget.border_rect.rounded_rectangle = [*widget.pos,
                                                         *widget.size,
                                                         *gradient._get_kivy_border_radius()]
                widget.border_rect.width = border_width

        with widget.canvas.before:
            Color(1, 1, 1, 1)
            widget.rect = RoundedRectangle(texture=gradient.texture,
                                           size=widget.size,
                                           pos=widget.pos,
                                           radius=gradient._get_kivy_radius())
            if border:
                Color(*border_color)
                widget.border_rect = Line(rounded_rectangle=[*widget.pos,
                                                             *widget.size,
                                                             *gradient._get_kivy_border_radius()],
                                          width=border_width)

        widget.bind(pos=update_rect, size=update_rect)

    