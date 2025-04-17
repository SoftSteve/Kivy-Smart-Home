from kivy.uix.floatlayout import FloatLayout
from custom_ui.customgradient import CustomGradient
from kivy.uix.gridlayout import GridLayout
from lights.custom_light_button import CustomLightButton

class MoreOptions(FloatLayout):
    def __init__(self, store, title='Default Title', size_hint=(.5,.3), pos_hint = {'center_x':.75, 'center_y':.15}, **kwargs):
        super().__init__(**kwargs)
        self.pos_hint = pos_hint
        self.size_hint = size_hint
        self.title = title
        self.store = store

        CustomGradient.enable_gradient(self, (.85, .85, .9, 0), (0.43, 0.54, 0.68754, 0), radius=9)

        self.button_container = GridLayout(
            size_hint = (1, .9),
            cols = 2,
            spacing = 10,
            padding = 5,
            pos_hint = {'center_x':.5, 'center_y':.5}
        )
        self.add_widget(self.button_container)

        self.all_lights = CustomLightButton(
            text='All On',
            button_id = 'All-Lights',
            state = False,
            store=self.store
        )

        self.all_25 = CustomLightButton(
            text='Dim 25%',
            button_id = 'All-25',
            state = False,
            store=self.store
        )
    
        self.all_50 = CustomLightButton(
            text='Dim 50%',
            button_id = 'All-50',
            state = False,
            store=self.store
        )

        self.all_75 = CustomLightButton(
            text='Dim 75%',
            button_id = 'All-75',
            state = False,
            store=self.store
        )

        self.button_container.add_widget(self.all_lights)
        self.button_container.add_widget(self.all_25)
        self.button_container.add_widget(self.all_50)
        self.button_container.add_widget(self.all_75)