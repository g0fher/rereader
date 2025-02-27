from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.clock import Clock

class ClickableLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.normal_color = (1, 1, 1, 1)
        self.highlight_color = (0, 1, 0, 1)

    def activate_long_press(self, dt):
        app = App.get_running_app()
        if not app.lifted_before_clock:
            app.is_long_press_on = True
            self.long_press_active = True
            self.color = self.highlight_color
            print(f"Long press activated on: {self.text}")
        else:
            print("Failed hold")

    def on_touch_down(self, touch):
        app = App.get_running_app()
        if self.collide_point(*touch.pos):
            # Start a timer for long press detection (0.5 seconds)
            app.lifted_before_clock = False
            Clock.schedule_once(self.activate_long_press, 0.5)
            return True  # Consume touch
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        app = App.get_running_app()
        if app.is_long_press_on:
            if self.collide_point(*touch.pos):
                self.color = self.highlight_color
                app.is_on_label = True
                print(f"Over: {self.text}")
                return True
            else:
                self.color = self.normal_color
                app.is_on_label = False
        return super().on_touch_move(touch)
    
    def on_touch_up(self, touch):
        app = App.get_running_app()
        if app.is_long_press_on:
            app.is_long_press_on = False
            # self.parent.clear_hightlights()
            app.clear_hightlights_all()
            if app.is_on_label:
                print("Lifted on")
            else:
                print("Lifted off")
            return True
        else:
            app.lifted_before_clock = True
            
        return super().on_touch_up(touch)

class JustifiedBoxLayout(BoxLayout):
    def __init__(self, words, height, **kwargs):
        super().__init__(**kwargs)
        self.words = words
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = height
        self.bind(size=self.update_layout)

        # Create labels for each word
        for word in words:
            label = ClickableLabel(text=word, size_hint_x=None)
            self.add_widget(label)

        # self.update_layout()
        Clock.schedule_once(self.update_layout, 0)
    
    def clear_hightlights(self):
        # Loop through all children of the layout
        for child in self.children:
            # Check if the child is a Label (or a subclass like ClickableLabel)
            if isinstance(child, Label):  
                child.color = (1, 1, 1, 1)
    
    def update_layout(self, *args):
        """ Adjusts label width and spacing to ensure even distribution """
        if not self.children:
            return

        total_label_width = sum(child.texture_size[0] for child in self.children)
        available_width = self.width

        # Calculate the number of gaps between labels
        gap_count = len(self.children) - 1

        # No negative spacing
        if gap_count > 0:
            # Evenly distribute remaining space
            spacing = max((available_width - total_label_width) / gap_count, 0)
        else:
            spacing = 0

        # Update label sizes and positions
        # Start placing labels from the left edge
        x_offset = 0
        for child in self.children:
            child.size_hint_x = None
            child.width = child.texture_size[0]
            child.x = x_offset
            # Move to the next position
            x_offset += child.width + spacing

        self.spacing = spacing

class JustifiedTextApp(App):
    is_long_press_on = False
    is_lifted = False
    is_on_label = False
    lifted_before_clock = True

    def build(self):
        self.root = BoxLayout(orientation='vertical', padding=0)

        words = ["This", "is", "a", "justified", "text", "example", "help", "text", "example", "help"]
        self.justified_line = JustifiedBoxLayout(words, 40)
        self.root.add_widget(self.justified_line)

        words2 = ["This", "is", "an", "ass", "text", "example", "ahhhh"]
        self.justified_line2 = JustifiedBoxLayout(words2, 40)
        self.root.add_widget(self.justified_line2)

        # words3 = ["This", "is", "an", "ass", "text", "example"]
        # self.justified_line3 = JustifiedBoxLayout(words3, 40)
        # root.add_widget(self.justified_line3)

        # self.clear_hightlights_all()

        return self.root

    def clear_hightlights_all(self):
        # Loop through all children of the layout
        for widget in self.root.children:
            print("ass2")
            for labels in widget.children:
                if isinstance(labels, Label):  
                    labels.color = (1, 1, 1, 1)
                    print("ass")
    


if __name__ == "__main__":
    JustifiedTextApp().run()
