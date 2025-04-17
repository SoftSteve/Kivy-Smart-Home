from kivy.lang import Builder
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.properties import (
    BooleanProperty,
    ColorProperty,
    ListProperty,
    StringProperty,
)
from kivy.uix.behaviors import ToggleButtonBehavior

from kivymd.uix.behaviors import CircularRippleBehavior, ScaleBehavior
from kivymd.uix.behaviors.state_layer_behavior import StateLayerBehavior
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.label import MDIcon  # Only import what's needed

# Assuming you already have the .kv file loaded properly
Builder.load_file("custom_ui/customswitch.kv")


class SwitchThumbIcon(MDIcon):
    '''Implement icon to thumb'''


class SwitchThumb(MDFloatLayout):
    def _set_ellipse(self, instance, value):
        self.ellipse.size = (self._ripple_rad, self._ripple_rad)
        if self.ellipse.size[0] > self.width * 1.5 and not self._fading_out:
            self.fade_out()
        self.ellipse.pos = (
            self.center_x - self._ripple_rad / 2.0,
            self.center_y - self._ripple_rad / 2.0,
        )
        self.stencil.pos = (
            self.center_x - (self.width * self.ripple_scale) / 2,
            self.center_y - (self.height * self.ripple_scale) / 2,
        )


class CustomSwitch(StateLayerBehavior, MDFloatLayout):
    md_bg_color_disabled = ColorProperty(None)
    ripple_effect = BooleanProperty(True)
    active = BooleanProperty(False)
    icon_active = StringProperty('')
    icon_inactive = StringProperty('')
    icon_active_color = ColorProperty(None)
    icon_inactive_color = ColorProperty(None)
    thumb_color_active = ColorProperty(None)
    thumb_color_inactive = ColorProperty(None)
    thumb_color_disabled = ColorProperty(None)
    track_color_active = ColorProperty(None)
    track_color_inactive = ColorProperty(None)
    track_color_disabled = ColorProperty(None)
    line_color_disabled = ColorProperty(None)
    _thumb_pos = ListProperty([0, 0])
    _line_color = ColorProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(icon_active=self.set_icon, icon_inactive=self.set_icon)
        Clock.schedule_once(lambda x: self.on_active(self, self.active))
    
    def set_icon(self, instance_switch, icon_value: str) -> None:
        def set_icon(*args):
            icon = icon_value if icon_value else "blank"
            self.ids.thumb.ids.icon.icon = icon

        Clock.schedule_once(set_icon, 0.1)
    
    def on_line_color(self, instance, value) -> None:
        if not self.disabled:
            self._line_color = value

    def on_active(self, instance_switch, active_value: bool) -> None:
        size = (
            ((dp(16), dp(16)) if not self.icon_inactive else (dp(24), dp(24)))
            if not active_value
            else (dp(24), dp(24))
        )
        icon = "blank"

        if self.icon_active and active_value:
            icon = self.icon_active
        elif self.icon_inactive and not active_value:
            icon = self.icon_inactive
    
        Animation(size=size, t="out_quad", d=0.3).start(self.ids.thumb)
        self.set_icon(self, icon)
        self._update_thumb_pos()

    def on_thumb_down(self) -> None:
        if self.active:
            size = (dp(28), dp(28))
        else:
            size = (dp(24), dp(24))

        Animation(size=size, t="out_quad", d=0.3).start(self.ids.thumb)

    def _update_thumb_pos(self, *args, animation=True):
        if self.active:
            _thumb_pos = (
                self.width - dp(46 if self.icon_inactive else 40),
                self.height / 2 - dp(16),
            )
        else:
            _thumb_pos = (
                0 if not self.icon_inactive else dp(-14),
                self.height / 2 - dp(16),
            )
        Animation.cancel_all(self, "_thumb_pos")

        if animation:
            Animation(_thumb_pos=_thumb_pos, duration=0.3, t="out_quad").start(
                self
            )
        else:
            self._thumb_pos = _thumb_pos
