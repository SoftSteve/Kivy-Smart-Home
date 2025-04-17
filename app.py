# STILL IN DEVELOPMENT STAGES

from kivy.config import Config
Config.set('kivy', 'keyboard_mode', 'none')
Config.set('graphics', 'dpi', '100')

'''import RPi.GPIO as GPIO'''

# Kivy and KivyMD imports
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.config import Config
from kivy.core.image import Image as CoreImage
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.properties import BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivymd.app import MDApp
from kivymd.uix.button import MDButton, MDButtonText, MDFabButton
from kivymd.uix.divider import MDDivider
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDButtonIcon
import logging
from kivy.logger import Logger

logging.getLogger('kivy').setLevel(logging.WARNING)

# Standard library imports
import logging
import os
import threading
import time
from datetime import datetime

# Project Imports
from home.home_screen import HomeScreen
from lights.lights_control_screen import LightsControlScreen
from blinds.blinds_control_screen import BlindsControlScreen
from fans.fans_control_screen import FanControlScreen
from thermostat.thermostat_screen import ThermostatScreen
from settings.settings_screen import SettingScreen

from lights.light_state_store import ButtonStateStore
from blinds.blinds_state_store import BlindsStateStore
from fans.fans_state_store import FansStateStore
from home.lock_store import LockStore
from home.thermostat_state import ThermostatStore
from home.weather_store import WeatherStore

from custom_ui.customgradient import CustomGradient


screen_height = Window.height
screen_width = Window.width
Window.always_on_top = True
Window.size = (700, 375)
Window.display = 1


class MainScreen(MDScreen):
    
    is_dark_theme = BooleanProperty(True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.light_store = ButtonStateStore()

        self.lights_control_screen = LightsControlScreen(store=self.light_store)

        self.blind_store = BlindsStateStore()

        self.blinds_screen = BlindsControlScreen(store=self.blind_store)

        self.fan_store = FansStateStore()

        self.fan_screen = FanControlScreen(store=self.fan_store)

        self.lock_store = LockStore()

        self.therm_store = ThermostatStore()
        
        self.weather_store = WeatherStore()



        self.home_screen = HomeScreen(
            lock_store=self.lock_store, 
            therm_store=self.therm_store, 
            store=self.light_store, 
            weather_store=self.weather_store, 
            callback=self.show_thermostat_content
        )
        
        Window.bind(on_resize=self.on_window_resize)

        self.button_frames = []

        self.build_layout()
        
        self.show_home_content(self.home_screen)
        

    def on_window_resize(self, instance, width, height):
        self.screen_width = width
        self.screen_height = height

    def build_layout(self):
        self.root_layout = FloatLayout()
    
        self.bg_texture = CoreImage('images/background_black.jpg').texture

        with self.canvas.before:
            self.rect = Rectangle(size=self.size, pos=self.pos, texture=self.bg_texture)

        self.bind(size=self.update_bg_image, pos=self.update_bg_image)

        button_directory = {
            'LIGHT': self.show_lights_content,
            'FAN': self.show_fan_content,
            'BLIND': self.show_blinds_content,
            'THERMOSTAT': self.show_thermostat_content,
        }

        self.navigation_container = FloatLayout(
            size_hint = (.2, .95),
            pos_hint = {'x': 0.015, 'y': .0235}
        )
        self.root_layout.add_widget(self.navigation_container)

        self.nav_gradient = CustomGradient.enable_gradient(self.navigation_container, (0.4, 0.45, 0.55, 0.4),(0.2, 0.22, 0.27, 0.3), radius=9, direction='vertical')

        self.button_container = BoxLayout(orientation = 'vertical', size_hint = (1,1), pos_hint = {'x': 0, 'y': 0.38})

        self.is_pressed = None

        self.buttons = []

        self.names = ['Lights','Fans', 'Blinds', 'Thermostat']

        for button_name, callback in zip(self.names, button_directory.values()):
            self.button_colors = []
            self.button = MDButton(
                MDButtonText(
                    text=button_name, 
                    pos_hint = {'center_x': .5, 'center_y': .5}, 
                    theme_text_color='Custom',
                    text_color=(.85, .85, .85, 1) if self.is_dark_theme else (1,1,1,1),
                    font_size = 20,
                    bold=False,
                ),
                style='tonal',
                on_release=callback,
                size_hint = (1, None),
                height = self.height * 0.1,
                theme_shadow_color = 'Custom',
                shadow_color = (1,1,1,0),
                theme_width = 'Custom',
                theme_bg_color = 'Custom',
                md_bg_color = (0,0,0,0),
                size_hint_x = 1,
                radius = [1,1,1,1],
                on_press=self.button_pressed,
                ripple_color = (1,1,1.6),
            )
            self.button_container.add_widget(self.button)
            self.buttons.append(self.button)
        self.navigation_container.add_widget(self.button_container)
        
        self.clock_container = BoxLayout(orientation='vertical', size_hint = (1, .175), pos_hint = {'x': .25, 'y': 0.81})

        self.clock_label = Label(
            text = "00:00:00",
            font_size = self.width * 0.2,
            font_name = 'fonts/ttf/Roboto-Regular.ttf',
            color = (.85, .85, .85, 1)
        )

        self.date_label = Label(
            text = 'date, here day',
            font_size = self.width * 0.01,
            font_name = 'fonts/ttf/Roboto-light.ttf',
            color = (1,1,1,.7)
        )
        self.clock_container.add_widget(self.clock_label)
        self.clock_container.add_widget(self.date_label)
        Clock.schedule_interval(self.update_clock, 1)

        self.navigation_container.add_widget(self.clock_container)

        self.divider = MDDivider(size_hint_x = 1, pos_hint = {'x':0, 'y': .8})
        self.navigation_container.add_widget(self.divider)

        self.home_button = MDFabButton(
            theme_bg_color = 'Custom',
            md_bg_color = (0.25, 0.25, 0.35, 1),
            icon = 'home', 
            theme_icon_color='Custom',
            icon_color = (0.85, 0.85, 0.85, 1), 
            style = 'standard',
            pos_hint = {'x': 0.08, 'y': 0.825}, 
            on_release=self.show_home_content
        )
        self.navigation_container.add_widget(self.home_button)

        self.settings_button = MDFabButton(
            theme_bg_color = 'Custom',
            md_bg_color = (0.25, 0.25, 0.35, 1),
            icon = 'cog-outline',
            theme_icon_color='Custom',
            icon_color = (0.85, 0.85, 0.85, 1), 
            style='small',
            pos_hint={'x': 0.15, 'y': 0.02},
            on_release=self.show_settings_content,
        )
        self.navigation_container.add_widget(self.settings_button)

        self.theme_toggle_button = MDFabButton(
            theme_bg_color = 'Custom',
            md_bg_color = (0.25, 0.25, 0.35, 1),
            icon = 'theme-light-dark',
            theme_icon_color='Custom',
            icon_color = (0.85, 0.85, 0.85, 1),
            style='small',
            pos_hint={'x': 0.55, 'y': 0.02},
            on_release=self.theme_change,
        )
        self.navigation_container.add_widget(self.theme_toggle_button)
        
        self.bind(is_dark_theme=self.on_theme_change)

       
        self.content_area = FloatLayout(
            size_hint=(1, .95),  
            pos_hint={'x': 0.3, 'y': 0},  
        )
        self.root_layout.add_widget(self.content_area)

        
        self.add_widget(self.root_layout)
        
        self.panels = {
            'active_panel':self.home_screen.home_screen_panel.active_panel,
            'weather_panel':self.home_screen.home_screen_panel.weather_panel,
            'lock_panel':self.home_screen.home_screen_panel.door_lock_panel,
            'app_panel':self.home_screen.home_screen_panel.apps_panel,
            'thermostat_panel':self.home_screen.home_screen_panel.thermostat_panel,
            'extra_panel': self.home_screen.home_screen_panel.extra_options
        }

        self.bind(size=self.update_nav_sizes)

    def button_pressed(self, instance):
        pass

    def update_panel_colors(self, panel_key, color1, color2):
        if panel_key in self.panels:
            self.panels[panel_key].update_color(color1, color2)

    def theme_change(self, *args):
        self.is_dark_theme = not self.is_dark_theme

    def on_theme_change(self, instance, value):

        left_panel = ['app_panel', 'thermostat_panel', 'lock_panel']

        for button in self.button_container.children:
            if isinstance(button, MDButton):
                button.children[0].text_color = (0.85, 0.85, 0.85, 1) if self.is_dark_theme else (1, 1, 1, 1)

        for button in self.navigation_container.children:
            if isinstance(button, MDFabButton):
                button.shadow_color = (0,0,0,0) if self.is_dark_theme else (0.2, 0.25, 0.45, 1)
                button.md_bg_color = (0.25, 0.25, 0.35, 1) if self.is_dark_theme else (0.4, 0.45, 0.55, 1)
                button.icon_color = (0.85, 0.85, 0.85, 1) if self.is_dark_theme else (0.82, 0.90, 0.99, 1)

        if self.is_dark_theme:
            self.bg_texture = CoreImage('images/background_black.jpg').texture
        
            for name, value in self.panels.items():
                if name != 'app_panel':
                    self.label_color(value, color=(0.85, 0.85, 0.85, 1))
            
            for name in self.panels:
                if name in left_panel:
                    self.update_panel_colors(name, (0.43, 0.54, 0.68754, 0.2),(.85, .85, .9, .3))
                elif name == 'extra_panel':
                    self.update_panel_colors(name, (.85, .85, .9, .3), (.85, .85, .9, .3))
                else:
                    self.update_panel_colors(name, (.85, .85, .9, .3),(0.43, 0.54, 0.68754, 0.2))

        else:
            self.bg_texture = CoreImage('images/background_image_light.jpg').texture
            
            for name in self.panels:
                if name in left_panel:
                    self.update_panel_colors(name, (0.4, 0.45, 0.55, 0.4),(0.2, 0.22, 0.27, 0.3))
                elif name == 'extra_panel':
                    self.update_panel_colors(name, (0.2, 0.22, 0.27, 0.3), (0.2, 0.22, 0.27, 0.3))
                else:
                    self.update_panel_colors(name, (0.2, 0.22, 0.27, 0.3),(0.4, 0.45, 0.55, 0.4))
            
            for name, value in self.panels.items():
                if name not in ['app_panel', 'thermostat_panel']: 
                    self.label_color(value, color=(1,1,1,1))
            
            for name, value in self.panels.items():
                if name == 'thermostat_panel':
                    self.therm_buttons(value, bg_color=(0.4, 0.45, 0.55, 1), icon_color=(0.82, 0.90, 0.99, 1))

        self.rect.texture = self.bg_texture

    def label_color(self, widget, depth = 0, color = (1,1,1,1)):
        for child in reversed(widget.children):
            self.label_color(child, depth + 1, color)
            if isinstance(child, MDLabel):
                child.text_color = color

    def therm_buttons(self, widget, depth = 0, bg_color = (1,1,1,1), icon_color=(1,1,1,1)):
        for child in reversed(widget.children):
            self.therm_buttons(child, depth + 1, bg_color, icon_color)
            if isinstance(child, MDFabButton):
                child.md_bg_color = bg_color
                child.icon_color = icon_color 

    def update_clock(self, dt):
        now = datetime.now()
        date = datetime.today()
        self.clock_label.text = now.strftime("%I") + ':' + now.strftime("%M")
        self.date_label.text =  date.strftime("%B") + " " + date.strftime("%d")
    
    def update_bg_image(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def show_lights_content(self, instance):
        threading.Thread(target=self.load_lights_content).start()

    def load_lights_content(self):
        Clock.schedule_once(self.refresh_ui, 0)  

    def refresh_ui(self, dt):
        self.lights_control_screen.control_panel.Refresh_UI()
        self.update_content("", self.lights_control_screen)

    def show_fan_content(self, instance):
        self.fan_screen.control_panel.refresh_ui()
        self.update_content("", self.fan_screen)

    def show_blinds_content(self, instance):
        self.blinds_screen.control_panel.refresh_ui()
        self.update_content("", self.blinds_screen)
    
    def show_thermostat_content(self, instance):
        thermostat_screen = ThermostatScreen(therm_store=self.therm_store)
        self.update_content("", thermostat_screen)

    def show_home_content(self, instance):
        threading.Thread(target=self.load_home_content).start()

    def load_home_content(self):
        Clock.schedule_once(self.refresh_home_ui, 0)  

    def refresh_home_ui(self, dt):
        self.home_screen.home_screen_panel.active_panel.update_active_devices()
        self.home_screen.home_screen_panel.thermostat_panel.therm_on.refresh_ui()
        self.home_screen.home_screen_panel.thermostat_panel.update_content()
        self.update_content('', self.home_screen) 
    
    def show_settings_content(self, instance):
        settings_screen = SettingScreen()
        self.update_content('', settings_screen)

    def update_content(self, label_text, widget):
        self.start_time = time.time() 

        self.content_area.clear_widgets()

        widget.opacity = 0
    
        self.content_area.add_widget(widget)

        anim = Animation(opacity=1, duration=0.05, t='out_quad')
        anim.bind(on_complete=self.content_loaded)

        anim.start(widget)

    def content_loaded(self, animation, widget):
        elapsed_time = time.time() - self.start_time  
        print(f"Content loaded in {elapsed_time:.4f} seconds")

    def update_nav_sizes(self, *args):
        for buttons in self.buttons:
            buttons.height = self.height * 0.1
            buttons.font_size = self.height * 0.02

        self.clock_label.font_size = self.width * 0.035
        self.date_label.font_size = self.width * 0.02

class MyApp(MDApp):
    def build(self):
        
        return MainScreen()
    
    

if __name__ == "__main__":
    MyApp().run()

    

   

    