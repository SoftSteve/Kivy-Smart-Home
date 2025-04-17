from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout

from kivy.properties import BooleanProperty
from kivy.animation import Animation
from kivy.clock import Clock

from kivymd.uix.label import MDLabel
from kivy.uix.scrollview import ScrollView

from custom_ui.customgradient import CustomGradient 
from .active_buttons import DeviceListItem 


class ActivePanel(Widget):
    def __init__(self, store, **kwargs):
        super().__init__(**kwargs)
        self.store = store
        self.active_buttons = {}
        self.text_color = (0.82, 0.90, 0.99, 1)
         

        self.update_color(
        color1 = (.85, .85, .9, .3),
        color2 = (0.43, 0.54, 0.68754, 0.2)
        )

        self.main_container = FloatLayout(size_hint=(1, 1))
        self.add_widget(self.main_container)

        self.scroll_view = ScrollView(
            size_hint=(.9, None),
            do_scroll_y=True,
            effect_y=None,
            bar_width=3,
            bar_pos_y='left',
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.main_container.add_widget(self.scroll_view)

        self.grid_container = GridLayout(
            size_hint=(1, None),
            padding=10,
            cols=1,
            spacing=5,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
        )
        self.grid_container.bind(minimum_height=self.grid_container.setter('height'))
        self.scroll_view.add_widget(self.grid_container)

        self.title = MDLabel(
            text='Running Devices',
            theme_font_name='Custom',
            font_name='fonts/ttf/Roboto-Regular.ttf',
            theme_text_color='Custom',
            text_color=self.text_color,
            pos_hint={'center_x': .5, 'center_y': .9},
            halign='center'
        )
        self.main_container.add_widget(self.title)

        self.no_devices_label = MDLabel(
            text="No active devices",
            theme_text_color="Custom",
            text_color='white',
            halign="center"
        )
        self.grid_container.add_widget(self.no_devices_label)

    def update_active_devices(self, *args):
        active_devices = self.store.get_active_devices()
        self.dont_add = {'All-Lights', 'All-25', 'All-50', 'All-75'}

        active_ids = {device['checkbox_id'] for device in active_devices}

        for device_id in list(self.active_buttons.keys()):
            if device_id not in active_ids:
                self.remove_button(self.active_buttons[device_id])

        if active_devices:
            if self.no_devices_label.parent:
                self.grid_container.remove_widget(self.no_devices_label)

            for device in active_devices:
                device_id = device['checkbox_id']
                if device_id in self.dont_add:
                    continue

                last_brightness = self.store.get_state(device_id).get("last_brightness", 0.8)

                if device_id not in self.active_buttons:
                    new_button = DeviceListItem(
                        text=device['name'],
                        id=device_id,
                        state=device['active'],
                        last_brightness=last_brightness,
                        store=self.store,
                        on_press=self.toggle_state
                    )
                    self.grid_container.add_widget(new_button)
                    self.active_buttons[device_id] = new_button  
        else:
            if not self.no_devices_label.parent:
                self.grid_container.add_widget(self.no_devices_label)

    def toggle_state(self, button):
        current_state = self.store.get_state(button.id).get("state", False)
        new_state = not current_state
        current_brightness = self.store.get_state(button.id).get("last_brightness", 0.8)

        self.store.update_state(button.id, button.text.split(':')[0], new_state, current_brightness)

        if not new_state:
            Clock.schedule_once(lambda dt: self.remove_button(button), 0.1)

    def remove_button(self, button):
        fade_out = Animation(opacity=0, duration=0.6)
        fade_out.bind(on_complete=lambda *args: self._final_remove(button))
        fade_out.start(button)

    def _final_remove(self, button):
        if button in self.active_buttons.values():
            self.grid_container.remove_widget(button)
            self.active_buttons.pop(button.id, None)  

        if not self.active_buttons: 
            self.grid_container.add_widget(self.no_devices_label)

    def update_color(self, color1, color2):
        self.canvas.before.clear()
        CustomGradient.enable_gradient(self, color1, color2, radius=9)

    def update_content_position(self, *args):
        self.main_container.size = (self.width, self.height)
        self.main_container.pos = self.pos

        self.scroll_view.size = (self.width * .8, self.height * .725) 
        self.scroll_view.pos = self.pos

        self.grid_container.size = (self.scroll_view.width, self.grid_container.height) 
        self.grid_container.pos = self.pos

