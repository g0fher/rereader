import warnings
warnings.filterwarnings('ignore')

import ebooklib
from ebooklib import epub
import re
from html import unescape
from PIL import ImageFont
from functools import lru_cache
import time


def break_text_into_lines(text, max_width_px, font):  
    # Split the text into chunks (words) by whitespaces
    words = text.split()
    
    lines = []
    current_line = []
    current_width = 0

    for word in words:
        # Get word width
        word_width = get_word_width(word, font)
        # word_width = font.getlength(word + " ")
        # Line overflow
        if current_width + word_width > max_width_px:
            lines.append(" ".join(current_line))
            # Begin new line with the current word
            current_line = [word]
            current_width = word_width
        else:
            current_line.append(word)
            current_width += word_width

    # If there's anything left, put it in the last line
    if current_line:
        lines.append(" ".join(current_line))

    return lines


def extract_paragraphs_from_epub(epub_file):
    book = epub.read_epub(epub_file)
    
    paragraphs = []
    
    # Iterate through all the items in the book
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            # Extract the HTML content from the item
            content = item.get_body_content().decode('utf-8')
            
            # Find all <p>...</p> tags, as .epub files have paragraphs in them
            p_tags = re.findall(r'<p.*?>(.*?)</p>', content, re.DOTALL)
            
            # Clean and unescape HTML entities (e.g., &amp; -> &)
            for par in p_tags:
                # Remove html tags
                par = re.sub(r'<[^>]+>', '', par)
                # Remove new lines inside paragraphs if any
                par = re.sub(r'\s*\n\s*', ' ', par)
                # Unescape, for example: (&amp; -> &)
                par = unescape(par.strip())
                paragraphs.append(par)
    
    return paragraphs

def split_pars_into_lines(final_lines, paragraphs, max_width_px, font):
    for par in paragraphs:
        lines = break_text_into_lines(par, max_width_px, font)
        for line in lines:
            final_lines.append(line + " ")
            # final_lines.append(line + "\n")
        final_lines[len(final_lines) - 1] += "\n"
    
    return final_lines

@lru_cache(maxsize=None)
def get_word_width(word, font):
    return font.getlength(word + " ")

if __name__ == "__main__":

    print("Start")

    # par = extract_paragraphs_from_epub('The Billiard Ball Asimov Isaac.epub')
    # par = extract_text_from_epub('The Billiard Ball Asimov Isaac.epub')
    # par = extract_text_from_epub('story_of_your_life.epub')
    # par = extract_text_from_epub('The Three-Body Problem.epub')

    # book_path = 'djury.epub'
    # book_path = 'The Three-Body Problem.epub'
    # book_path = 'hemingway-old-man-and-the-sea.epub'
    book_path = 'louisa-may-alcott_little-women.epub'
    # book_path = 'daniel-defoe_the-life-and-adventures-of-robinson-crusoe.epub'

    font_path = "PTSans-Regular.ttf"
    max_width = 1080
    font_size = 24

    font = ImageFont.truetype(font_path, font_size)

    # text = "test123test123test123test123blablatesetassasi"
    # text = "iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiit"
    text = "............................................................................"

    print(get_word_width(text, font))

    
    # space_width = font.getbbox(" ")[2]

    # bbox = font.getbbox("tg")
    # font_height = bbox[3] - bbox[1]


    # pars = extract_paragraphs_from_epub(book_path)
    # print("Done paragraphs")
    # par = extract_text_from_epub(book_path)
    # print("Number of paragraphs:", len(pars))
    # print(pars[0:20])

    # final_lines = []

    # start = time.perf_counter()
    # final_lines = split_pars_into_lines(final_lines, pars, max_width, font)
    # final_lines = split_pars_into_lines(final_lines, pars[601:1200], max_width, font)
    # end = time.perf_counter()

    # print("Done splitting")
    # print(len(final_lines))
    # print(f"Splitting time: {end - start:.6f} seconds")

    # print(final_lines[0:20])
    # i = 0
    # for line in final_lines:
    #     print(i, line)
    #     i += 1
    

    # print(par[0:10])
    # print(pars[80:100])



