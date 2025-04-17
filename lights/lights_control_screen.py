from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView

from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.divider import MDDivider
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.dialog import (
    MDDialog, MDDialogHeadlineText, MDDialogSupportingText, MDDialogContentContainer,
    MDDialogButtonContainer, MDDialogIcon
)
from kivymd.uix.textfield import MDTextField
from kivymd.uix.list import MDListItem, MDListItemLeadingIcon, MDListItemSupportingText, MDListItemTrailingCheckbox
from kivymd.uix.boxlayout import MDBoxLayout

from custom_ui.custom_app_bar import AppBar
from  custom_ui.custom_graph import LightEnergyGraph 
from lights.custom_light_button import CustomButton  
from lights.more_option import MoreOptions
from custom_ui.customgradient import CustomGradient


class LightsControlPanel(Widget):
    def __init__(self, store, **kwargs):
        super().__init__(**kwargs)
        
        self.store = store
        self.buttons = {}
    
        self.initial_names = []
        self.edit_delete_name = []
        
        self.main_container = FloatLayout(size_hint=(1, 1))
        self.add_widget(self.main_container)
    
        self.scroll_view = ScrollView(
            size_hint=(None, None), 
            size=(.45, .8), 
            pos_hint={'center_x':.275, 'center_y':.425},
            bar_pos_y='left',
            bar_width=5,
            bar_margin=-10,

        )
        self.main_container.add_widget(self.scroll_view)

        self.button_container = GridLayout(
            spacing=15, 
            padding=5,
            cols=1,
            size_hint_y=None,
            size_hint_x=1,
            pos_hint = {'center_x':.1},
            height=self.height,
        )
        self.scroll_view.add_widget(self.button_container)
        self.button_container.bind(minimum_height=self.button_container.setter('height'))
        
        self.app_bar = AppBar(
            title_name='Lights',
            menu_items=[
                {"text": f"Edit Names", "callback": self.callback_edit},
                {"text": f"Delete", "callback": self.callback_delete},
                {"text": f"Add Devices", "callback": self.callback_add},
            ],
            
        )
        self.main_container.add_widget(self.app_bar)

        self.title_divider = MDDivider(orientation='horizontal', size_hint_x = .9, pos_hint={'center_x':.5, 'center_y':.85})
        self.main_container.add_widget(self.title_divider)

        self.energy_graph = LightEnergyGraph(pos_hint={'center_x':.7, 'center_y':.575})
        self.main_container.add_widget(self.energy_graph)

        
        self.more_options = MoreOptions(pos_hint={'center_x':.7, 'center_y':.175}, store=self.store)
        self.main_container.add_widget(self.more_options)
        
        CustomGradient.enable_gradient(self, (0.43, 0.54, 0.68754, 0.2), (.85, .85, .9, .3), radius=9)

        with open('find/names.txt', 'r') as file:
            for line in file:
                stripped_line = line.strip()
                if stripped_line: 
                    words = stripped_line.split() 
                    self.initial_names.append(" ".join(words[:2]))

    
    def initialize_add_dialog(self, *args):
        if not hasattr(self, 'dialog') or self.dialog is None:
            device_items = []
            
            # Create list items
            for i, self.name in enumerate(self.initial_names):
                device_item = MDListItem(
                    MDListItemLeadingIcon(icon="plus"),
                    MDListItemSupportingText(id=f'text{i+1}', text=self.name),
                    MDListItemTrailingCheckbox(
                        id=f'uniqueID{i+1}',
                        active=False,
                        color_active="blue",
                    ),
                    size_hint_y=None,
                    theme_bg_color="Custom",
                    md_bg_color=(1, 1, 1, 1),
                    theme_line_color='Custom',
                    line_color='grey'
                )
                device_items.append(device_item)

            scrollable_container = MDScrollView(
                MDBoxLayout(
                    *device_items,
                    orientation="vertical",
                    adaptive_height = True,
                    size_hint_y=None,
                    height=(len(self.edit_delete_name) * 56),  
                ),
                size_hint_y=None,
                height=device_item.height * 2  
            )

            self.dialog = MDDialog(
                MDDialogHeadlineText(text="Searching.."),
                MDDialogSupportingText(
                    text="Searching for new devices to quickly add them to your smart hub control panel"
                ),
                MDDialogContentContainer(
                    MDDivider(),
                    scrollable_container,
                    MDDivider(),
                    orientation="vertical",
                    padding="8dp",
                    spacing="8dp"
                ),
                MDDialogButtonContainer(
                    Widget(),
                    MDButton(
                        MDButtonText(text="Cancel"),
                        style="text",
                        on_release=self.dismiss_menus
                    ),
                    MDButton(
                        MDButtonText(text="Accept"),
                        style="text",
                        on_release=self.create_button,
                    ),
                    spacing="8dp",
                ),
                auto_dismiss=False,
                size_hint=(0.6, .4),
            )
            self.dialog.open()

    
    def initialize_delete_dialog(self, *args):
        if not hasattr(self, 'delete_dialog') or self.delete_dialog is None:

            device_items = []
            
            for i, self.name in enumerate(self.edit_delete_name):
                    device_item = MDListItem(
                        MDListItemLeadingIcon(icon="plus"),
                        MDListItemSupportingText(id=f'text{i+1}', text=self.name),
                        MDListItemTrailingCheckbox(
                            id=f'uniqueID{i+1}',
                            active=False,
                            color_active="blue",
                        ),
                        theme_bg_color="Custom",
                        md_bg_color=(1, 1, 1, 1),
                        theme_line_color='Custom',
                        line_color='grey'
                    )
                    device_items.append(device_item)

            scrollable_container = MDScrollView(
                MDBoxLayout(
                    *device_items,
                    orientation="vertical",
                    adaptive_height = True,
                    size_hint_y=None,
                    height=(len(self.edit_delete_name) * 56),  
                ),
                size_hint_y=None,
                height=device_item.height * 2  
            )
            self.delete_dialog = MDDialog(
                MDDialogIcon(icon="lightbulb"),
                MDDialogHeadlineText(text="Searching.."),
                MDDialogSupportingText(
                    text="Devices you can delete will display here. Select the devices you want to delete and press Accept."
                ),
                MDDialogContentContainer(
                    MDDivider(),
                    scrollable_container, 
                    MDDivider(),
                    orientation="vertical",
                ),
                MDDialogButtonContainer(
                    Widget(),
                    MDButton(
                        MDButtonText(text="Cancel"),
                        style="text",
                        on_release=self.dismiss_menus
                    ),
                    MDButton(
                        MDButtonText(text="Accept"),
                        style="text",
                        on_release=self.delete_button,
                    ),
                    spacing="8dp",
                ),
                auto_dismiss=False,
                size_hint=(0.6, .4)
            )
            self.delete_dialog.open()


    def initialize_edit_dialog(self, *args):
        if not hasattr(self, 'edit_dialog') or self.edit_dialog is None:
            
            device_items = []
            
            for i, self.name in enumerate(self.edit_delete_name):
                device_item = MDListItem(
                    MDListItemLeadingIcon(icon="plus"),
                    MDListItemSupportingText(id=f'text{i+1}', text=self.name),
                    MDListItemTrailingCheckbox(
                        id=f'uniqueID{i+1}',
                        active=False,
                        color_active="blue",
                    ),
                    theme_bg_color="Custom",
                    md_bg_color=(1, 1, 1, 1),
                    theme_line_color='Custom',
                    line_color='grey'
                )
                device_items.append(device_item)

            scrollable_container = MDScrollView(
                MDBoxLayout(
                    *device_items,
                    orientation="vertical",
                    adaptive_height = True,
                    size_hint_y=None,
                    height=(len(self.edit_delete_name) * 56),  
                ),
                size_hint_y=None,
                height=device_item.height * 2  
            )
            
            self.edit_dialog = MDDialog(
                MDDialogIcon(icon="lightbulb"),
                MDDialogHeadlineText(text="Searching.."),
                MDDialogSupportingText(
                    text="Searching for new devices to quickly add them to your smart hub control panel"
                ),
                MDDialogContentContainer(
                    MDDivider(),
                    scrollable_container,  # Add all device items here
                    MDDivider(),
                    orientation="vertical",
                ),
                MDDialogButtonContainer(
                    Widget(),
                    MDButton(
                        MDButtonText(text="Cancel"),
                        style="text",
                        on_release=self.dismiss_menus
                    ),
                    MDButton(
                        MDButtonText(text="Accept"),
                        style="text",
                        on_release=self.edit_button_dialog,
                    ),
                    spacing="8dp",
                ),
                ripple_behavior = False,
                scrim_color = (0,0,0,1),
                auto_dismiss=False,
                size_hint=(0.6, None)
            )
            self.edit_dialog.open()

    
    def initialize_edit_name(self, *args):

        
        self.name_dialog = MDDialog(
                    MDDialogHeadlineText(text="Edit Device Name"),
                    MDDialogSupportingText(
                        text=f"Edit the name of the device:{self.key_to_edit}"
                    ),
                    MDDialogContentContainer(
                        MDTextField(
                            id="edit_textfield",
                            hint_text="Enter new device name",
                            text=self.key_to_edit,
                            size_hint=(1, None),
                            height="48dp",
                        )
                    ),
                    MDDialogButtonContainer(
                        Widget(),
                        MDButton(
                            MDButtonText(text="Cancel"),
                            style="text",
                            on_release=self.dismiss_menus,
                        ),
                        MDButton(
                            MDButtonText(text="Save"),
                            style="text",
                            on_release=self.save_edited_name
                        ),
                        spacing="8dp",
                    ),
                )
        self.name_dialog.open()
        

    def callback_edit(self, *args):
        print(f"Editing device:")

        self.initialize_edit_dialog()
        self.explore_extract_map()


    def callback_delete(self, *args):
        print(f"Deleting device: ")
        
        self.initialize_delete_dialog()
        self.explore_extract_map()


    def callback_add(self, *args):
        print(f"Adding device: ")

        self.initialize_add_dialog()
        self.explore_extract_map()

 
    def explore_extract_map(self, *args):
        # lists of extracted children
        self.device_names = [] 
        self.device_checkbox = []
        self.checkbox_states = []
        self.mapped_devices = []

        # extracts supporting text and store in devices names
        def extract_text(widget, depth = 0):
            for child in widget.children:
                extract_text(child, depth + 1)

                if isinstance(child, MDListItemSupportingText):
                    self.device_names.append(child.text)

        # extracts checkbox id and active state and stores them in their respective lists.
        def extract_checkbox(widget, depth=0):
            for child in widget.children:
                extract_checkbox(child, depth + 1)

                if isinstance(child, MDListItemTrailingCheckbox):
                    self.device_checkbox.append(child.id)
                    self.checkbox_states.append(child.active)
                    

                    #bind self.on_checkbox_active to child on active
                    child.bind(active=self.on_checkbox_active)
        
        # creates a list of dialogs
        dialogs = [getattr(self, dialog_attr) for dialog_attr in ['dialog', 'delete_dialog', 'edit_dialog'] if hasattr(self, dialog_attr) and getattr(self, dialog_attr)]
    
        # function called to explore and extract text(name), id(unique identifier), and active state(set to False)
        for dialog in dialogs:
            extract_text(dialog)
            extract_checkbox(dialog)

        # using extracted data, maps data into a structured format by combining name, checkbox_id, and active state
        def map_devices():
            for name, checkbox_id, state in zip(self.device_names, self.device_checkbox, self.checkbox_states):
                self.mapped_devices.append({"name": name, "checkbox_id": checkbox_id, "active": state})

        map_devices() 
            
   
    def on_checkbox_active(self, checkbox, value):
        self.active_devices = []
        for device in self.mapped_devices:
            if device["checkbox_id"] == checkbox.id:
                device["active"] = value
            if device['active']:
                self.active_devices.append(device['name'])
            else:
                pass
                    
        print(f'Active Devices:{self.active_devices}')


    def create_button(self, *args):
        self.button_container.clear_widgets()

        for device in self.mapped_devices:
            if device["active"] and device["checkbox_id"] not in self.buttons:
                device_name = device['name']
                device_id = device['checkbox_id']

                previous_state = self.store.get_state(device_id).get("state", False)
                last_brightness = self.store.get_state(device_id).get("last_brightness", 0.8)

                new_button = CustomButton(
                    text=device_name, 
                    id=device_id,
                    state=previous_state,
                    last_brightness=last_brightness,
                    store=self.store,
                    on_press=self.update_button_state
                )
                self.button_container.add_widget(new_button)

                self.buttons[device_id] = new_button  
                self.store.update_state(device_id, device_name, previous_state, last_brightness)

        self.Refresh_UI()
        self.dismiss_menus(*args)


    def create_button(self, *args):
        for device in self.mapped_devices:
            device_id = device["checkbox_id"]

            if device["active"] and device_id not in self.buttons:
                device_name = device['name']
                previous_state = self.store.get_state(device_id).get("state", False)
                last_brightness = self.store.get_state(device_id).get("last_brightness", 0.8)

                new_button = CustomButton(
                    text=device_name, 
                    id=device_id,
                    state=previous_state,
                    last_brightness=last_brightness,
                    store=self.store,
                    on_press=self.update_button_state
                )
                self.button_container.add_widget(new_button)
                self.buttons[device_id] = new_button  
                self.store.update_state(device_id, device_name, previous_state, last_brightness)

        self.Refresh_UI()
        self.dismiss_menus(*args)


    def Refresh_UI(self, *args):
        current_devices = {device['checkbox_id']: device for device in self.store.get_all_devices()}
        dont_add = {'All-Lights', 'All-25', 'All-50', 'All-75'}

        for device_id, device in current_devices.items():
            if device_id in dont_add:
                continue

            device_name = device['name']
            saved_state = device['active']
            last_brightness = device.get("last_brightness", 0.8)

            if device_id in self.buttons:
                button = self.buttons[device_id]
                button.text = device_name
                button.switch_active = saved_state
                button.last_brightness = last_brightness
                button.initialize_dimmer_state()
                button.apply_theme()
            else:
                button = CustomButton(
                    text=device_name,
                    id=device_id,
                    state=saved_state,
                    last_brightness=last_brightness,
                    store=self.store,
                    on_press=self.update_button_state
                )
                self.button_container.add_widget(button)
                self.buttons[device_id] = button

            if device_name not in self.edit_delete_name:
                self.edit_delete_name.append(device_name)

        for device_id in list(self.buttons.keys()):
            if device_id not in current_devices and device_id not in dont_add:
                self.button_container.remove_widget(self.buttons[device_id])
                del self.buttons[device_id]


    def update_button_state(self, button):
        current_state = self.store.get_state(button.button_id).get("state", False)
        current_brightness = self.store.get_state(button.button_id).get("last_brightness", 0.8)
        current_color_temperature = self.store.get_state(button.button_id).get("last_color_temperature", 6500)

        new_state = not current_state

        self.store.update_state(button.button_id, button.text, new_state, current_brightness)

        
        button.switch_active = new_state
        button.apply_theme()


    def delete_button(self, *args):
        keys = []
        store_names = []
        self.dont_add = ['All-Lights', 'All-25', 'All-50', 'All-75']
        
        for name in self.active_devices:
            if name not in self.dont_add:
                keys.append(name)

        for device in self.store.get_all_devices():
            device_name = device.get("name")
            if device_name:
                store_names.append(device_name)
                if device_name not in self.edit_delete_name:
                    self.edit_delete_name.append(device_name)

        for key_to_delete in keys:
            if key_to_delete in store_names:
                self.store.delete_state_by_name(key_to_delete)
                self.edit_delete_name.remove(key_to_delete)

        self.Refresh_UI()
        self.delete_dialog.dismiss()
        self.delete_dialog = None
        self.app_bar.menu.dismiss()


    def edit_button_dialog(self, *args):
        self.edit_keys = list(self.active_devices) 
        self.dont_add = ['All-Lights', 'All-25', 'All-50', 'All-75']

        if not self.edit_keys:
            return  

        for key in self.edit_keys:
            if key in self.active_devices:
                self.key_to_edit = key
                self.initialize_edit_name()
                print('DIALOG OPENED')
                break  


    def save_edited_name(self, *args):
        text_strip = []

        def strip_text(widget, depth=0):
            for child in widget.children:
                strip_text(child, depth + 1)
                if isinstance(child, MDTextField):
                    text_strip.append(child.text)

        if hasattr(self, 'name_dialog') or self.name_dialog:
            strip_text(self.name_dialog)

        for name in text_strip:
            self.new_name = name

        updated = False
        button_id_to_update = None

        for button_id, data in self.store.states.items():
            print(f"Checking button_id: {button_id}, name: {data['name']}")
            if data["name"] == self.key_to_edit:
                button_id_to_update = button_id
                data["name"] = self.new_name
                updated = True
                break

        if updated:
            self.edit_delete_name.remove(self.key_to_edit)
            self.store.save_states()
            print(f"Updated store name: {self.key_to_edit} → {self.new_name}")

    
            self.button_container.clear_widgets()
            self.buttons.clear()
            self.Refresh_UI()

            self.dismiss_menus()
            self.name_dialog = None
            self.edit_dialog = None

    def dismiss_menus(self, *args):
       
        if hasattr(self, 'dialog') and self.dialog:
            self.dialog.dismiss()
            self.dialog = None
     
        if hasattr(self, 'edit_dialog') and self.edit_dialog:
            self.edit_dialog.dismiss()
            self.edit_dialog = None
     
        if hasattr(self, 'delete_dialog') and self.delete_dialog:
            self.delete_dialog.dismiss()
            self.delete_dialog = None
        
        if hasattr(self, 'name_dialog') and self.name_dialog:
            self.name_dialog.dismiss()
            self.name_dialog = None
       
        if hasattr(self, 'app_bar') and self.app_bar.menu:
            self.app_bar.menu.dismiss()


    def update_content_position(self, *args):
        self.main_container.size = (self.width, self.height)
        self.main_container.pos = self.pos

        self.scroll_view.size=(self.width * .45 ,self.height * .8)



class LightsControlScreen(FloatLayout):
    def __init__(self, store, **kwargs):
        super().__init__(**kwargs)
        self.store = store

        self.control_panel = LightsControlPanel(
            size_hint=(.75, 1),
            pos_hint = {'x': 0.225, 'y': 0.025},
            store = store
        )
        self.add_widget(self.control_panel)
    
        