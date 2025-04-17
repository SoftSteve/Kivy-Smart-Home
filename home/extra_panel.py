from kivy.uix.floatlayout import FloatLayout

from kivymd.uix.button import MDIconButton, MDButton, MDButtonText, MDFabButton

from custom_ui.customgradient import CustomGradient
from .extra_home import ExtraHome

class Extra(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.build()

    def build(self):
        self.update_color(
            color1 = (.85, .85, .9, .3),
            color2 = (.85, .85, .9, .3)
            )
        self.content = FloatLayout(size_hint = (1,1), pos_hint = {'center_x':.5, 'center_y':.5})
        self.add_widget(self.content)

        self.show_home()

    def show_home(self, *args):
        self.extra_home = ExtraHome(volume_callback=self.show_volume_popup, bt_callback=self.show_bt_popup)
        self.update_content(self.extra_home)

    def show_volume_popup(self, *args):
        pass

    def show_bt_popup(self, *args):
        pass
    
    def update_content(self, widget):
        self.content.clear_widgets()
        self.content.add_widget(widget)

    def update_color(self, color1, color2):
        self.canvas.before.clear()
        CustomGradient.enable_gradient(self, color1, color2, radius=9, direction='vertical')
    
    def update_content_position(self, *args):
        self.content.pos = self.pos
        self.content.size = self.size