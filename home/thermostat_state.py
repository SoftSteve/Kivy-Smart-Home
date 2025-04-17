import json

import json

class ThermostatStore:
    def __init__(self, filename="states/thermostat_states.json"):
        self.filename = filename
        self.active = {}
        self.states = {}
        self.temperature = {}
        self.load_state()  

    def load_state(self):
        try:
            with open(self.filename, "r") as file:
                data = json.load(file)
                self.states = data.get("states", {})
                self.active = data.get("active", {})
                self.thermostat = data.get("temperature", {})
        except (FileNotFoundError, json.JSONDecodeError):
            self.states = {}
            self.active = {}
            self.thermostat = {}

    def save_state(self):
        data = {
            "states": self.states,
            "active": self.active,
            "temperature": self.temperature,
        }
        with open(self.filename, "w") as file:
            json.dump(data, file, indent=4)

    def update_state(self, button_id, state):
        self.states[button_id] = state  
        self.save_state()

    def get_state(self, button_id):
        return self.states.get(button_id, False)

    def get_all_states(self):
        return self.states

    def update_active_content(self, current_content, state):
        self.active[current_content] = state
        self.save_state()

    def get_active_content(self, current_content):
        return self.active.get(current_content, False)
    
    def get_all_content(self):
        return self.active
     
    def update_temperature(self, thermostat_id, digit):
        self.temperature[thermostat_id] = digit
        self.save_state()

    def get_temperature(self, temperature,):
        return self.temperature.get(temperature, 69)
        

