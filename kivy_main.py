from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window

from math import floor
from PIL import ImageFont
import time

import book


class BookApp(App):
    def build(self):

        # book_path = 'The Billiard Ball Asimov Isaac.epub'
        # book_path = 'story_of_your_life.epub' # need to use text function for that
        # book_path = 'The Three-Body Problem.epub'
        # book_path = 'hemingway-old-man-and-the-sea.epub'
        # book_path = 'louisa-may-alcott_little-women.epub'
        book_path = 'daniel-defoe_the-life-and-adventures-of-robinson-crusoe.epub'
        # book_path = 'All Clear.epub'
        # book_path = 'Good-Omens.epub'
        # book_path = 'djury.epub' #ass

        self.font_size = 24
        self.line_height = 1.2
        self.font_bb_height = 26
        self.white_space_length = 9

        layout_padding = 10
        layout = BoxLayout(orientation='vertical', padding=layout_padding)

        window_size_x = 520
        window_size_y = 850
        scale = Window.dpi / 96
        Window.size = (window_size_x / scale, window_size_y / scale)

        self.first_resize = True

        # Main reading area text
        self.text_label = Label(
            text="", 
            markup=True, 
            size_hint_y=0.85, 
            text_size=(None, None), 
            valign='middle', 
            halign='left',
            # halign='justify',
            font_name='PTSans-Regular.ttf',
            font_size=self.font_size,
            line_height=self.line_height
        )

        self.lines_per_page = 0
        self.text_area_width = window_size_x - layout_padding * 2 + self.white_space_length
        print(self.text_area_width)
        self.text_label.bind(texture_size=self.update_label_height)
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


        self.par_cap = 100
        self.resplit_lines()
        self.lines_per_page = 18
        self.update_lines(self.lines_per_page)

        return layout
    
    def resplit_lines(self):
        self.final_lines = []
        start = time.perf_counter()
        self.final_lines = book.split_pars_into_lines(self.final_lines, self.pars[0:self.par_cap], self.text_area_width, self.font)
        end = time.perf_counter()
        print("Done splitting")
        print(f"Splitting time: {end - start:.6f} seconds")
        print("Number of lines:", len(self.final_lines))
        self.number_of_lines = len(self.final_lines)
        self.current_line_index = 0
        self.update_lines(self.lines_per_page)

    def next_line(self, instance):
        if self.current_line_index < self.number_of_lines - 1:
            self.current_line_index += self.lines_per_page
            self.update_lines(self.lines_per_page)
        
    def prev_line(self, instance):
        if self.current_line_index > 0:
            self.current_line_index -= self.lines_per_page
            self.update_lines(self.lines_per_page)

    def update_lines(self, lines_per_page):
        self.text_label.text = self.display_lines(lines_per_page)

    def update_label_height(self, instance, size):
        # Resize the label's texture area to match the window height
        self.text_label.height = size[1]
        self.text_area_width = self.text_label.width
        print("Width:", self.text_area_width)
        self.resplit_lines()
        self.lines_per_page = floor(self.text_label.height / (self.font_bb_height + self.line_height * self.font_bb_height)) + 1
        print("Height:", self.text_label.height, "Lpp:", self.lines_per_page)
    
    def update_label_text_size(self, instance, value):
        # Update the text size when the label's size changes
        instance.text_size = instance.size

    def display_lines(self, lines_per_page):
        if self.current_line_index > self.number_of_lines - 1:
            print("Line index exceeding total number of lines")
            return -1
        page = ""
        print("============")
        for i in range(self.current_line_index, self.current_line_index + lines_per_page):
            print(i, self.final_lines[i])
            page += self.final_lines[i]

            if i > self.number_of_lines - 1:
                print("Lines have ended")
                return page

        return page

    # def update_page_lines(self):

    # def paginate_lines(self)


if __name__ == "__main__":
    BookApp().run()
