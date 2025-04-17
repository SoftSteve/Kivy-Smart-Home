from kivy.uix.widget import Widget
from kivy.properties import BooleanProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout

from kivymd.uix.button import MDIconButton, MDFabButton
from kivymd.uix.label import MDLabel
from kivy.metrics import dp

from .thermostat_onscreen import ThermostatOnScreen
from.add_thermostat import AddThermostatScreen, InitializePopup
from custom_ui.customgradient import CustomGradient


class ThermostatControlPanel(FloatLayout):
    def __init__(self, therm_store, **kwargs):
        super().__init__(**kwargs)
        self.therm_store = therm_store

        self.add_device_screen = AddThermostatScreen(content_id='Add thermostat screen', current_content=False, callback=self.add_device)
        self.thermostat_active = ThermostatOnScreen(content_id='Thermostat On Screen', current_content=False, therm_store=self.therm_store)

     
        self.therm_active_id = self.thermostat_active.content_id
        self.add_therm_id = self.add_device_screen.content_id

        self.thermostat_active.current_content = self.therm_store.get_active_content(self.therm_active_id)
        self.add_device_screen.current_content = self.therm_store.get_active_content(self.add_therm_id)

        if not self.thermostat_active.current_content and not self.add_device_screen.current_content:
            self.add_device_screen.current_content = True 

        self.build()

    def build(self):
        self.update_color(
            color1=(0.43, 0.54, 0.68754, 0.2),
            color2=(.85, .85, .9, .3)
        )

        self.content = FloatLayout(size_hint=(1, 1), pos_hint={'center_x': .5, 'center_y': .5})
        self.add_widget(self.content)

        self.update_content()

    def add_device(self, *args):
        self.init_popup = InitializePopup(callback_cancel=self.cancel, callback_accept=self.accept)
        self.init_popup.theme_cls.theme_style = 'Dark'
        self.init_popup.theme_cls.primary_palette = 'Royalblue'

    def cancel(self, *args):
        self.init_popup.dismiss()
        self.init_popup.theme_cls.theme_style = 'Light'

    def accept(self, *args):
        self.init_popup.dismiss()

        self.thermostat_active.current_content = True
        self.add_device_screen.current_content = False

        self.therm_store.update_active_content(self.therm_active_id, self.thermostat_active.current_content)
        self.therm_store.update_active_content(self.add_therm_id, self.add_device_screen.current_content)
        self.init_popup.theme_cls.theme_style = 'Light'
        self.update_content()

    def update_content(self, *args):
        self.content.clear_widgets()

        for content in [self.add_device_screen, self.thermostat_active]:
            if content.current_content:
                self.content.add_widget(content)

    def update_color(self, color1, color2):
        self.canvas.before.clear()
        CustomGradient.enable_gradient(self, color1, color2, radius=9)



