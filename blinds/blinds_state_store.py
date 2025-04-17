import os
import json
from kivy.app import App
from .custom_blind_buttons import CustomBlindButton

class BlindsStateStore():
    __events__ = ('on_state_update',)
    FILE_PATH = "states/blind_states.json"

    def __init__(self):
        self.states = {}
        self.load_states()

    def load_states(self):
        if os.path.exists(self.FILE_PATH):
            with open(self.FILE_PATH, 'r') as file:
                self.states = json.load(file)
        else:
            self.states = {}

    def save_states(self):
        with open(self.FILE_PATH, 'w') as file:
            json.dump(self.states, file, indent=4)

    def update_states(self, button_id, text, switch_active, blinds_start):
        if not button_id or button_id == 'Default Text':
            return
        
        if switch_active is not None:
            self.states[button_id] = {
                "name": text,
                "state": switch_active,
                "blinds_start": blinds_start
            }
            self.save_states()

    def on_state_update(self, *args):
        pass

    def get_all_devices(self):
        devices = []
        seen_ids = set()

        for button_id, device in self.states.items():
            if button_id not in seen_ids:
                devices.append({
                    "button_id": button_id,
                    "name": device["name"],
                    "state": device["state"],
                    "blinds_start": device["blinds_start"]
                })
                seen_ids.add(button_id)

        return devices

    def get_button_state(self, button_id):
        return self.states.get(button_id, {"state": False}) 
    
    def update_button_state(self, button_id, new_state):
        if button_id in self.states:
            self.states[button_id]["state"] = new_state

            # Update UI
            app = App.get_running_app()
            if app and app.root:
                for widget in app.root.walk():
                    if isinstance(widget, CustomBlindButton) and widget.button_id == button_id:
                        widget.switch_active = new_state
                        widget.apply_theme()
                        widget.animate_dimmer(widget.blinds_start if new_state else 0.075)

            return self.states[button_id]["state"]
        return None  # Button not found
    
    def update_button_blinds(self, button_id, new_blinds):
        if button_id in self.states:
            self.states[button_id]['blinds_start'] = new_blinds

            app = App.get_running_app()
            if app and app.root:
                for widget in app.root.walk():
                    if isinstance(widget, CustomBlindButton) and widget.button_id == button_id:
                        widget.switch_active = widget.state
                        widget.apply_theme()
                        widget.animate_dimmer(new_blinds if widget.switch_active else 0.075)
                                  