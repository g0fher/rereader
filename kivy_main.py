from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.clock import Clock

from math import floor
from PIL import ImageFont
import time

import book

# class ClickableLabel(Label):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.normal_color = (1, 1, 1, 1)
#         self.highlight_color = (0, 1, 0, 1)

#     def activate_long_press(self, dt):
#         app = App.get_running_app()
#         if not app.lifted_before_clock:
#             app.is_long_press_on = True
#             self.long_press_active = True
#             self.color = self.highlight_color
#             print(f"Long press activated on: {self.text}")
#         else:
#             print("Failed hold")

#     def on_touch_down(self, touch):
#         app = App.get_running_app()
#         if self.collide_point(*touch.pos):
#             # Start a timer for long press detection (0.5 seconds)
#             app.lifted_before_clock = False
#             Clock.schedule_once(self.activate_long_press, 0.5)
#             return True  # Consume touch
#         return super().on_touch_down(touch)

#     def on_touch_move(self, touch):
#         app = App.get_running_app()
#         if app.is_long_press_on:
#             if self.collide_point(*touch.pos):
#                 self.color = self.highlight_color
#                 app.is_on_label = True
#                 print(f"Over: {self.text}")
#                 return True
#             else:
#                 self.color = self.normal_color
#                 app.is_on_label = False
#         return super().on_touch_move(touch)
    
#     def on_touch_up(self, touch):
#         app = App.get_running_app()
#         if app.is_long_press_on:
#             app.is_long_press_on = False
#             # self.parent.clear_hightlights()
#             app.clear_hightlights_all()
#             if app.is_on_label:
#                 print("Lifted on")
#             else:
#                 print("Lifted off")
#             return True
#         else:
#             app.lifted_before_clock = True
            
#         return super().on_touch_up(touch)

# class JustifiedBoxLayout(BoxLayout):
#     def __init__(self, words, height, **kwargs):
#         super().__init__(**kwargs)
#         self.words = words
#         self.orientation = 'horizontal'
#         self.size_hint_y = None
#         self.height = height
#         self.bind(size=self.update_layout)

#         # Create labels for each word
#         for word in words:
#             label = ClickableLabel(text=word, size_hint_x=None)
#             self.add_widget(label)

#         # self.update_layout()
#         Clock.schedule_once(self.update_layout, 0)
    
#     def clear_hightlights(self):
#         # Loop through all children of the layout
#         for child in self.children:
#             # Check if the child is a Label (or a subclass like ClickableLabel)
#             if isinstance(child, Label):  
#                 child.color = (1, 1, 1, 1)
    
#     def update_layout(self, *args):
#         """ Adjusts label width and spacing to ensure even distribution """
#         if not self.children:
#             return

#         total_label_width = sum(child.texture_size[0] for child in self.children)
#         available_width = self.width

#         # Calculate the number of gaps between labels
#         gap_count = len(self.children) - 1

#         # No negative spacing
#         if gap_count > 0:
#             # Evenly distribute remaining space
#             spacing = max((available_width - total_label_width) / gap_count, 0)
#         else:
#             spacing = 0

#         # Update label sizes and positions
#         # Start placing labels from the left edge
#         x_offset = 0
#         for child in self.children:
#             child.size_hint_x = None
#             child.width = child.texture_size[0]
#             child.x = x_offset
#             # Move to the next position
#             x_offset += child.width + spacing

#         self.spacing = spacing



class BookApp(App):

    is_long_press_on = False
    is_lifted = False
    is_on_label = False
    lifted_before_clock = True

    def build(self):

        book_path = 'daniel-defoe_the-life-and-adventures-of-robinson-crusoe.epub'

        self.font_size = 24
        self.line_height = 1
        self.font_bb_height = 26
        self.white_space_length = 9

        layout_padding = 0
        layout = BoxLayout(orientation='vertical', padding=layout_padding)

        window_size_x = 500
        window_size_y = 850
        scale = Window.dpi / 96
        Window.size = (window_size_x / scale, window_size_y / scale)

        # Main reading area text
        self.text_label = Label(
            text="", 
            markup=True, 
            size_hint_y=0.85, 
            text_size=(None, None), 
            valign='middle', 
            # halign='left',
            halign='justify',
            font_name='PTSans-Regular.ttf',
            font_size=self.font_size,
            line_height=self.line_height
        )

        self.lines_per_page = 0
        self.text_area_width = window_size_x - layout_padding * 2
        print(self.text_area_width)
        self.text_label.bind(texture_size=self.update_label_area_size)
        self.text_label.bind(size=self.update_label_text_size)

        # Pagination Controls
        self.page_layout = GridLayout(cols=2, size_hint=(1, 0.15))
        self.prev_button = Button(text="Previous", on_press=self.prev_line)
        self.next_button = Button(text="Next", on_press=self.next_line)
        self.page_layout.add_widget(self.prev_button)
        self.page_layout.add_widget(self.next_button)

        self.page = ""

        layout.add_widget(self.text_label)
        layout.add_widget(self.page_layout)


        font_path = "PTSans-Regular.ttf"
        self.font = ImageFont.truetype(font_path, self.font_size)
        self.pars = book.extract_paragraphs_from_epub(book_path)
        print("Done paragraphs")
        print("Number of paragraphs:", len(self.pars))


        self.par_cap = 20
        self.resplit_lines()
        self.lines_per_page = 18
        self.update_lines()


        # root = BoxLayout(orientation='vertical', padding=0)
        # for i in range(self.lines_per_page):
        #     self.justified_line = JustifiedBoxLayout(self.final_lines[i].split(), 40)
        #     # print(self.final_lines[0:5])
        #     # print(self.lines_per_page)
        #     root.add_widget(self.justified_line)
        # # return root

        return layout

    def clear_hightlights_all(self):
        # Loop through all children of the layout
        for widget in self.root.children:
            for labels in widget.children:
                if isinstance(labels, Label):  
                    labels.color = (1, 1, 1, 1)
    
    def resplit_lines(self):
        print("============")
        self.final_lines = []
        start = time.perf_counter()
        self.final_lines = book.split_pars_into_lines(self.final_lines, self.pars[0:self.par_cap], self.text_area_width, self.font)
        end = time.perf_counter()
        print("Done splitting")
        print(f"Splitting time: {end - start:.6f} seconds")
        print("Number of lines:", len(self.final_lines))
        self.number_of_lines = len(self.final_lines)
        self.current_line_index = 0
        self.update_lines()

    def next_line(self, instance):
        if self.current_line_index < self.number_of_lines - 1:
            self.current_line_index += self.lines_per_page
            self.update_lines()
        
    def prev_line(self, instance):
        if self.current_line_index > 0:
            self.current_line_index -= self.lines_per_page
            self.update_lines()

    def update_lines(self):
        print("Lpp:", self.lines_per_page)
        self.text_label.text = self.display_lines()

    def update_label_area_size(self, instance, size):
        # Resize the label's texture height and width to match the window height
        # I don't understand how it works, but this line is important
        self.text_label.height = size[1]

        self.lines_per_page = floor(self.text_label.height / (self.font_bb_height + self.line_height * self.font_bb_height)) + 1
        
        # Don't resplit the lines in case of only height changes
        if self.text_area_width != self.text_label.width:
            self.text_area_width = self.text_label.width
            # Don't resplit on the first resize because it's incorrect
            self.resplit_lines()

        print("Width:", int(self.text_area_width), "Height:", int(self.text_label.height), "Lpp:", self.lines_per_page)
    
    def update_label_text_size(self, instance, value):
        # Update the text size when the label's size changes
        instance.text_size = instance.size

    def display_lines(self):
        if self.current_line_index > self.number_of_lines - 1:
            print("Line index exceeding total number of lines")
            return -1
        page = ""
        for i in range(self.current_line_index, self.current_line_index + self.lines_per_page):
            # print(i, self.final_lines[i])
            print(i, self.final_lines[i], end="")
            page += self.final_lines[i]

            if i > self.number_of_lines - 2:
                print("Lines have ended")
                return page

        return page

    # def update_page_lines(self):

    # def paginate_lines(self)


if __name__ == "__main__":
    BookApp().run()
