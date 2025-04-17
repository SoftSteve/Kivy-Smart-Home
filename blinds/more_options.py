from kivy.properties import BooleanProperty, NumericProperty
from kivymd.uix.button import MDButton, MDIconButton, MDButtonText
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.uix.floatlayout import FloatLayout
from kivy.animation import Animation
from .blinds_swiper import BlindsSwiper
from custom_ui.customgradient import CustomGradient

class CustomBlindButton2(MDCard):
    switch_active = BooleanProperty(False)
    blinds_start = NumericProperty(.95)  

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

        self.store.update_states(self.id, self.text, self.switch_active, self.blinds_start)

        self.all_btn_state = self.store.get_button_state('t100%')['state']

        if self.id == 't50%':
            self.toggle_50()
        if self.id == 't75%':
            self.toggle_75()
        if self.id == 't100%':
            self.toggle_100()

            
    def toggle_50(self, *args):
        all_btn_state = self.store.get_button_state('t50%')['state']
        self.dont_add = ['t100%', 'tscd', 't50%', 't75%', 'Patio-All']

        for button in self.store.get_all_devices():
            button_id = button['button_id']
            button_blinds = button['blinds_start']
            if button_id not in self.dont_add:
                button_blinds = .55
                self.store.update_button_blinds(button_id, button_blinds)
                self.store.save_states()
        
    def toggle_75(self, *args):
        all_btn_state = self.store.get_button_state('t75%')['state']
        self.dont_add = ['t100%', 'tscd', 't50%', 't75%', 'Patio-All']

        for button in self.store.get_all_devices():
            button_id = button['button_id']
            button_blinds = button['blinds_start']
            if button_id not in self.dont_add:
                button_blinds = .8
                self.store.update_button_blinds(button_id, button_blinds)
                self.store.save_states()
    
    def toggle_100(self, *args):
        all_btn_state = self.store.get_button_state('t100%')['state']
        self.dont_add = ['t100%', 'tscd', 't50%', 't75%', 'Patio-All']

        for button in self.store.get_all_devices():
            button_id = button['button_id']
            button_blinds = button['blinds_start']
            if button_id not in self.dont_add:
                button_blinds = .95
                self.store.update_button_blinds(button_id, button_blinds)
                self.store.save_states()

            if button_id not in self.dont_add:
                self.button_blind = button['blinds_start']
                self.store.update_button_state(button_id, all_btn_state)
                self.store.save_states()  

    def schedule_blinds(self, *args):
        self.dont_add = ['t100%', 'tscd', 't50%', 't75%']

        for button in self.store.get_all_devices():
            button_id = button['button_id']
            button_blinds = button['blinds_start']
            schedule_time = None
            blinds_pos = None
            if button_id not in self.dont_add and schedule_time:
                button_blinds = blinds_pos
                self.store.update_button_blinds(button_id, button_blinds)
                self.store.save_states()