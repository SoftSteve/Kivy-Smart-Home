from kivymd.uix.dialog import MDDialog, MDDialogButtonContainer, MDDialogHeadlineText, MDDialogIcon, MDDialogContentContainer
from kivymd.uix.list import MDListItem, MDListItemSupportingText, MDListItemLeadingIcon, MDListItemTrailingCheckbox
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.divider import MDDivider
from kivymd.uix.card import MDCard
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.widget import Widget

from kivy.uix.scrollview import ScrollView 
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.metrics import dp

from bleak import BleakScanner
import asyncio
import logging

from custom_ui.customgradient import CustomGradient


logging.getLogger("bleak").setLevel(logging.WARNING)

async def discover_bluetooth_devices(callback):
    print("Scanning for Bluetooth devices...")
    scanner = BleakScanner()
    
    def detection_callback(device, advertisement_data):
        device_name = device.name
        if device_name and device_name.strip(): 
            Clock.schedule_once(lambda dt: callback(device_name, device.address), 0)
    
    scanner.register_detection_callback(detection_callback)
    await scanner.start()
    await asyncio.sleep(20.0)
    await scanner.stop()
    print("Scan complete")


class BluetoothPop(MDDialog):
    def __init__(self, *args, callback_cancel, callback_accept, **kwargs):
        super().__init__(*args, **kwargs)
        self.auto_dismiss = False
        self.padding = 10

        self.callback_cancel = callback_cancel
        self.callback_accept = callback_accept

        self.bluetooth_devices = {}  
        self.item_count = 0  

        self.item_height = dp(56)

        self.scrollable_container = ScrollView(
            size_hint_y=None,
        )
        
        self.item_container = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height = self.item_height * 2
        )
        self.item_container.bind(minimum_height = self.item_container.setter('height'))
        self.scrollable_container.add_widget(self.item_container)

        self.add_widget(MDDialogHeadlineText(text="Select Bluetooth Device"))
        self.add_widget(MDDialogIcon(icon='bluetooth'))
        self.add_widget(MDDialogContentContainer(
            MDDivider(),
            self.scrollable_container,
            MDDivider(),
            orientation="vertical",
        ))
        self.add_widget(MDDialogButtonContainer(
            Widget(),
            MDButton(
                MDButtonText(text="Cancel"),
                style="text",
                on_press=self.callback_cancel
            ),
            MDButton(
                MDButtonText(text="Accept"),
                style="text",
                on_press=self.callback_accept
            ),
            spacing="8dp",
        ))
        self.open()

    def add_device(self, name, address):
        if name not in self.bluetooth_devices:  
            self.item_count += 1
            device_item = MDListItem(
                MDListItemLeadingIcon(icon="bluetooth"),
                MDListItemSupportingText(id=f'text{self.item_count}', text=name),
                MDListItemTrailingCheckbox(
                    id=f'uniqueID{self.item_count}',
                    active=False,
                    color_active="blue",
                ),
                size_hint_y=None,
            )
            device_item.address = address
            self.bluetooth_devices[name] = address
            self.item_container.add_widget(device_item)

            self.item_container.height=self.item_height * 2

            self.scrollable_container.height = min(self.item_count * self.item_height, self.item_height * 2)

            device_item.theme_cls.theme_style = 'Dark'


class WifiPop(MDDialog):
    def __init__(self, *args, callback_cancel, callback_accept, **kwargs):
        super().__init__(*args, **kwargs)
        self.auto_dismiss = False
        self.padding = 10
        self.callback_cancel = callback_cancel
        self.callback_accept = callback_accept

    
        # -----------------------Headline text-------------------------
        self.add_widget(MDDialogHeadlineText(
            text="Select Wifi",
        )),
        #------------------------icon----------------------------------
        self.add_widget(MDDialogIcon(
            icon = 'wifi',
        ))
        # -----------------------Custom content------------------------
        self.add_widget(MDDialogContentContainer(
            MDDivider(),
            MDListItem(
                MDListItemLeadingIcon(
                    icon="wifi",
                ),
                MDListItemSupportingText(
                    text="staub",
                ),
                theme_bg_color="Custom",
            ),
            MDListItem(
                MDListItemLeadingIcon(
                    icon="wifi",
                ),
                MDListItemSupportingText(
                    text="itburnswhenIP",
                ),
                theme_bg_color="Custom",
            ),
            MDDivider(),
            orientation="vertical",
        )),
        # ---------------------Button container------------------------
        self.add_widget(MDDialogButtonContainer(
            Widget(),
            MDButton(
                MDButtonText(text="Cancel"),
                style="text",
                on_press = self.callback_cancel
            ),
            MDButton(
                MDButtonText(text="Accept"),
                style="text",
                on_press = self.callback_accept
            ),
            spacing="8dp",
        ))
        self.open()


class SoundPop(MDFloatLayout):
    def __init__(self, callback_accept, callback_cancel, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (.9, .6)
        self.pos_hint = {'center_x':.5, 'center_y':.5}
        self.callback_accept = callback_accept
        self.callback_cancel = callback_cancel

        CustomGradient.enable_gradient(self, ( 0.25,0.25,0.25,1), (0.2,0.2,0.2,1), radius=12, direction='vertical')

        button_container = BoxLayout(
            orientation = 'horizontal',
            spacing = 5,
            size_hint = (.2, .2),
            pos_hint = {'center_x':.7, 'center_y':.145}
        )
        self.add_widget(button_container)

        self.accept = MDButton(
                MDButtonText(text="Accept", theme_text_color='Custom', text_color = (0.82, 0.9, 0.99, 1)),
                style="text",
                on_press=self.callback_accept
        )
        self.cancel = MDButton(
                MDButtonText(text="Cancel",theme_text_color='Custom', text_color = (0.82, 0.9, 0.99, 1)),
                style="text",
                on_press=self.callback_cancel
        )

        button_container.add_widget(self.cancel)
        button_container.add_widget(self.accept)