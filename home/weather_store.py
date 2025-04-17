import json

class WeatherStore:
    def __init__(self, filename="states/weather_state.json"):
        self.file_name = filename
        self.active = {}
        self.city = {}
        self.load_state()
        
    def load_state(self):
        try:
            with open(self.file_name, 'r') as file:
                data = json.load(file)
                self.active = data.get("active", {})
                self.city = data.get("city", {})
        except (FileNotFoundError, json.JSONDecodeError):
            self.active = {}
            self.city = {}

    def save_state(self):
        data = {
            "active": self.active,
            "city": self.city
        }
        with open(self.file_name, "w") as file:
            json.dump(data, file, indent=4)
    
    def update_active_content(self, current_content, state):
        self.active[current_content] = state
        self.save_state()

    def get_active_content(self, current_content):
        return self.active.get(current_content, False)

    def update_city(self, zip_input, digit):
        self.city[zip_input] = digit
        self.save_state()
    
    def get_city(self, zip_input):
        return self.city.get(zip_input, 00000)
