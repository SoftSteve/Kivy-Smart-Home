import json
from kivy.app import App
from lights.custom_light_button import CustomButton

class ButtonStateStore:
    def __init__(self, filename="states/button_states.json"):
        self.filename = filename
        self.states = {}
        self.load_states()

    def load_states(self):
        try:
            with open(self.filename, "r") as file:
                self.states = json.load(file)
                
        except FileNotFoundError:
            self.states = {}

    def save_states(self):
        with open(self.filename, "w") as file:
            json.dump(self.states, file, indent=4)

    def update_state(self, button_id, name, switch_active, last_brightness):
        if not button_id or button_id == "Default Text":
            print(f"Skipping update: Invalid button_id ({button_id})")
            return
        
        if name != "Default Text" and switch_active is not None:
            self.states[button_id] = {
                "name": name,
                "state": switch_active,
                "last_brightness": last_brightness,
            }
            self.save_states()

    def update_button_state(self, name, new_state):
        for button_id, data in self.states.items():
            if data.get("name") == name:
                self.states[button_id]["state"] = new_state

                for widget in App.get_running_app().root.walk():
                    if isinstance(widget, CustomButton) and widget.text == name:
                        widget.switch_active = new_state 
                        widget.apply_theme()
                        widget.animate_dimmer(widget.last_brightness if new_state else 0.075) 
                        break

                return self.states[button_id]["state"]
        
        return None  # Name not found

    def update_button_brightness(self, name, new_brightness):
        for button_id, data in self.states.items():
            if data.get('name') == name:
                self.states[button_id]['last_brightness'] = new_brightness

                for widget in App.get_running_app().root.walk():
                    if isinstance(widget, CustomButton) and widget.text == name:
                        widget.last_brightness = new_brightness
                        widget.apply_theme
                        widget.animate_dimmer(new_brightness if widget.switch_active else 0.075)
                        break
                return self.states[button_id]['last_brightness']
        return None

    def get_state(self, button_id):
        return self.states.get(button_id, {"state": False})
    
    def get_therm_states(self, id):
        return self.states.get(id, {'state': False})
    
    def get_active_devices(self):
        return [
            {"checkbox_id": button_id, "name": device["name"], "active": device["state"], "last_brightness": device.get("last_brightness", 0.8)} 
                for button_id, device in self.states.items()
                if device.get('state', False)
        ]
    
    def get_all_devices(self):
        devices = []
        seen_ids = set()

        for button_id, device in self.states.items():
            if button_id not in seen_ids:
                devices.append({
                    "checkbox_id": button_id,
                    "name": device["name"],
                    "active": device["state"],
                    "last_brightness": device.get("last_brightness", 0.8),
                })
                seen_ids.add(button_id)  # Track seen IDs

        return devices
    
    def delete_state_by_name(self, name):
        button_id_to_delete = None
        for button_id, device in self.states.items():
            if device["name"] == name:
                button_id_to_delete = button_id
                break

        if button_id_to_delete:
            del self.states[button_id_to_delete] 
            self.save_states() 
            print(f"Button with name '{name}' and checkbox_id '{button_id_to_delete}' has been deleted.")
        else:
            print(f"No button found with name '{name}'")