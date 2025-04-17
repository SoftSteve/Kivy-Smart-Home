from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.button import MDIconButton
from kivy.graphics import Color, RoundedRectangle
from kivy.properties import BooleanProperty, NumericProperty
from kivy.uix.image import AsyncImage
from kivy.animation import Animation
from kivy.clock import Clock


class DimSwiper(FloatLayout):
    locked = BooleanProperty(False)
    lock_position = NumericProperty(0.075)
    def __init__(self, lock_store, parent, **kwargs):
        super().__init__(**kwargs)
        self.parent_widget = parent
        self.lock_store = lock_store

        self.is_animating = False  
        self.is_updating = False

        self.track_start = 0  
        self.track_end = 1 
        self.light_start_value = 0  
        self.light_end_value = 255  
        self.border_color = (0,0,0,1)

        self.lock_progress =  self.lock_position
        self.swipe_progress = self.lock_progress 

        self.size_hint = (1,1)
        self.pos_hint = {'center_x': .5, 'center_y': .5}

        with self.canvas.before:
            self.swipe_color = Color(.82, .9, .99, 1)  
            self.swipe_track = RoundedRectangle(size=(self.width * self.swipe_progress, self.height * .97), pos=self.pos, radius=[17.5])

        self.bind(size=self.update_track, pos=self.update_track)

        self.thumb = MDIconButton(
            icon='',
            style='filled',
            theme_bg_color='Custom',
            md_bg_color=(.45, .45, .45, 1),
            theme_icon_color='Custom',
            icon_color=(.227, .274, .862, .5),
            size_hint=(None, None), 
            ripple_effect = False,
        )
        self.thumb.size = (40, 40)  

        self.arrow_animation = AsyncImage(
            source="images/arrow_animation2.gif",
            size_hint=(None, None),
            size=(30,30),
            pos_hint = {'center_x':.5, 'center_y':.5},
            anim_delay=0.03  
        )

        self.add_widget(self.arrow_animation)
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

            self.update_swipe_track(swipe_progress)
            self.update_thumb(swipe_progress)

            self.swipe_progress = swipe_progress

            if self.locked == False and self.swipe_progress > .6:
                self.lock_animation(.95)
            
            if self.locked == True and self.swipe_progress < .4:
                self.unlock_animation(0.075)

    def update_swipe_track(self, swipe_progress):
        self.swipe_progress = swipe_progress
        self.swipe_track.size = (self.width * swipe_progress, self.height * .97)
        self.swipe_track.pos = self.pos

    def update_track(self, *args):
        self.swipe_track.size = (self.width * self.swipe_progress, self.height * 1)
        self.swipe_track.pos = self.pos
        self.update_thumb(self.swipe_progress)

    def update_thumb(self, swipe_progress):
        self.thumb.pos = (
            self.pos[0] - 5 + (self.width * swipe_progress) - (self.thumb.width / 2),
            self.pos[1] + (self.height / 2) - (self.thumb.height / 2)
        )
    
    def lock_animation(self, target_progress, *args):
        if self.locked:
            return
        self.is_animating = True
        anim = Animation(swipe_progress = target_progress, duration=0.3)
        anim.bind(on_progress = lambda *args: self.update_visuals(self.swipe_progress))
        anim.bind(on_complete=lambda *args: self.lock_done())
        anim.start(self)

    def unlock_animation(self, target_progress, *args):
        if not self.locked:
            return
        self.is_animating = True
        anim = Animation(swipe_progress = target_progress, duration = 0.3)
        anim.bind(on_progress=lambda *args: self.update_visuals(self.swipe_progress))
        anim.bind(on_complete=lambda *args: self.unlock_done())
        anim.start(self)
    
    def update_visuals(self, *args):
        self.update_track(self.swipe_progress)
        self.update_thumb(self.swipe_progress)
    
    def lock_done(self, *args):
        self.is_animating = False
        self.locked = True
        self.lock_store.update_lock_states(True)
        self.apply_lock()
        print(self.locked)
    
    def unlock_done(self, *args):
        self.is_animating = False
        self.locked = False
        self.lock_store.update_lock_states(False)
        self.apply_unlock()
        print(self.locked)

    def apply_lock(self, *args):
        self.parent_widget.lock_icon.icon = 'lock'
        self.parent_widget.label.text = 'Locked'
        self.thumb.md_bg_color = (1,1,1,1)

    def apply_unlock(self, *args):
        self.parent_widget.lock_icon.icon = 'lock-open-variant'
        self.parent_widget.label.text = 'Unlocked'
        self.thumb.md_bg_color = (.45, .45, .45, 1)
        