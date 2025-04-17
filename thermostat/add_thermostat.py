from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton, MDButton, MDButtonText
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import MDListItem, MDListItemLeadingIcon, MDListItemSupportingText, MDListItemTrailingCheckbox
from kivymd.uix.divider import MDDivider
from kivymd.uix.dialog import MDDialogHeadlineText, MDDialogSupportingText, MDDialogContentContainer, MDDialogButtonContainer


class AddThermostatScreen(FloatLayout):
    content_id = StringProperty('Initial')
    current_content = BooleanProperty(True)

    def __init__(self, content_id, callback, current_content, **kwargs):
        super().__init__(**kwargs)

        self.size_hint = (1,1)
        self.pos_hint = {'center_x':.5, 'center_y':.5}
        self.content_id = content_id
        self.current_content = current_content
        self.callback = callback

        self.add_device_lbl = MDLabel(
            text = 'Press to add a device',
            theme_text_color = 'Custom',
            text_color = (0.9, 0.9, 0.9, .8),
            size_hint = (1,1),
            font_size = self.width * 0.03,
            pos_hint = {'center_x':.5, 'center_y': .55},
            halign = 'center'
        )
        self.add_widget(self.add_device_lbl)
        self.bind(size=self.update_label)

        plus_icon = MDIconButton(
            icon = 'plus-circle-outline', 
            style = 'outlined',
            theme_icon_color = 'Custom',
            icon_color = (0.9, 0.9, 0.9, .8),
            pos_hint = {'center_x':.5, 'center_y':.4},
            on_press = self.callback
        )
        self.add_widget(plus_icon)
    
    def update_label(self, *args):
        self.add_device_lbl.font_size = self.width * 0.03


class InitializePopup(MDDialog):
    def __init__(self, *args, callback_accept, callback_cancel, **kwargs):
        super().__init__(*args, **kwargs)
        self.padding = 10
        self.callback_cancel = callback_cancel
        self.callback_accept = callback_accept
        self.auto_dismiss = False

    
        # -----------------------Headline text-------------------------
        self.add_widget(MDDialogHeadlineText(
            text="Select Thermostat",
        )),
        # -----------------------Supporting text-----------------------
        self.add_widget(MDDialogSupportingText(
            text="Select a thermostat to add to your home.",
        )),
        # -----------------------Custom content------------------------
        self.add_widget(MDDialogContentContainer(
            MDDivider(),
            MDListItem(
                MDListItemLeadingIcon(
                    icon="home-thermometer-outline",
                ),
                MDListItemSupportingText(
                    text="Amazon Smart Thermostat",
                ),
                MDListItemTrailingCheckbox(

                ),
                theme_bg_color="Custom",
            ),
            MDListItem(
                MDListItemLeadingIcon(
                    icon="home-thermometer-outline",
                ),
                MDListItemSupportingText(
                    text="Google Nest Thermostatv2.3",
                ),
                MDListItemTrailingCheckbox(

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