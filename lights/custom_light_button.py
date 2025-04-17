from kivy.properties import BooleanProperty, NumericProperty, StringProperty
from kivymd.uix.button import MDButton, MDIconButton, MDButtonText
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.uix.floatlayout import FloatLayout
from kivy.animation import Animation
from .dim_swiper import DimSwiper 
from custom_ui.customgradient import CustomGradient


class CustomLightButton(MDButton):
    switch_active = BooleanProperty(False)
    last_brightness = NumericProperty(0.8)  

    def __init__(self, store, text = 'Testing', button_id='Default Text', **kwargs):
        self.switch_active = kwargs.pop("state", False)
        
        super().__init__(**kwargs)
        self.theme_width = 'Custom'
        self.size_hint = (.45, .3)
        self.text = text
        self.id = button_id
        self.theme_bg_color = 'Custom'
        self.md_bg_color = (0.82, 0.90, 0.99, .8)
        self.theme_shadow_color = 'Custom'
        self.shadow_color = (0,0,0,0)
        self.line_color = 'black'
        self.ripple_behavior = False
        self.radius = [16]
        self.pos_hint = {'center_x': .5, 'center_y': .5}
        self.focus_color = (1,1,1,.2)
        self.store = store
        self.on_press = lambda *args: self.toggle_active(self)

        self.button_text = MDButtonText(
            text = self.text,
            pos_hint = {'center_x':.5, 'center_y':.5}
        )
        self.add_widget(self.button_text)


    def toggle_active(self, instance):
        self.switch_active = not self.switch_active
        print(f"Button {self.id} toggled to {'ON' if self.switch_active else 'OFF'}")

        self.store.update_state(self.id, self.text, self.switch_active, self.last_brightness)

        if self.id == 'All-Lights':
            self.toggle_all()

        if self.id == 'All-50':
            self.dim_50()
        
        if self.id == 'All-25':
            self.dim_25()
        
        if self.id == 'All-75':
            self.dim_75()


    def toggle_all(self, *args):
        all_btn_state = self.store.get_state('All-Lights')
        control_panel = self.get_control_panel()
        self.dont_add = ['All On', 'Dim 25%', 'Dim 50%', 'Dim 75%']

        for button in self.store.get_all_devices():
            name = button['name']
            if name not in self.dont_add:
                self.store.update_button_state(name, all_btn_state['state'])
                self.store.save_states()

    def dim_25(self, *args):
        dim_25 = self.store.get_state('All-25')
        self.dont_add = ['All On', 'Dim 25%', 'Dim 50%', 'Dim 75%']

        for button in self.store.get_all_devices():
            name = button['name']
            if name not in self.dont_add:
                dim_25['last_brightness'] = 0.3
                self.store.update_button_brightness(name, dim_25['last_brightness']) 
                self.store.save_states()


    def dim_50(self, *args):
        dim_50 = self.store.get_state('All-50')
        self.dont_add = ['All On', 'Dim 25%', 'Dim 50%', 'Dim 75%']

        for button in self.store.get_all_devices():
            name = button['name']
            if name not in self.dont_add:
                dim_50['last_brightness'] = 0.55
                self.store.update_button_brightness(name, dim_50['last_brightness']) 
                self.store.save_states()

    def dim_75(self, *args):
        dim_75 = self.store.get_state('All-75')
        self.dont_add = ['All On', 'Dim 25%', 'Dim 50%', 'Dim 75%']

        for button in self.store.get_all_devices():
            name = button['name']
            if name not in self.dont_add:
                dim_75['last_brightness'] = 0.8
                self.store.update_button_brightness(name, dim_75['last_brightness']) 
                self.store.save_states()

    def get_control_panel(self):
        parent = self.parent
        while parent:
            if hasattr(parent, 'Refresh_UI'):
                return parent
            parent = parent.parent
        return None


class CustomButton(MDCard):
    text = StringProperty("Default Text")
    button_id = StringProperty("Default Text")
    switch_active = BooleanProperty(False)
    last_brightness = NumericProperty(0.8)  
    current_brightness = NumericProperty(0.8)  

    def __init__(self, store, **kwargs):
        self.text = kwargs.pop("text", "Default Text")
        self.button_id = kwargs.pop("id", "Default Text")
        self.switch_active = kwargs.pop("state", False)

        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (225, 100)
        self.theme_bg_color = 'Custom'
        self.md_bg_color = (0, 0, 0, 0)
        self.line_color = 'grey'
        self.ripple_behavior = False
        self.radius = [30]
        self.pos_hint = {'center_x': .5, 'center_y': .5}
        self.focus_color = (0, 0, 0, 0)
        self.store = store
        

        self.border_color = (0, 0, 0, 1)
        CustomGradient.enable_gradient(self, (0.43, 0.54, 0.68754, 0.2), (.85, .85, .9, .3), radius=30)

        self.main_container = FloatLayout()
        self.add_widget(self.main_container)

        self.switch = MDIconButton(
            pos_hint={'center_x': 0.87, 'center_y': 0.74},
            icon='power',
            theme_icon_color='Custom',
            icon_color='lightgrey' if not self.switch_active else (0.82, 0.90, 0.99, 1),
            on_press=self.toggle_active,
            size_hint=(None, None),
            ripple_effect=False
        )
        self.switch.font_size = 30
        self.main_container.add_widget(self.switch)

        self.label = MDLabel(
            text=self.text,
            pos_hint={'center_x': 0.5, 'center_y': 0.7},
            size_hint_x = .8,
            theme_text_color='Custom',
            text_color='white' if self.switch_active else 'grey',
            halign='left'
        )
        self.label.font_size = 18
        self.main_container.add_widget(self.label)

        self.dim_container = FloatLayout(size_hint=(.875, .35), pos_hint={'center_x': .5, 'center_y': .3})
        self.main_container.add_widget(self.dim_container)
        CustomGradient.enable_gradient(self.dim_container, (0, 0, 0, .15), (0, 0, 0, .15), radius=15)

        self.dimmer = DimSwiper(parent=self)
        self.dim_container.add_widget(self.dimmer)

        self.apply_theme()

        self.initialize_dimmer_state()

    def initialize_dimmer_state(self):
        if self.switch_active:
            self.animate_dimmer(self.last_brightness)
        else:
            self.animate_dimmer(0.075)
        
    def apply_theme(self):
        self.switch.icon_color = (0.82, 0.90, 0.99, 1) if self.switch_active else 'grey'
        self.label.color = 'white' if self.switch_active else 'grey'
        self.dimmer.thumb.md_bg_color = (.95, .95, 1, 1) if self.switch_active else 'grey'

    def toggle_active(self, instance):
        if self.switch_active:
            self.last_brightness = self.dimmer.swipe_progress  
            self.last_color_temperature = 6500
            self.animate_dimmer(0.075)

        else:
            self.animate_dimmer(self.last_brightness)  

        self.switch_active = not self.switch_active
        self.apply_theme()

        self.store.update_state(
            self.button_id,
            self.text,
            self.switch_active,
            self.last_brightness,
        )

        print(f"Button {self.button_id} toggled to {'ON' if self.switch_active else 'OFF'}")

    def animate_dimmer(self, target_progress):
        self.dimmer.is_animating = True  
        anim = Animation(swipe_progress=target_progress, duration=0.1, t='out_quad')
        anim.bind(on_progress=lambda *args: self.update_dimmer_visuals())
        anim.bind(on_complete=lambda *args: self.animation_done())  
        anim.start(self.dimmer)

    def animation_done(self):
        self.dimmer.is_animating = False

    def update_dimmer_visuals(self):
        self.dimmer.update_swipe_track(self.dimmer.swipe_progress)
        self.dimmer.update_thumb(self.dimmer.swipe_progress)

    
    def on_touch_down(self, touch):
        if self.switch.collide_point(*touch.pos):
            return super().on_touch_down(touch)
            
        if self.collide_point(*touch.pos):
            return False
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        if self.switch.collide_point(*touch.pos):
            return super().on_touch_up(touch)
        
        if self.collide_point(*touch.pos):
            return False
        return super().on_touch_up(touch)