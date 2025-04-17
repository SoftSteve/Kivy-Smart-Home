from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.button import MDIconButton
from kivy.graphics import Color, RoundedRectangle
from kivy.clock import Clock


class DimSwiper(FloatLayout):
    def __init__(self, parent, **kwargs):
        super().__init__(**kwargs)
        self.parent_widget = parent

        self.is_animating = False  
        self.is_updating = False

        self.track_start = 0  
        self.track_end = 1 
        self.light_start_value = 0  
        self.light_end_value = 255  
        self.border_color = (0,0,0,1)

        self.initial_swipe_position = self.parent_widget.last_brightness  
        self.swipe_progress = self.initial_swipe_position  

        self.size_hint = (1,1)
        self.pos_hint = {'center_x': .5, 'center_y': .5}

        with self.canvas.before:
            self.swipe_color = Color(1, 1, 1, 1)  
            self.swipe_track = RoundedRectangle(size=(self.width * self.swipe_progress, self.height * 98), pos=self.pos, radius=[15])

        self.bind(size=self.update_track, pos=self.update_track)

        self.thumb = MDIconButton(
            icon='lightbulb-night',
            style='filled',
            theme_bg_color='Custom',
            md_bg_color=(.95, .95, 1, 1),
            theme_icon_color='Custom',
            icon_color=(.227, .274, .862, .5),
            size_hint=(None, None), 
            ripple_effect = False
        )
        self.thumb.size = (36, 36)  
        self.add_widget(self.thumb)

        self.update_swipe_track(self.swipe_progress) 
        self.update_thumb(self.swipe_progress)
    

    def on_touch_move(self, touch):
        if self.is_animating:
            return  

        if self.collide_point(*touch.pos):
            self.is_updating = True
            touch_position = touch.pos[0]
            swipe_progress = (touch_position - self.pos[0]) / self.width
            swipe_progress = max(.075, min(.95, swipe_progress))

            light_value = self.light_start_value + (swipe_progress * (self.light_end_value - self.light_start_value))

            self.update_swipe_track(swipe_progress)
            self.update_thumb(swipe_progress)

            self.parent_widget.last_brightness = swipe_progress

            if self.is_updating == True:
                Clock.schedule_once(lambda *args: self.update_store(swipe_progress), .1)

    def update_swipe_track(self, swipe_progress):
        self.swipe_progress = swipe_progress
        self.swipe_track.size = (self.width * swipe_progress, self.height * 1)
        self.swipe_track.pos = self.pos

        r = max(0.1, 1 - swipe_progress * 0.3)
        g = max(0.1, 1 - swipe_progress * 0.3)
        b = min(1, 1 + swipe_progress * 1)
        alpha = 0.1 + (swipe_progress * 0.9)

        self.swipe_color.rgba = (r, g, b, alpha)

    def update_track(self, *args):
        self.swipe_track.size = (self.width * self.swipe_progress, self.height * 1)
        self.swipe_track.pos = self.pos
        self.update_thumb(self.swipe_progress)

    def update_thumb(self, swipe_progress):
        self.thumb.pos = (
            self.pos[0] - 5 + (self.width * swipe_progress) - (self.thumb.width / 2),
            self.pos[1] + (self.height / 2) - (self.thumb.height / 2)
        )
    
    def update_store(self, swipe_progress, *args):
        self.parent_widget.store.update_state(
            self.parent_widget.button_id,
            self.parent_widget.text,
            self.parent_widget.switch_active,
            swipe_progress,
        )
