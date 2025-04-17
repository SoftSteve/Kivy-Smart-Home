from .home_screen_panel import HomeScreenPanel
from kivy.uix.floatlayout import FloatLayout

class HomeScreen(FloatLayout):
    def __init__(self, lock_store, therm_store, store, weather_store, callback, **kwargs):
        super().__init__(**kwargs)
        self.lock_store = lock_store
        self.therm_store = therm_store
        self.store = store
        self.weather_store = weather_store
        self.therm_screen_callback = callback

        self.home_screen_panel = HomeScreenPanel(
            size_hint=(.75, 1), 
            pos_hint={'x': 0.225, 'y': 0.025},
            lock_store=self.lock_store,
            therm_store=self.therm_store,
            store=self.store,
            callback=self.therm_screen_callback,
            weather_store=self.weather_store
            )
            
        
        self.add_widget(self.home_screen_panel)