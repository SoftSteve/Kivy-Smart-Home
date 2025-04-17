from kivy.uix.floatlayout import FloatLayout
from .thermostat_panel import ThermostatControlPanel

class ThermostatScreen(FloatLayout):
    def __init__(self, therm_store, **kwargs):
        super().__init__(**kwargs)
        self.therm_store = therm_store

        self.control_panel = ThermostatControlPanel(
            size_hint = (.75, 1),
            pos_hint={'x': 0.225, 'y': 0.025},
            therm_store=self.therm_store
        )
        self.add_widget(self.control_panel)

