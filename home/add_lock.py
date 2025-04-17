from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton, MDButton, MDButtonText
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import MDListItem, MDListItemLeadingIcon, MDListItemSupportingText, MDListItemTrailingCheckbox
from kivymd.uix.divider import MDDivider
from kivymd.uix.dialog import MDDialogHeadlineText, MDDialogSupportingText, MDDialogContentContainer, MDDialogButtonContainer


class AddLockScreen(FloatLayout):
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
            text = 'Add Lock',
            theme_text_color = 'Custom',
            text_color = (0.9, 0.9, 0.9, .8),
            size_hint = (1,1),
            font_size = self.width * 0.03,
            pos_hint = {'center_x':.5, 'center_y': .7},
            halign = 'center'
        )
        self.add_widget(self.add_device_lbl)
        self.bind(size=self.update_label)

        self.plus_icon = MDIconButton(
            icon = 'home-plus', 
            style = 'outlined',
            theme_icon_color = 'Custom',
            icon_color = (0.9, 0.9, 0.9, .8),
            size_hint = (None, None),
            width = self.width * 0.2,
            height = self.height * 0.2,
            font_size = self.width * 0.075,
            pos_hint = {'center_x':.5, 'center_y':.35},
            on_press = self.callback
        )
        self.add_widget(self.plus_icon)
    
    def update_label(self, *args):
        self.add_device_lbl.font_size = self.width * 0.07
        self.plus_icon.width = self.width * 0.15
        self.plus_icon.height = self.width * 0.15
        self.plus_icon.font_size = self.width * 0.1
        self.plus_icon.halign = 'center'


class InitializePopup(MDDialog):
    def __init__(self, *args, callback_accept, callback_cancel, **kwargs):
        super().__init__(*args, **kwargs)
        self.padding = 10
        self.callback_cancel = callback_cancel
        self.callback_accept = callback_accept
        self.auto_dismiss = False

    
        # -----------------------Headline text-------------------------
        self.add_widget(MDDialogHeadlineText(
            text="Select Lock",
        )),
        # -----------------------Supporting text-----------------------
        self.add_widget(MDDialogSupportingText(
            text="Select a lock to add to your home.",
        )),
        # -----------------------Custom content------------------------
        self.add_widget(MDDialogContentContainer(
            MDDivider(),
            MDListItem(
                MDListItemLeadingIcon(
                    icon="door-closed-lock",
                ),
                MDListItemSupportingText(
                    text="Smart Lockv2.3",
                ),
                MDListItemTrailingCheckbox(

                ),
                theme_bg_color="Custom",
            ),
            MDListItem(
                MDListItemLeadingIcon(
                    icon="door-closed-lock",
                ),
                MDListItemSupportingText(
                    text="Google Nest Lock 2.0.1",
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