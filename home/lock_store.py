import json

class LockStore:
    def __init__(self, filename="states/lock_state.json"):
        self.file_name = filename
        self.state = {}
        self.active = {}
        self.load_state()
        
    def load_state(self):
        try:
            with open(self.file_name, 'r') as file:
                data = json.load(file)
                self.state = data.get("state", {})
                self.active = data.get("active", {})
        except (FileNotFoundError, json.JSONDecodeError):
            self.state = {}
            self.active = {}

    def save_state(self):
        data = {
            "states": self.state,
            "active": self.active,
        }
        with open(self.file_name, "w") as file:
            json.dump(data, file, indent=4)

    def update_lock_states(self, state):
        if state is not None:
            self.state['state'] = state  # Updates only the 'state' key
            self.save_state()

    def get_state(self, state):
        return self.state.get(state, {})  # Return empty dict if key doesn't exist
    
    def update_active_content(self, current_content, state):
        self.active[current_content] = state
        self.save_state()

    def get_active_content(self, current_content):
        return self.active.get(current_content, False)

