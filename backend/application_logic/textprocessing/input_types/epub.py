import ebooklib
from bs4 import BeautifulSoup
from ebooklib import epub
import os
from application_logic.textprocessing.input_types.input_type import InputType


class EPUB(InputType):
    def __init__(self):
        super().__init__()

    def to_text(self, input) -> str:
        """
        Gets the text from the .txt file and returns it as str

        :param input: unparsed .txt file
        :return: the parsed text element from the .txt file
        """
        try:
            book = epub.read_epub(input)
            items = list(book.get_items_of_type(ebooklib.ITEM_DOCUMENT))
            text = ""
            for item in items:
                soup = BeautifulSoup(item.get_body_content(), 'html.parser')
                chapter_text = [para.get_text() for para in soup.find_all('p')]
                text += ''.join(chapter_text)
        except Exception:
            raise Exception("Could not parse input")

        return text
