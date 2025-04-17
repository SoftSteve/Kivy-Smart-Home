from kivymd.uix.label import MDLabel
from kivy.uix.widget import Widget
from kivy.graphics import Line, Color
from kivy.properties import NumericProperty, StringProperty

class ThermostatWidget(Widget):
    temperature = NumericProperty(69)
    thermostat_id = StringProperty('Default Text')

    def __init__(self, callback, therm_store, **kwargs):
        super().__init__(**kwargs)
        self.therm_store = therm_store
        self.callback = callback
        
        self.thermostat_id = 'Thermostat1'
        self.temperature = self.therm_store.get_temperature(self.thermostat_id)

        with self.canvas:
            self.color = Color(1, 1, 1, .2)
            
            self.arc = Line(
                circle=(0, 0, 0, 225, 495),  
                width=8,
                cap_precision=10,  
            )
            self.temp_line_color = Color(0.82, 0.90, 0.99, 1) 
            self.temp_line = Line(
                circle=(0, 0, 0, 225, 225),  
                width=8,
                cap_precision=10,
            )
        self.bind(pos=self.update_arc, size=self.update_arc)
        self.update_arc()

        self.temp_label = MDLabel(
            id = self.thermostat_id,
            text=f'{self.temperature}°',
            size_hint = (1, 1),
            font_size = self.width * 0.125,
            halign = 'center',
            text_color = (0.82, 0.90, 0.99, 1),
            pos_hint = {'center_x':.52, 'center_y':.6}
        )
        self.bind(size=self.callback)

    def update_arc(self, *args):
        center_x = self.x + self.width / 2
        center_y = self.y + self.height / 2

        radius = min(self.width, self.height) / 2 - 10

        self.arc.circle = (
            center_x,
            center_y,
            radius, 
            225,  
            495,  
        )
        self.update_temperature_line(center_x, center_y, radius)

    def update_temperature_line(self, center_x, center_y, radius):
        temp_angle = 225 + (self.temperature / 100) * 270  

        self.temp_line.circle = (
            center_x,
            center_y,
            radius,
            225,  
            temp_angle,  
        )


    def increase_temperature(self, instance):
        self.temperature += 1
        if self.temperature > 99:  
            self.temperature = 99
        self.update_arc() 
        self.temp_label.text = f'{self.temperature}°'
        self.therm_store.update_temperature(self.thermostat_id, self.temperature)
        
    def decrease_temperature(self, instance):
        self.temperature -= 1
        if self.temperature < 0: 
            self.temperature = 0
        self.update_arc() 
        self.temp_label.text = f'{self.temperature}°'
        self.therm_store.update_temperature(self.thermostat_id, self.temperature)