from kivy.properties import BooleanProperty, NumericProperty
from kivymd.uix.button import MDButton, MDIconButton, MDButtonText
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.uix.floatlayout import FloatLayout
from kivy.animation import Animation
from .fan_swiper import FanSwiper
from custom_ui.customgradient import CustomGradient

class CustomFanButton2(MDCard):
    switch_active = BooleanProperty(False)
    fan_speed = NumericProperty(.95)  

    def __init__(self, store, text = '', button_id='', **kwargs):
        self.switch_active = kwargs.pop("state", False)
        
        super().__init__(**kwargs)
        self.theme_width = 'Custom'
        self.size_hint = (.45, .3)
        self.text = text
        self.id = button_id
        self.theme_bg_color = 'Custom'
        self.md_bg_color = (0,0,0,0)
        self.theme_shadow_color = 'Custom'
        self.shadow_color = (0,0,0,0)
        self.line_color = 'black'
        self.ripple_behavior = False
        self.radius = [15]
        self.pos_hint = {'center_x': .5, 'center_y': .5}
        self.focus_color = (1,1,1,.2)
        self.store = store
        self.on_press = lambda: self.toggle_active(self)

        CustomGradient.enable_gradient(self, (.85, .85, .9, .3), (0.43, 0.54, 0.68754, 0.2), radius=15)

        self.label = MDLabel(
            text=self.text,
            pos_hint={'center_x': 0.5, 'center_y': 0.475},
            theme_text_color='Custom',
            size_hint_x = .8,
            text_color='white',
            halign='center'
        )
        self.label.font_size = 16
        self.add_widget(self.label)


    def toggle_active(self, instance):
        self.switch_active = not self.switch_active
        print(f"Button {self.id} toggled to {'ON' if self.switch_active else 'OFF'}")

        self.store.update_states(self.id, self.text, self.switch_active, self.fan_speed)

        self.all_btn_state = self.store.get_button_state('All-Fans')['state']
        
        if self.id == '50%':
            self.toggle_50()
        if self.id == '75%':
            self.toggle_75()
        if self.id == 'All-Fans':
            self.toggle_100()

            
    def toggle_50(self, *args):
        #if store.get_button_state('Patio-Left')["state"] or store.get_button_state('Patio-Right')["state"]:
        self.dont_add = ['All-Fans', 'scd', '50%', '75%']

        for button in self.store.get_all_devices():
            button_id = button['button_id']
            button_fans = button['fan_speed']
            if button_id not in self.dont_add:
                button_fans = .55
                self.store.update_button_fans(button_id, button_fans)
                self.store.save_states()
        
    def toggle_75(self, *args):
        all_btn_state = self.store.get_button_state('75%')['state']
        self.dont_add = ['All-Fans', 'scd', '50%', '75%']

        for button in self.store.get_all_devices():
            button_id = button['button_id']
            button_fans = button['fan_speed']
            if button_id not in self.dont_add:
                button_fans = .8
                self.store.update_button_fans(button_id, button_fans)
                self.store.save_states()
    
    def toggle_100(self, *args):
        all_btn_state = self.store.get_button_state('All-Fans')['state']
        self.dont_add = ['All-Fans', 'scd', '50%', '75%']

        for button in self.store.get_all_devices():
            button_id = button['button_id']
            button_fans = button['fan_speed']
            if button_id not in self.dont_add:
                button_fans = .95
                self.store.update_button_fans(button_id, button_fans)
                self.store.save_states()

            if button_id not in self.dont_add:
                self.button_blind = button['fan_speed']
                self.store.update_button_state(button_id, all_btn_state)
                self.store.save_states()  

    def schedule_blinds(self, *args):
        self.dont_add = ['All-Fans', 'scd', '50%', '75%']

        for button in self.store.get_all_devices():
            button_id = button['button_id']
            button_fans = button['fans_speed']
            schedule_time = None
            fans_speed = None
            if button_id not in self.dont_add and schedule_time:
                button_fans = fans_speed
                self.store.update_button_fans(button_id, button_fans)
                self.store.save_states()

