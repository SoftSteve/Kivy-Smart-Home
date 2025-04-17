from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivy.uix.floatlayout import FloatLayout
from custom_ui.customgradient import CustomGradient
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.behaviors import RectangularRippleBehavior, BackgroundColorBehavior
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDLabel
from kivy.metrics import dp
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.image import Image
from kivy.uix.label import Label
from custom_ui.custom_circle import ColorCircle
from custom_ui.five_circle_shape import FiveCircleShape
from kivymd.uix.button import MDFabButton
from kivymd.uix.pickers import MDTimePickerDialHorizontal


class DimSwiper(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.track_start = 0  
        self.track_end = 1 
        self.light_start_value = 0  
        self.light_end_value = 255  
        self.border_color = (0,0,0,1)

        self.size_hint = (1,1)
        self.pos_hint = {'center_x': .5, 'center_y': .5}

        with self.canvas.before:
            self.swipe_color = Color(1, 1, 1, 1)  
            self.swipe_track = RoundedRectangle(size=self.size, pos=self.pos)

        self.bind(size=self.update_track, pos=self.update_track)

        self.value_indicator = MDIconButton(
            icon='lightbulb-night-outline', 
            font_size=30,
            theme_icon_color = 'Custom',
            icon_color=(0.25, 0.25, 0.25, 1),
            ripple_effect= False,
            focus_color = (0,0,0,0),
            size_hint=(None, None),
            size=(30, 30),
            pos_hint={'center_x': 0.55, 'y': 0.2},  
        )
        self.value_indicator.font_size = dp(24)
        self.add_widget(self.value_indicator)

    def on_touch_move(self, touch):
        if self.collide_point(*touch.pos):
            touch_position = touch.pos[1] 

            swipe_progress = (touch_position - self.pos[1] + 8) / self.height
            swipe_progress = max(0, min(1, swipe_progress))

            light_value = self.light_start_value + (swipe_progress * (self.light_end_value - self.light_start_value))
            self.set_light_output(light_value)

            self.update_swipe_track(swipe_progress)
            self.update_value_indicator(swipe_progress)

    def set_light_output(self, value):
        print(f"Setting light brightness to: {value}")

    def update_swipe_track(self, swipe_progress):
        self.swipe_track.pos = (self.pos[0], self.pos[1])
        self.swipe_track.size = (self.width, self.height * swipe_progress)
        self.swipe_color.rgba = (swipe_progress, swipe_progress, swipe_progress + 0.1, 1)

    def update_value_indicator(self, swipe_progress):
        self.value_indicator.color = (1, 1, 1, 1) if swipe_progress < 0.4 else (0.25, 0.25, 0.25, 1)

    def update_track(self, *args):
        self.swipe_track.size = self.size
        self.swipe_track.pos = self.pos




class DimLightsContent(FloatLayout):
    def __init__(self, size_hint = (1,1), pos_hint={'center_x':.5, 'center_y':.5}, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = size_hint
        self.pos_hint = pos_hint

        CustomGradient.enable_gradient(self, (0.65,.765,.876,0.2), (1,1,1,0.2), radius=10, border=True, border_color=(.65,.65,.65,1))

        self.img_container = BoxLayout(orientation='vertical', size_hint=(.3,1), pos_hint = {'center_x':.111, 'center_y':.5})
        self.add_widget(self.img_container)

        self.light_name = MDLabel(
            text='Light Name',
            theme_text_color = 'Custom',
            text_color = (1,1,1,1),
            font_style = 'Headline',
            role = 'small',
            size_hint_x = 1,
            halign='center',
            pos_hint={'center_x':.5, 'center_y':.9}
        )
        self.add_widget(self.light_name)

        self.light_image = Image(
            source='images/light-icon-dimmer.png',
            size_hint=(None, 1),   
            size=(self.width * 0.5, self.height)
        )  

        self.light_image.pos_hint = {'x': 0, 'top': 1}
        self.img_container.add_widget(self.light_image)

        self.bind(size=self.update_image_size)


        self.swipe_container = FloatLayout(size_hint=(.125,.65), pos_hint={'center_x':.9, 'center_y':.45})
        self.add_widget(self.swipe_container)
        CustomGradient.enable_gradient(self.swipe_container, (.1,0.1,0.1,1), (0.1,0.1,0.1,1), radius=10, border=True, border_color=(0,0,0,1), border_width=1.5)

        self.dimmer = DimSwiper()
        self.swipe_container.add_widget(self.dimmer)

        self.schedule_button = MDFabButton(
            icon='clock-plus-outline',
            style='small',
            pos_hint={'center_x':.7, 'center_y':.575},
            on_press = self.show_time_picker,
        )
        self.add_widget(self.schedule_button)

        self.color_button = MDFabButton(
            icon='palette-outline',
            style='small',
            pos_hint={'center_x':.7, 'center_y':.325},
        )
        self.add_widget(self.color_button)


    def show_time_picker(self, instance):
        time_picker = MDTimePickerDialHorizontal()
        time_picker.open()

    def on_time_selected(self, instance, time_value):
        print(f"Selected Time: {time_value}")

    def update_image_size(self, *args):
        self.light_image.size = (self.width * 0.5, self.height)

        