import os

from PyPDF2 import PdfReader

from application_logic.textprocessing.input_types.input_type import InputType


class PDF(InputType):
    def __init__(self):
        super().__init__()

    def to_text(self, input) -> str:
        """
        Gets the text from the .txt file and returns it as str

        :param input: unparsed .txt file
        :return: the parsed text element from the .txt file
        """
        try:
            reader = PdfReader(input)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
        except Exception:
            raise Exception("Could not parse input")

        return text
