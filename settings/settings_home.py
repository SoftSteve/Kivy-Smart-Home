from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout

from kivymd.uix.button import MDButton, MDFabButton, MDButtonText
from kivymd.uix.label import MDLabel

from custom_ui.customgradient import CustomGradient

import platform 
import socket
import time
import os
import subprocess

class SettingsHome(FloatLayout):
    def __init__(self, bt_callback, wifi_callback, sound_callback, **kwargs):
        super().__init__(**kwargs)
        self.pos_hint = {'center_x':.5, 'center_y':.5}
        self.size_hint = (1,1)
        self.bt_callback = bt_callback
        self.wifi_callback = wifi_callback
        self.sound_callback = sound_callback

        self.button_container = GridLayout(
            cols = 1,
            padding = self.width * 0.05,
            spacing = self.width / 6,
            size_hint = (.275, .8),
            pos_hint = {'center_x':.2, 'center_y':.5}
        )
        self.add_widget(self.button_container)
    
        self.bluetooth_btn = MDFabButton(
            icon = 'bluetooth',
            size_hint = (None, None),
            width = self.width * 0.2,
            height = self.height * 0.22,
            font_size = self.width * 0.05,
            theme_bg_color = 'Custom',
            md_bg_color = (0.25, 0.25, 0.3, 1),
            theme_icon_color='Custom',
            icon_color = (0.82, 0.90, 0.99, 1),
            theme_shadow_color = 'Custom',
            shadow_color = (0.82, 0.90, 0.99, 1),
            on_press = self.bt_callback
        )
        
        self.wifi_btn = MDFabButton(
            icon = 'wifi',
            size_hint = (None, None),
            width = self.width * 0.2,
            height = self.height * 0.22,
            font_size = self.width * 0.05,
            theme_bg_color = 'Custom',
            md_bg_color = (0.25, 0.25, 0.3, 1),
            theme_icon_color='Custom',
            icon_color = (0.82, 0.90, 0.99, 1),
            theme_shadow_color = 'Custom',
            shadow_color = (0.82, 0.90, 0.99, 1),
            on_press = self.wifi_callback
        )

        self.sound_btn = MDFabButton(
            icon = 'volume-high',
            size_hint = (None, None),
            width = self.width * 0.2,
            height = self.height * 0.22,
            font_size = self.width * 0.05,
            theme_bg_color = 'Custom',
            md_bg_color = (0.25, 0.25, 0.3, 1),
            theme_icon_color='Custom',
            icon_color = (0.82, 0.90, 0.99, 1),
            theme_shadow_color = 'Custom',
            shadow_color = (0.82, 0.90, 0.99, 1),
            on_press = self.sound_callback
        )

        self.button_container.add_widget(self.wifi_btn)
        self.button_container.add_widget(self.bluetooth_btn)
        self.button_container.add_widget(self.sound_btn)

        self.title = MDLabel(
            text = 'Settings',
            theme_text_color = 'Custom',
            text_color = 'white',
            font_size = self.width * 0.1,
            size_hint_x = 1,
            size_hint_y = .2,
            halign = 'center',
            pos_hint = {'center_x':.5,'center_y':.9}
        )
        self.add_widget(self.title)


        self.description_container = BoxLayout(
            orientation = 'vertical',
            size_hint = (.6, .7), 
            pos_hint = {'center_x':.6, 'center_y':.475}
        )
        self.add_widget(self.description_container)
        CustomGradient.enable_gradient(self.description_container, (0,0,0,0), (0,0,0,0), radius=10, border=True, border_color=(0.5,0.5,0.5,1))

        self.label_container = BoxLayout(orientation = 'vertical', size_hint = (0.9, 0.8), pos_hint = {'center_x':.5})
        self.description_container.add_widget(self.label_container)

        self.wifi_lbl = MDLabel(
            text = f'Wifi:',
            theme_text_color = 'Custom',
            text_color = 'white',
            font_size = self.width * 0.03,
            size_hint_x = .8,
            size_hint_y = .2,
            halign = 'left',
            pos_hint = {'center_y':.9}
        )
        self.bluetooth_lbl = MDLabel(
            text = f'Bluetooth:',
            theme_text_color = 'Custom',
            text_color = 'white',
            font_size = self.width * 0.03,
            size_hint_x = .8,
            size_hint_y = .2,
            halign = 'left',
            pos_hint = {'center_y':.9}
        )
        self.sound_lbl = MDLabel(
            text = f'Volume:',
            theme_text_color = 'Custom',
            text_color = 'white',
            font_size = self.width * 0.03,
            size_hint_x = .8,
            size_hint_y = .2,
            halign = 'left',
            pos_hint = {'center_y':.9}
        )
        self.device_lbl = MDLabel(
            text = f'Device:',
            theme_text_color = 'Custom',
            text_color = 'white',
            font_size = self.width * 0.03,
            size_hint_x = .8,
            size_hint_y = .2,
            halign = 'left',
            pos_hint = {'center_y':.9}
        )
        self.timezone_lbl = MDLabel(
            text = f'Timezone:',
            theme_text_color = 'Custom',
            text_color = 'white',
            font_size = self.width * 0.03,
            size_hint_x = .8,
            size_hint_y = .2,
            halign = 'left',
            pos_hint = {'center_y':.9}
        )

        
        self.label_container.add_widget(self.device_lbl)
        self.label_container.add_widget(self.wifi_lbl)
        self.label_container.add_widget(self.bluetooth_lbl)
        self.label_container.add_widget(self.sound_lbl)
        self.label_container.add_widget(self.timezone_lbl)

        self.bind(size=self.update_sizes)
        self.get_descrip_placeholders()

    def update_sizes(self, *args):
        self.button_container.spacing = self.width * 0.05
        self.button_container.padding = self.width * 0.05

        for button in [self.bluetooth_btn, self.wifi_btn, self.sound_btn]:
            button.width = self.width * 0.125
            button.height = self.height * 0.185
            button.font_size = self.width * 0.05

        self.title.font_size = self.width * 0.05
        
        for lbl in [self.wifi_lbl, self.sound_lbl, self.device_lbl, self.bluetooth_lbl, self.timezone_lbl]:
            lbl.font_size = self.width * 0.025
            lbl.theme_font_name = 'Custom'
            lbl.font_name = 'fonts/ttf/Roboto-Light.ttf'

    def get_descrip_placeholders(self, *args):
        device_name = socket.gethostname()
        self.device_lbl.text = f'Device: {device_name}'

        timezone = time.tzname
        self.timezone_lbl.text = f'Timezone: {timezone}'

        wifi_name = self.get_wifi_name()
        self.wifi_lbl.text = f'Wifi: {wifi_name}'

        bluetooth_name = 'None'
        self.bluetooth_lbl.text = f'Bluetooth: {bluetooth_name}'

        volume = 100
        self.sound_lbl.text = f'Volume: {volume}'
        

    def get_wifi_name(self, *args):
        try:
            output = subprocess.check_output("netsh wlan show interfaces", shell=True, text=True)
            for line in output.split("\n"):
                if "SSID" in line and "BSSID" not in line:
                    return line.split(":")[1].strip()
        except Exception as e:
            return f"Error: {e}"

    