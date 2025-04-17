from kivy.uix.floatlayout import FloatLayout

from custom_ui.customgradient import CustomGradient  
from .lock_onscreen import LockOnScreen
from .add_lock import AddLockScreen, InitializePopup

class DoorLockPanel(FloatLayout):
    def __init__(self, lock_store, **kwargs):
        super().__init__(**kwargs)
        self.size_hint=(1,1)
        self.lock_store = lock_store
        self.text_color = (0.82, 0.90, 0.99, 1)

        self.add_device_screen = AddLockScreen(content_id='Add Lock screen', current_content=False, callback=self.add_device)
        self.lock_active = LockOnScreen(content_id='Lock On Screen', current_content=False, lock_store=self.lock_store)

     
        self.therm_active_id = self.lock_active.content_id
        self.add_therm_id = self.add_device_screen.content_id

        self.lock_active.current_content = self.lock_store.get_active_content(self.therm_active_id)
        self.add_device_screen.current_content = self.lock_store.get_active_content(self.add_therm_id)

        if not self.lock_active.current_content and not self.add_device_screen.current_content:
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

        self.lock_active.current_content = True
        self.add_device_screen.current_content = False

        self.lock_store.update_active_content(self.therm_active_id, self.lock_active.current_content)
        self.lock_store.update_active_content(self.add_therm_id, self.add_device_screen.current_content)
        self.init_popup.theme_cls.theme_style = 'Light'
        self.update_content()

    def update_content(self, *args):
        self.content.clear_widgets()

        for content in [self.add_device_screen, self.lock_active]:
            if content.current_content:
                self.content.add_widget(content)

    def update_color(self, color1, color2):
        self.canvas.before.clear()
        CustomGradient.enable_gradient(self, color1, color2, radius=9)

