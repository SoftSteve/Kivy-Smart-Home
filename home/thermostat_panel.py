from kivy.uix.widget import Widget
from kivy.properties import BooleanProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout

from kivymd.uix.button import MDIconButton, MDFabButton
from kivymd.uix.label import MDLabel
from kivy.metrics import dp

from custom_ui.customgradient import CustomGradient
from .thermostat import ThermostatWidget
from .thermostat_on import ThermostatOnScreen
from .add_thermostat import AddThermostatScreen

class ThermostatPanel(FloatLayout):
    active_button = BooleanProperty(False)
    def __init__(self, therm_store, callback, **kwargs):
        super().__init__(**kwargs)
        self.therm_store = therm_store
        #-----------------thermostat screen from app.py----------#
        self.therm_screen_callback = callback
        #----------------home screen thermostat------------------#
        self.therm_on = ThermostatOnScreen(therm_store=self.therm_store)
        self.add_therm = AddThermostatScreen(callback=self.therm_screen_callback)

        self.update_color(
            color1=(0.43, 0.54, 0.68754, 0.2),
            color2=(.85, .85, .9, .3)
        )

        self.content = FloatLayout(size_hint=(1, 1), pos_hint={'center_x': .5, 'center_y': .5})
        self.add_widget(self.content)

        self.update_content()

    def update_content(self, *args):
        for key, values in self.therm_store.active.items():
            if values == False:
                self.content.clear_widgets()
                self.content.add_widget(self.add_therm)

            elif key == 'Thermostat On Screen' and values == True:
                self.content.clear_widgets()
                self.content.add_widget(self.therm_on)

    def update_color(self, color1, color2):
        
        self.canvas.before.clear()
        CustomGradient.enable_gradient(self, color1, color2, radius=9)
        