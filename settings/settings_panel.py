from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from threading import Thread
import asyncio

from custom_ui.customgradient import CustomGradient
from .settings_home import SettingsHome
from .popups import BluetoothPop, WifiPop, SoundPop, discover_bluetooth_devices


class SettingsControlPanel(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build()

    def build(self):
        CustomGradient.enable_gradient(self, (0.43, 0.54, 0.68754, 0.2), (.85, .85, .9, .3), radius=9)
        self.content = FloatLayout(size_hint=(1, 1), pos_hint={'center_x': .5, 'center_y': .5})
        self.add_widget(self.content)
        self.settings_home()

    def settings_home(self, *args):
        self.home = SettingsHome(wifi_callback=self.show_wifi, bt_callback=self.show_bluetooth, sound_callback=self.show_sound)
        self.update_content(self.home)

    #----------------bluetooth-------------------
    def show_bluetooth(self, *args):
        self.bt_popup = BluetoothPop(
            callback_cancel=self.cancel_bt,
            callback_accept=self.accept_bt
        )

        self.bt_popup.theme_cls.theme_style = 'Dark'

        thread = Thread(target=self.run_discovery, daemon=True)
        thread.start()

    def run_discovery(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(discover_bluetooth_devices(self.bt_popup.add_device))

    def accept_bt(self, *args):
        self.bt_popup.dismiss()
        self.bt_popup.theme_cls.theme_style = 'Light'

    def cancel_bt(self, *args):
        self.bt_popup.dismiss()
        self.bt_popup.theme_cls.theme_style = 'Light'

    #--------------------wifi--------------------
    def show_wifi(self, *args):
        self.wifi_popup = WifiPop(callback_cancel=self.cancel_wifi, callback_accept=self.accept_wifi)
        self.wifi_popup.theme_cls.theme_style = 'Dark'

    def accept_wifi(self, *args):
        self.wifi_popup.dismiss()
        self.wifi_popup.theme_cls.theme_style = 'Light'

    def cancel_wifi(self, *args):
        self.wifi_popup.dismiss()
        self.wifi_popup.theme_cls.theme_style = 'Light'

    #--------------------sound------------------------

    def show_sound(self, *args):
        self.sound_popup = SoundPop(callback_accept=self.s_accept, callback_cancel=self.s_cancel)
        self.update_content(self.sound_popup)

    def s_accept(self, *args):
        self.update_content(self.home)
    
    def s_cancel(self, *args):
        self.update_content(self.home)

    

    def update_content(self, widget):
        self.content.clear_widgets()
        self.content.add_widget(widget)

    def update_content_position(self, *args):
        self.content.pos = self.pos
        self.content.size = self.size