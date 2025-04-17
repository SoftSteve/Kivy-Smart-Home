from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Rectangle, Color, RoundedRectangle
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.animation import Animation
from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.button import MDFabButton, MDIconButton

class SwipeTrack(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.size_hint = (.5, .5)
        
        self.touch_started = False
        self.target_position = 0
        self.track_width = 0
        self.track_height = 0
        
        self.create_swipe_track()

        self.bind(size=self.on_size)

    def create_swipe_track(self):
        self.track = FloatLayout(
            size_hint=(None, None), 
            size=(self.track_width, 
            self.track_height), 
            pos=(self.width * 0.1, self.height * 0.45)
        )

        with self.track.canvas.before:
            Color(0.2, 0.2, 0.2, 1) 
            self.track_rect = RoundedRectangle(pos=self.track.pos, size=self.track.size, radius=[20])
        
        self.add_widget(self.track)

        self.swipe_button = MDIconButton(
            icon='lock', 
            style='filled', 
            font_size='12sp',
            size_hint=(None, None), 
            size=(.1 * self.width, .5 * self.track_height), 
            ripple_effect = False
        )
        self.swipe_button.font_size = '16sp'
        
        self.swipe_button.pos = (self.track.pos[0], self.track.pos[1] + self.track.height / 9)
        
        self.track.add_widget(self.swipe_button)

        self.swipe_button.bind(on_touch_move=self.on_swipe)
        self.swipe_button.bind(on_touch_up=self.on_swipe_end)
        self.swipe_button.bind(on_touch_down=self.on_touch_start)
    
    def on_size(self, instance, value):
        self.track_width = self.width * 0.5  
        self.track_height = self.height * 0.1  
        self.target_position = self.track_width
        
        self.track.size = (self.track_width, self.track_height)
        self.track.pos = (self.width * 0.1, self.height * 0.4) 
        
        self.swipe_button.size = (.13 * self.track_width, .8 * self.track_height) 
        self.swipe_button.pos = (self.track.pos[0] + 5, self.track.pos[1] + self.track.height / 9)

        self.track_rect.pos = self.track.pos
        self.track_rect.size = self.track.size

    def on_touch_start(self, instance, touch):
        if instance.collide_point(*touch.pos):
            self.touch_started = True

    def on_swipe(self, instance, touch):
        if self.touch_started:
            new_x = touch.x - instance.width / 2  
            
            track_left_bound = self.track.pos[0]
            track_right_bound = self.track.pos[0] + self.track_width
            if track_left_bound <= new_x <= track_right_bound - instance.width:
                instance.x = new_x

            if new_x >= (self.target_position * 0.4):
                self.auto_slide_to_end(instance)

    def on_swipe_end(self, instance, touch):
        if self.touch_started:
            if instance.x >= self.target_position:
                self.trigger_function()
        
        self.touch_started = False
    
    def auto_slide_to_end(self, instance):
        end_position = self.track.pos[0] + self.track_width - 5 - instance.width
        anim = Animation(x=end_position, duration=0.3)  
        anim.bind(on_complete=self.reset_button_position_delay)  
        anim.start(instance)

    def reset_button_position_delay(self, *args):
        Clock.schedule_once(self.reset_button_position, 0.15)

    def reset_button_position(self, *args):
        """Reset the button's position after the animation is complete."""
        anim = Animation(x=self.track.pos[0]+ 5, duration=0.3) 
        anim.start(self.swipe_button)

    def trigger_function(self):
        """Action to trigger after swipe reaches the target."""
        print("Button swiped to the target position! Action triggered.")

class SwipeApp(MDApp):
    def build(self):
        return SwipeTrack()

if __name__ == "__main__":
    SwipeApp().run()
