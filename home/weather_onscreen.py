from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.properties import BooleanProperty, StringProperty
from kivy.clock import Clock

from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton
from kivymd.uix.divider import MDDivider

from kivy.network.urlrequest import UrlRequest

from custom_ui.customgradient import CustomGradient 

class WeatherContent(FloatLayout):
    content_id = StringProperty('Initial')
    current_content = BooleanProperty(True)
    def __init__(self,current_content, content_id, weather_store, api_key, zip_code, country_code="US", **kwargs):
        super().__init__(**kwargs)
        self.pos_hint= {'center_x': .5, 'center_y': .5}
        self.text_color = (0.82, 0.90, 0.99, 1)
        self.weather_store = weather_store

        self.api_key = api_key
        self.zip_code = zip_code
        self.country_code = country_code
        self.weather_data = None

        self.current_content = current_content
        self.content_id = content_id


        self.icon = Image(
            size_hint=(None, None),
            width = self.width * 0.2,
            height = self.height * 0.2,
            pos_hint={'center_x': .2, 'center_y': .7},
        )

        self.current_weather = MDLabel(
            text='loading',
            theme_text_color='Custom',
            text_color=self.text_color,
            theme_font_name='Custom',
            font_name='fonts/ttf/Roboto-Light.ttf',
            font_style='Label',
            bold=False,
            halign='center',
            font_size = self.width * 0.5,
            pos_hint={'center_x': .225, 'center_y': .575},
        )
        self.current_weather.font_size = '12sp'

        self.current_city = MDLabel(
            text="Loading...",
            theme_text_color='Custom',
            text_color=self.text_color,
            bold=False,
            theme_font_name='Custom',
            font_name='fonts/ttf/Roboto-Light.ttf',
            halign='center',
            pos_hint={'center_x': .63, 'center_y': .87},
            font_size = self.width * 0.05,
        )
        self.current_city.font_size = '18sp'

        self.current_temp = MDLabel(
            text="Loading...",
            adaptive_size=True,
            font_size = self.width * 0.2,
            theme_text_color='Custom',
            text_color=self.text_color,
            bold=False,
            halign='center',
            pos_hint={'center_x': .625, 'center_y': .675},
        )
        self.current_temp.font_size = '30sp'

        self.refresh_weather_icon = MDIconButton(
            icon='refresh',
            style='outlined',
            theme_line_color='Custom',
            line_color=(0, 0, 0, 0),
            theme_icon_color='Custom',
            icon_color=(0.82, 0.90, 0.99, 1),
            pos_hint={'center_x': .925, 'center_y': .9},
            ripple_effect=False,
            on_press=self.press_animation,
            
        )
        self.refresh_weather_icon.font_size = 24

        self.divider = MDDivider(
            orientation='horizontal',
            size_hint_x=.9,
            pos_hint={'center_x': .5, 'center_y': .5}
        )

        self.forecast_layout_icon = BoxLayout(
            orientation = 'horizontal',
            size_hint=(1, .2), 
            spacing = self.width * 0.2,
            pos_hint={'center_x': .5, 'center_y': .2},
        )

        self.forecast_layout_temps = BoxLayout(
            orientation = 'horizontal', 
            size_hint=(1, None),
            spacing = self.width * 0.2,
            pos_hint={'center_x': .52, 'center_y': .11},
        )

        self.forecast_icons = [Image(
            size_hint=(None, None), 
            height = self.height * 0.2,
            width = self.width * 0.2,
            ) for _ in range(3)
        ]
        self.forecast_temps = [MDLabel(
            text='Loading...', 
            font_size=self.width * 0.1, 
            halign='center', 
            theme_text_color='Custom',
            text_color=self.text_color,
            bold=False,
            theme_font_name='Custom',
            font_name='fonts/ttf/Roboto-Light.ttf',
            ) for _ in range(3)
        ]

        for i in range(3):
            self.forecast_layout_icon.add_widget(self.forecast_icons[i])
            self.forecast_layout_temps.add_widget(self.forecast_temps[i])

        self.add_widget(self.icon)
        self.add_widget(self.current_city)
        self.add_widget(self.current_weather)
        self.add_widget(self.current_temp)
        self.add_widget(self.refresh_weather_icon)
        self.add_widget(self.divider)
        self.add_widget(self.forecast_layout_icon)
        self.add_widget(self.forecast_layout_temps)

        self.fetch_weather()

        self.bind(size=self.update_content)
        self.bind(size=self.update_position)

    def fetch_weather(self):
        url = f"http://api.openweathermap.org/data/2.5/forecast?zip={self.zip_code},{self.country_code}&appid={self.api_key}&units=imperial"
        UrlRequest(url, on_success=self.update_weather, on_error=self.error, on_failure=self.error)

    def update_weather(self, request, result):
        cloud_descriptions = ["few clouds", "scattered clouds", "broken clouds", 'overcast clouds']

        if result.get("cod") != "200":
            self.error(request, result)
            return

        self.weather_data = result
        current_weather = result['list'][0]
        weather_condition = current_weather['weather'][0]['main']
        weather_description = current_weather['weather'][0]['description']
        temperature = round(current_weather['main']['temp'])
        high_temp = round(current_weather['main']['temp_max'])
        low_temp = round(current_weather['main']['temp_min'])
        wind_speed = round(current_weather['wind']['speed'])
        rain_chance = int(current_weather.get('pop', 0) * 100)

        self.icon.source = self.get_weather_icon(weather_condition)
        if self.icon.source == 'images/clear.png':
            self.icon.width = self.width * 0.325
            self.icon.height = self.height * 0.325
            self.icon.pos_hint = {'center_x':.22, 'center_y':.8}

        city_name = result.get("city", {}).get("name", self.zip_code)
        self.current_city.text = f"{city_name}, PA"
        for current_weather in cloud_descriptions:
            if weather_description == current_weather:
                weather_description = 'partly cloudy'
        self.current_weather.text = weather_description.strip().title()
        self.current_temp.text = f'{temperature}°'

        for i in range(1, 4):
            day_forecast = result['list'][i * 8] 
            day_condition = day_forecast['weather'][0]['main']
            day_temp = round(day_forecast['main']['temp'])

            self.forecast_icons[i - 1].source = self.get_weather_icon(day_condition)
            self.forecast_temps[i - 1].text = f'{day_temp}°'
            
            if self.forecast_icons[i-1].source == 'images/clear.png':
                self.forecast_icons[i-1].source = 'images/cloudy.png'

    def get_weather_icon(self, condition):
        icon_mapping = {
            "Clear": "images/clear.png",
            "Clouds": "images/cloudy.png",
            "Rain": "images/rain.png",
            "Snow": "images/snow.png",
            "Thunderstorm": "images/thunderstorm.png",
            "Drizzle": "images/drizzle.png",
            "Mist": "images/mist.png"
        }
        return icon_mapping.get(condition, "images/default.png")

    def error(self, *args):
        self.current_weather.text = "Error fetching weather data!"
        print("Error fetching weather data:", args)

        self.zip_code = self.weather_store.get_city('zip_code')
        print(self.zip_code)
        
        Clock.schedule_once(lambda *args: self.fetch_weather(), 0)


    def press_animation(self, instance):
        anim = Animation(opacity=0.5, duration=0.1) + Animation(opacity=1, duration=0.3)
        anim &= Animation(font_size=16, duration=.1) + Animation(font_size=24.5, duration=.1)
        anim.start(instance)

        self.fetch_weather()


    def update_content(self, *args):
        self.icon.width = self.width * 0.5
        self.icon.height = self.height * 0.5

        if self.icon.source == 'images/clear.png':
            self.icon.width = self.width * 0.325
            self.icon.height = self.height * 0.325

        for icons in self.forecast_icons:
            icons.width = self.width * 0.3
            icons.height = self.height * 0.3

        self.forecast_layout_icon.spacing = self.width * 0.04

        for labels in self.forecast_temps:
            labels.font_size = self.width * 0.08
        
        self.forecast_layout_temps.spacing = self.width * 0.042

        self.current_temp.font_size = self.width * 0.125

        self.current_city.font_size = self.width * 0.08

        self.current_weather.font_size = self.width * 0.06

    def update_position(self, *args):
        if self.icon.source == 'images/clear.png':
            self.icon.pos_hint = {'center_x': .22, 'center_y': 0.8}