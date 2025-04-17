from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDButton, MDButtonIcon
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu
from kivy.graphics import Color, RoundedRectangle


class AppBar(BoxLayout):
    def __init__(self, title_name='', menu_items=None, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (1, 0.15)
        self.pos_hint = {'x': 0, 'y': 0.85}
        self.orientation = 'horizontal'
        self.spacing = 10
        self.title_name = title_name
        self.menu_items = menu_items if menu_items else [
            {"text": f"Item {i}", "callback": lambda: print(f"Default callback for Item {i}")}
            for i in range(5)
        ]

        with self.canvas.before:
            Color(1, 1, 1, 0)  
            self.border = RoundedRectangle(pos=self.pos, size=self.size, radius=[9])
            Color(0, 0, 0, .0)  
            self.rect = RoundedRectangle(
                pos=(self.pos[0] + 1, self.pos[1] + 1),
                size=(self.size[0] - 2, self.size[1] - 2),
                radius=[8],
            )
        self.bind(pos=self.update_rect, size=self.update_rect)
        
        self.menu_button_icon = MDButtonIcon(
                icon='menu',
                theme_font_size = 'Custom',
                font_size = '26sp',
                theme_icon_color = 'Custom',
                icon_color = 'white', 
                
            )
        self.menu_button = MDButton(
            self.menu_button_icon,
            style='outlined',
            size_hint_x = .2,
            pos_hint = {'center_y': .5},
            theme_line_color = 'Custom',
            line_color = (0,0,0,0),
            theme_bg_color = 'Custom',
            md_bg_color = (0,0,0,0),
            on_release = self.menu_open
        )
        self.add_widget(self.menu_button)

        self.title = MDLabel(
            text = title_name,
            size_hint_x = .6,
            halign='center', 
            pos_hint = {'center_y': 0.4},
            font_style = 'Headline',
            text_color = 'white',
            role = 'medium'
        )
        self.add_widget(self.title)

        self.lock_button = MDButton(
            MDButtonIcon(
                icon='lock',
                theme_font_size = 'Custom',
                font_size = '26sp',
                theme_icon_color = 'Custom',
                icon_color = 'white'
            ),
            style='outlined',
            size_hint_x = .2,
            pos_hint = {'center_y': .5},
            theme_line_color = 'Custom',
            line_color = (0,0,0,0),
            theme_bg_color = 'Custom',
            md_bg_color = (0,0,0,0),
        )
        self.add_widget(self.lock_button)

    def update_rect(self, *args):
            self.border.pos = self.pos
            self.border.size = self.size
            self.rect.pos = (self.pos[0] + 1, self.pos[1] + 1)
            self.rect.size = (self.size[0] - 2, self.size[1] - 2)
    
    def menu_open(self, instance, menu_background_color=(.2,.2,.3,1)):
        menu_items = [
            {
                "text": item["text"],
                "on_release": item["callback"],
            } for item in self.menu_items
        ]
        self.menu = MDDropdownMenu(
            caller=instance, 
            items=menu_items,
            width_mult=4,
            background_color=menu_background_color
        )
        self.menu.open()
        
    def menu_callback(self, text_item):
        print(f"Selected: {text_item}")