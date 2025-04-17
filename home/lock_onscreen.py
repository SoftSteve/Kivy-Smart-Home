from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import BooleanProperty, StringProperty

from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton

from .lock_swipe import DimSwiper
from custom_ui.customgradient import CustomGradient  

class LockOnScreen(FloatLayout):
    content_id = StringProperty('Initial')
    current_content = BooleanProperty(True)
    def __init__(self, lock_store, **kwargs):
        super().__init__(**kwargs)
        self.size_hint=(1,1)
        self.pos_hint = {'center_x':.5, 'center_y':.5}
        self.lock_store = lock_store
        self.text_color = (0.82, 0.90, 0.99, 1)

        self.title = MDLabel(
            text='Front Door Lock',
            size_hint=(.8, None),
            text_color = self.text_color,
            pos_hint = {'center_x':.5, 'center_y':.775},
            halign = 'left'
            
        )
        self.add_widget(self.title)

        self.label = MDLabel(
            text='Unlocked',
            text_color = self.text_color,
            size_hint_x = .8,
            pos_hint = {'center_x':.5, 'center_y':.565},
            halign = 'left'
            
        )
        self.label.font_size='12sp'
        self.add_widget(self.label)

        self.lock_icon = MDIconButton(
            icon='lock-open-variant',
            ripple_effect = False,
            theme_icon_color = 'Custom',
            icon_color = (0.82, 0.90, 0.99, 1),
            pos_hint = {'center_x':.92, 'center_y':.8},

        )
        self.lock_icon.font_size = '20sp'
        self.add_widget(self.lock_icon)

        self.swipe_container = FloatLayout(size_hint = (.8, .35), pos_hint = {'center_x':.5, 'center_y':.25})
        self.add_widget(self.swipe_container)
        CustomGradient.enable_gradient(self.swipe_container, (0.45,0.45,0.45,.2), (0.45,.45,.45,.2), radius=17.5)

        self.lock_swipe = DimSwiper(parent=self, lock_store=self.lock_store)
        self.swipe_container.add_widget(self.lock_swipe)

