from kivy.uix.widget import Widget
from kivy.properties import BooleanProperty, StringProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout

from kivymd.uix.button import MDIconButton, MDFabButton
from kivymd.uix.label import MDLabel
from kivy.metrics import dp

from custom_ui.customgradient import CustomGradient
from .thermostat import ThermostatWidget

class ThermostatOnScreen(FloatLayout):
        content_id = StringProperty('Initial')
        current_content = BooleanProperty(False)
        active_button = BooleanProperty(False)
        
        def __init__(self, content_id, current_content, therm_store, **kwargs):
            super().__init__(**kwargs)
            self.therm_store = therm_store
            self.content_id = content_id
            self.current_content = current_content

            self.pos_hint = {'center_x':.5, 'center_y':.55}

            self.thermostat = ThermostatWidget(size_hint=(.7, .7),pos_hint={'center_x':.5, 'center_y':.55}, callback = self.update_label, therm_store=self.therm_store)
            self.add_widget(self.thermostat)

            self.button_container = BoxLayout(
                 orientation='horizontal', 
                 size_hint=(.2, .2), 
                 pos_hint={'center_x':.51, 'center_y':.35}, 
                 spacing = 15
            )

            self.btn_increase = MDIconButton(
                icon='minus',
                style='outlined',
                theme_icon_color = 'Custom',
                icon_color = (0.82, 0.90, 0.99, 1),
                theme_line_color = 'Custom',
                line_color = (0.82, 0.90, 0.99, 1),
                halign='center',
                width = self.width * 0.85,
                font_size = self.width * 0.125,
                size_hint=(1, 1), 
                on_press=self.thermostat.decrease_temperature
            )
            
            self.btn_decrease = MDIconButton(
                icon='plus',
                style='outlined',
                theme_icon_color = 'Custom',
                icon_color = (0.82, 0.90, 0.99, 1),
                theme_line_color = 'Custom',
                line_color = (0.82, 0.90, 0.99, 1),
                width = self.width * 0.85,
                font_size = self.width * 0.125,
                halign='center',
                on_press=self.thermostat.increase_temperature
            )
            
            self.button_container.add_widget(self.btn_increase)
            self.button_container.add_widget(self.btn_decrease)
            
            self.add_widget(self.button_container)
            
            self.temp_label = self.thermostat.temp_label
            self.add_widget(self.temp_label)

            self.button_container2 = BoxLayout(
                orientation = 'horizontal',
                size_hint = (.775, .2),
                pos_hint = {'center_x':.5, 'center_y':.1},
                padding = 10,
                spacing = self.width * .1,
            )
            self.bind(size=self.update_spacing)

            self.heat = MDFabButton(
                id = 'Heat',
                icon = 'fire',
                adaptive_size = True,
                size_hint_x = None,
                width = self.width * 0.11,
                height = self.height * 0.16,
                font_size = self.width * 0.05,
                theme_bg_color = 'Custom',
                md_bg_color = (0.25, 0.25, 0.3, 1),
                theme_shadow_color = 'Custom',
                shadow_color = 'white',
                theme_icon_color = 'Custom',
                icon_color = (0.82, 0.90, 0.99, 1),
                on_release=self.change_button_state
            )
            self.cool = MDFabButton(
                id = 'Cool',
                icon = 'snowflake',
                adaptive_size = True,
                size_hint_x = None,
                width = self.width * 0.11,
                height = self.height * 0.16,
                font_size = self.width * 0.05,
                theme_bg_color = 'Custom',
                md_bg_color = (0.25, 0.25, 0.3, 1),
                theme_shadow_color = 'Custom',
                shadow_color = 'white',
                theme_icon_color = 'Custom',
                icon_color = (0.82, 0.90, 0.99, 1),
                on_release=self.change_button_state
            )
            self.eco = MDFabButton(
                id = 'Eco',
                icon='leaf',
                size_hint = (1,1),
                adaptive_size = True,
                size_hint_x = None,
                width = self.width * 0.11,
                height = self.height * 0.16,
                font_size = self.width * 0.05,
                theme_bg_color = 'Custom',
                md_bg_color = (0.25, 0.25, 0.3, 1),
                theme_shadow_color = 'Custom',
                shadow_color = 'white',
                theme_icon_color = 'Custom',
                icon_color = (0.82, 0.90, 0.99, 1),
                on_release=self.change_button_state
            )
            self.fan = MDFabButton(
                id = 'Fan',
                icon = 'weather-windy',
                adaptive_size = True,
                size_hint_x = None,
                width = self.width * 0.11,
                height = self.height * 0.16,
                font_size = self.width * 0.05,
                theme_bg_color = 'Custom',
                md_bg_color = (0.25, 0.25, 0.3, 1),
                theme_shadow_color = 'Custom',
                shadow_color = 'white',
                theme_icon_color = 'Custom',
                icon_color = (0.82, 0.90, 0.99, 1),
                on_release=self.change_button_state
            )
            self.bind(size=self.update_buttons)

            self.mode_label = MDLabel(
                text = 'Mode: None',
                text_color = 'white',
                size_hint = (1,1),
                font_size = self.width * 0.03,
                pos_hint = {'center_x':.5, 'center_y':.48},
                halign = 'center',
                theme_font_name = 'Custom',
                font_name = 'fonts/ttf/Roboto-Light.ttf'
            )
            self.bind(size=self.update_label)
            self.add_widget(self.mode_label)
            
            self.add_widget(self.button_container2)
            self.button_container2.add_widget(self.heat)
            self.button_container2.add_widget(self.cool)
            self.button_container2.add_widget(self.eco)
            self.button_container2.add_widget(self.fan)
            

            self.refresh_ui()

        def change_button_state(self, instance, false_color_bg=(0.25, 0.25, 0.3, 1), false_icon = (0.82, 0.90, 0.99, 1)):
            if self.active_button:
                self.active_button.md_bg_color =  false_color_bg
                self.active_button.icon_color =  false_icon
                self.mode_label.text = 'Mode: None'
                print(f"{self.active_button.id}: Inactive")
                self.therm_store.update_state(self.active_button.id, False)

            if self.active_button == instance:
                self.active_button = False 

            else:
                instance.md_bg_color = (0.82, 0.90, 0.99, 1)
                instance.icon_color = (0.25, 0.25, 0.3, 1)
                self.active_button = instance
                self.mode_label.text = f'Mode: {instance.id}'
                print(f"{self.active_button.id}: Active")
                self.therm_store.update_state(instance.id, True)
    
        def refresh_ui(self):
            for button in [self.heat, self.cool, self.eco, self.fan]:
                if self.therm_store.get_state(button.id):  # Check if button was active
                    button.md_bg_color = (0.82, 0.90, 0.99, 1)
                    button.icon_color = (0.25, 0.25, 0.3, 1)
                    self.mode_label.text = f'Mode: {button.id}'
                    self.active_button = button
                else:
                    button.md_bg_color = (0.25, 0.25, 0.3, 1)
                    button.icon_color = (0.82, 0.90, 0.99, 1)

        def update_color(self, color1, color2):
            self.canvas.before.clear()
            CustomGradient.enable_gradient(self, color1, color2, radius=9)

        def update_label(self, *args):
            self.mode_label.font_size = self.width * .03
            self.thermostat.temp_label.font_size = self.width * 0.125

        def update_buttons(self, *args):
            for button in [self.heat, self.cool, self.eco, self.fan]:
                button.width = self.width * 0.11
                button.height = self.height * 0.16
                button.font_size = self.width * 0.05
                button.halign = 'center'

            for buttons in [self.btn_decrease, self.btn_increase]:
                buttons.width = self.width * 0.085
                buttons.height = self.height * 0.125
                buttons.font_size = self.width * 0.05

        def update_spacing(self, *args):
            self.button_container2.spacing = self.width * .1
            self.button_container.spacing = self.width * 0.02