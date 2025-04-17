from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.divider import MDDivider
from kivymd.uix.label import MDLabel
from kivymd.uix.pickers import MDTimePickerDialHorizontal
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarSupportingText
from kivy.metrics import dp
from custom_ui.custom_app_bar import AppBar  # Assuming AppBar is in a separate file
from .custom_fan_button import CustomFanButton  # Assuming CustomBlindButton is in a separate file
from .more_options import CustomFanButton2  # Assuming CustomBlindButton2 is in a separate file
from custom_ui.customgradient import CustomGradient  # Assuming CustomGradient is in a separate file


class FansControlPanel(Widget):
    def __init__(self, store, **kwargs):
        super().__init__(**kwargs)
        self.store = store

        CustomGradient.enable_gradient(self, (0.43, 0.54, 0.68754, 0.2), (.85, .85, .9, .3), radius=9)

        self.main_container = FloatLayout(size_hint=(1, 1))
        self.add_widget(self.main_container)    

        #-----------------------------Title-------------------------------#
        self.app_bar = AppBar(
            title_name='Fans',
            menu_items=[
                {"text": f"Edit Names", "callback": self.callback_edit},
                {"text": f"Delete", "callback": self.callback_delete},
                {"text": f"Add Devices", "callback": self.callback_add},
            ]
        )
        self.main_container.add_widget(self.app_bar)
        self.main_container.add_widget(MDDivider(orientation='horizontal', size_hint_x = .9, pos_hint={'center_x':.5, 'center_y':.85}))
        #-----------------------------Content Area Left-------------------------------#
        self.content_container = FloatLayout(
            size_hint = (1, .85),
            pos_hint = {'center_x':.5, 'center_y':.425}
        )
        self.main_container.add_widget(self.content_container)

        self.scrollview = MDScrollView(
            size_hint =(.45, .9),
            do_scroll_y = True,
            pos_hint={'center_x':0.275, 'center_y':.5},
            bar_pos_y = 'left',
            bar_width = 5,
            bar_margin=-22
        )
        self.content_container.add_widget(self.scrollview)

        self.grid_layout = GridLayout(
            size_hint = (.95, None),
            cols = 1,
            spacing  = 15,
            padding = 10,
            pos_hint={'center_x':.4, 'center_y':.5}
        )
        self.grid_layout.bind(minimum_height=self.grid_layout.setter('height'))
        self.scrollview.add_widget(self.grid_layout)
        

        left_state = store.get_button_state('Patio-Left')["state"]
        right_state = store.get_button_state('Patio-Right')["state"]
        
        self.fan_left = CustomFanButton(
            text='Back Patio-Left',
            id='Patio-Left',
            state=left_state,
            store=store
        )

        self.fan_right = CustomFanButton(
            text='Back Patio-Right',
            id='Patio-Right',
            state=right_state,
            store=store
        )

        self.grid_layout.add_widget(self.fan_left)
        self.grid_layout.add_widget(self.fan_right)

        #--------------------------Content Area Right---------------------------#
        self.content_container_right = BoxLayout(
            orientation='vertical', 
            size_hint=(.45,.9), 
            spacing=10,
            pos_hint = {'center_x':.725, 'center_y':.5}
        )
        self.content_container.add_widget(self.content_container_right)
        
        self.content_top = FloatLayout(
            size_hint = (1, .55),
        )

        self.content_bottom = FloatLayout(
            size_hint = (.9, .45)
        )
        CustomGradient.enable_gradient(self.content_top, (0.43, 0.54, 0.68754, 0), (.85, .85, .9, 0), radius = 9)
        CustomGradient.enable_gradient(self.content_bottom, (0.43, 0.54, 0.68754, 0), (.85, .85, .9, 0), radius = 9)
        self.content_container_right.add_widget(self.content_top)
        self.content_container_right.add_widget(self.content_bottom)

        self.top_label = MDLabel(
            text = 'All Fans',
            theme_text_color = 'Custom',    
            text_color = 'white',
            font_style='Title',
            role='medium',
            pos_hint={'center_x':.5, 'center_y':.9},
            halign = 'left'
        )
        self.content_top.add_widget(self.top_label)

        self.bottom_label = MDLabel(
            text = 'Development',
            theme_text_color = 'Custom',
            text_color = 'white',
            font_style='Title',
            role='medium',
            pos_hint={'center_x':.5, 'center_y':.9},
            halign = 'left'
        )
        self.content_bottom.add_widget(self.bottom_label)

        self.top_btn_container = GridLayout(
            cols = 2,
            spacing = 10,
            padding=5,
            size_hint = (.9, .7),
            pos_hint = {'center_x':.5, 'center_y':.45}
        )

        self.content_top.add_widget(self.top_btn_container)

        self.half_btn = CustomFanButton2(
            text='50% Speed',
            button_id='50%',
            state=False,
            store = self.store,
            size_hint = (.4, .35),
            pos_hint = {'center_x':.5, 'center_y':.75},
        )

        self.threequarter_btn = CustomFanButton2(
            text='75% Speed',
            button_id='75%',
            state=False,
            store = self.store,
            size_hint = (.4, .35),
            pos_hint = {'center_x':.5, 'center_y':.75},
        )

        self.schedule_btn = CustomFanButton2(
            text='Schedule',
            button_id='scd',
            state=False,
            store = self.store,
            size_hint = (.4, .35),
            pos_hint = {'center_x':.5, 'center_y':.3},
        )
        self.schedule_btn.bind(switch_active=self.open_time_picker)

        self.lower = CustomFanButton2(
            text='All fans',
            button_id='All-Fans',
            state=False,
            store = self.store,
            size_hint = (.4, .35),
            pos_hint = {'center_x':.5, 'center_y':.3},
        )

        self.top_btn_container.add_widget(self.lower)
        self.top_btn_container.add_widget(self.schedule_btn)
        self.top_btn_container.add_widget(self.half_btn)
        self.top_btn_container.add_widget(self.threequarter_btn)
        
        self.bind(size=self.update_sizes)
        
    #-----------------------------Positioning and Functions-------------------------------#

    def callback_edit(self, *args):
        print(f"Editing device:")
    
    def callback_delete(self, *args):
        print(f"Deleting device: ")
    
    def callback_add(self, *args):
        print(f"Adding device: ")
    
    def open_time_picker(self, *args):
        self.scrollview.do_scroll_y = False
        self.scrollview.do_scroll_x = False
        self.time_picker_horizontal = MDTimePickerDialHorizontal()
        self.time_picker_horizontal.theme_cls.theme_style = 'Dark'
        self.time_picker_horizontal.bind(on_cancel=self.on_cancel)
        self.time_picker_horizontal.bind(on_ok=self.on_ok)
        self.time_picker_horizontal.open()
    
    def on_cancel(self, time_picker_horizontal: MDTimePickerDialHorizontal):
        self.time_picker_horizontal = time_picker_horizontal
        time_picker_horizontal.dismiss()
        self.time_picker_horizontal.theme_cls.theme_style = 'Light'
        self.scrollview.do_scroll_y = True

    def on_ok(self, time_picker_horizontal: MDTimePickerDialHorizontal):
        self.time_picker_horizontal = time_picker_horizontal

        MDSnackbar(
            MDSnackbarSupportingText(text=f"Time is `{self.time_picker_horizontal.hour}:{self.time_picker_horizontal.minute}`"),
            y=dp(24),
            orientation="horizontal",
            pos_hint={"center_x": 0.5},
            size_hint_x=0.5,
        ).open()

        self.time_picker_horizontal.bind(time=self.get_time)
        time_picker_horizontal.dismiss()
        self.time_picker_horizontal.theme_cls.theme_style = 'Light'
        self.scrollview.do_scroll_y = True
    
    def get_time(self, instance, time):
        if time:
            print(f"Selected time: {time}")
        else:
            print("No time selected")

    def refresh_ui(self, *args):
        if self.grid_layout.children:
            pass
        else:
            self.grid_layout.clear_widgets()
            self.store.load_states()
            self.dont_add = ['All-Fans', 'scd', '50%', '75%']

            for device in self.store.get_all_devices():
                button_id = device['button_id']
                name = device['name']
                saved_state = device['state']
                new_fan_speed = device["fan_speed"]
                if button_id not in self.dont_add:
                    self.new_button = CustomFanButton(
                        text=name,
                        id=button_id,
                        state=saved_state,
                        fan_speed = new_fan_speed,
                        store=self.store,
                    )
                    self.grid_layout.add_widget(self.new_button)

                    self.new_button.apply_theme()

                    self.store.update_states(button_id, name, saved_state, new_fan_speed)   

    def update_content_position(self, *args):
        self.main_container.pos = self.pos
        self.main_container.size = self.size   

    def update_sizes(self, *args):
        for button in [self.fan_right, self.fan_left]:
            button.width = self.width * 0.3475
            button.height = self.height * 0.235
            button.dimmer.thumb.width = self.width * 0.0575
            button.dimmer.thumb.height = self.height * 0.085
            button.dimmer.thumb.font_size = self.width * 0.04


class FanControlScreen(FloatLayout):
    def __init__(self, store, **kwargs):
        super().__init__(**kwargs)
        self.store = store
        
        self.control_panel = FansControlPanel(
            size_hint = (.75, 1),
            pos_hint={'x': 0.225, 'y': 0.025},
            store=self.store
        )
        self.add_widget(self.control_panel)

