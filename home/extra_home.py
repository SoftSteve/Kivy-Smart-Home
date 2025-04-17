from kivy.uix.floatlayout import FloatLayout

from kivymd.uix.button import MDIconButton, MDButton, MDButtonText, MDFabButton
from kivymd.uix.label import MDLabel



class ExtraHome(FloatLayout):
    def __init__(self, volume_callback, bt_callback, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (.9,.9)
        self.pos_hint = {'center_x':.5, 'center_y':.5}
        self.volume_callback = volume_callback
        self.bt_callback = bt_callback

        self.volume_btn = MDFabButton(
            icon = 'volume-high',
            style='small',
            theme_icon_color = 'Custom',
            icon_color = (0.85, 0.85, 0.85, 1),
            theme_bg_color = 'Custom',
            md_bg_color = (0.25,0.25,0.35,1),
            size_hint = (None, None),
            width = self.width * 0.2,
            height = self.height * 0.2,
            font_size = self.width * 0.075,
            pos_hint = {'center_x':.5, 'center_y':.7},
            on_press = self.volume_callback
        )
        self.bluetooth_btn = MDFabButton(
            icon = 'bluetooth',
            theme_icon_color = 'Custom',
            style = 'small',
            icon_color = (0.85, 0.85, 0.85, 1),
            theme_bg_color = 'Custom',
            md_bg_color = (0.25,0.25,0.35,1),
            size_hint = (None, None),
            width = self.width * 0.2,
            height = self.height * 0.2,
            font_size = self.width * 0.075,
            pos_hint = {'center_x':.5, 'center_y':.2},
            on_press = self.bt_callback
        )
        self.add_widget(self.volume_btn)
        self.add_widget(self.bluetooth_btn)

        self.volume_lbl = MDLabel(
            text = 'Volume',
            font_size = self.width * 0.02,
            theme_text_color = 'Custom',
            text_color = (.85, .85, .85, 1),
            size_hint_x = 1,
            halign = 'center',
            pos_hint = {'center_x':.5, 'center_y':.925}
        )
        self.bluetooth_lbl = MDLabel(
            text = 'Bluetooth',
            font_size = self.width * 0.02,
            theme_text_color = 'Custom',
            text_color = (.85, .85, .85, 1),
            size_hint_x = 1,
            halign = 'center',
            pos_hint = {'center_x':.5, 'center_y':.425}
        )
        self.add_widget(self.volume_lbl)
        self.add_widget(self.bluetooth_lbl)

        self.bind(size=self.update_sizes)

    def update_sizes(self, *args):
        for lbl in [self.bluetooth_lbl, self.volume_lbl]:
            lbl.font_size = self.width * 0.15