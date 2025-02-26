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
            halign='left',
            # halign='justify',
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


        self.par_cap = 5
        self.resplit_lines()
        self.lines_per_page = 18
        self.update_lines()

        return layout
    
    def resplit_lines(self):
        print("============")
        self.final_lines = ["............................................................................ "]
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
            print(i, self.final_lines[i])
            # print(i, self.final_lines[i], end="")
            page += self.final_lines[i]

            if i > self.number_of_lines - 1:
                print("Lines have ended")
                return page

        return page

    # def update_page_lines(self):

    # def paginate_lines(self)


if __name__ == "__main__":
    BookApp().run()
