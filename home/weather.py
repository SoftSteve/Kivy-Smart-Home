from kivy.uix.floatlayout import FloatLayout
from kivy.properties import NumericProperty
from kivy.metrics import dp

from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText

from custom_ui.customgradient import CustomGradient  
from .weather_onscreen import WeatherContent
from .weather_add import AddWeatherScreen, InitializePopup


class WeatherPanel(FloatLayout):
    zip_input = NumericProperty(11111)
    def __init__(self, weather_store, **kwargs):
        super().__init__(**kwargs)
        self.pos_hint = {'center_x':.5, 'center_y': .5}
        self.weather_store = weather_store
        self.text_color = (0.82, 0.90, 0.99, 1)
        

        self.add_device_screen = AddWeatherScreen(content_id='Add weather screen', current_content=False, callback=self.add_device)
        self.weather_active = WeatherContent(
            content_id='Weather On Screen', 
            api_key = "0f1332b54092476664f1de293d6de51d", 
            zip_code = self.zip_input, 
            country_code='US',
            current_content=False,
            weather_store=self.weather_store
        )

     
        self.therm_active_id = self.weather_active.content_id
        self.add_therm_id = self.add_device_screen.content_id

        self.weather_active.current_content = self.weather_store.get_active_content(self.therm_active_id)
        self.add_device_screen.current_content = self.weather_store.get_active_content(self.add_therm_id)

        if not self.weather_active.current_content and not self.add_device_screen.current_content:
            self.add_device_screen.current_content = True 

        self.build()

    def build(self):
        self.update_color(
            color1=(.85, .85, .9, .3),
            color2=(0.43, 0.54, 0.68754, 0.2)
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
        if len(str(self.init_popup.text_input.text)) != 5:
            MDSnackbar(
            MDSnackbarText(
                text="Enter a '5' digit zipcode.",
            ),
            y=dp(24),
            pos_hint={"center_x": 0.5},
            size_hint_x=0.5,
        ).open()
            return
        
        else:
            self.init_popup.dismiss()

            self.weather_active.current_content = True
            self.add_device_screen.current_content = False

            self.weather_store.update_active_content(self.therm_active_id, self.weather_active.current_content)
            self.weather_store.update_active_content(self.add_therm_id, self.add_device_screen.current_content)
            
            self.update_content()

            self.init_popup.theme_cls.theme_style = 'Light'

            self.zip_input = int(self.init_popup.text_input.text)

            self.weather_active.zip_code = self.zip_input
            
            self.weather_store.update_city('zip_code', self.weather_active.zip_code)

            self.weather_active.fetch_weather()

    def update_content(self, *args):
        self.content.clear_widgets()

        for content in [self.add_device_screen, self.weather_active]:
            if content.current_content:
                self.content.add_widget(content)

    def update_color(self, color1, color2):
        self.canvas.before.clear()
        CustomGradient.enable_gradient(self, color1, color2, radius=9)

