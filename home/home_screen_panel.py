from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty, NumericProperty
from kivy.graphics import Color, Rectangle

from .weather import WeatherPanel  # Ensure this module exists
from .app_panel import AppPanel  # Ensure this module exists
from .lock_panel import DoorLockPanel  # Ensure this module exists
from .thermostat_panel import ThermostatPanel  # Ensure this module exists
from .active_panel import ActivePanel 
from .extra_panel import Extra


class HomeScreenPanel(FloatLayout):
    def __init__(self, therm_store, lock_store, store, weather_store, callback, **kwargs):
        super().__init__(**kwargs)
        self.therm_store = therm_store
        self.store = store
        self.lock_store = lock_store
        self.weather_store = weather_store
        self.therm_screen_callback = callback

        self.weather_panel = WeatherPanel(
            size_hint_x = .425,
            weather_store=self.weather_store
        )
        
        self.apps_panel = AppPanel(size_hint_y = .6)
        
        self.door_lock_panel = DoorLockPanel(lock_store=self.lock_store, size_hint_y=.6)

        self.thermostat_panel = ThermostatPanel(therm_store=self.therm_store, callback=self.therm_screen_callback)
        
        self.active_panel = ActivePanel(store=self.store)
        
        self.extra_options = Extra(size_hint = (.2, 1))
        

        self.main_container = GridLayout(rows=2, size=self.size, pos_hint = {'center_x':.5, "center_y":.5}, spacing = 5)
        self.add_widget(self.main_container) 

        self.bind(pos=self.update_rect, size=self.update_rect)

        self.bottom_content = BoxLayout(
            orientation='horizontal', 
            size_hint = (1, .387),
            spacing = 5,
            pos_hint = {'center_x':.5, 'center_y':.1}
        )

        self.top_content= BoxLayout(
            orientation = 'horizontal',
            size_hint = (1, .6),
            spacing = 5,
            pos_hint = {'center_x':.5, 'center_y':.5}
        )
        
        self.main_container.add_widget(self.top_content)
        self.main_container.add_widget(self.bottom_content)

        self.small_btm_container = BoxLayout(
            orientation='vertical', 
            size_hint = (.4, 1), 
            spacing = 5,
            pos_hint = {'x':0, 'y': 0}
        )

        self.top_content.add_widget(self.thermostat_panel)
        self.top_content.add_widget(self.active_panel)

        self.bottom_content.add_widget(self.small_btm_container)
        self.bottom_content.add_widget(self.extra_options)
        self.bottom_content.add_widget(self.weather_panel)
        
        self.small_btm_container.add_widget(self.door_lock_panel)
        self.small_btm_container.add_widget(self.apps_panel)
        

        
    def update_rect(self, *args):

        self.update_content_position()

    def update_content_position(self, *args):
        pass

