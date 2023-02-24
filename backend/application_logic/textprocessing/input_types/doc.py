import docx2txt

from application_logic.textprocessing.input_types.input_type import InputType
import os

class DOC(InputType):
    def __init__(self):
        super().__init__()

    def to_text(self, input) -> str:
        """
        Gets the text from the .txt file and returns it as str

        :param input: unparsed .txt file
        :return: the parsed text element from the .txt file
        """
        try:
            text = docx2txt.process(input)
        except Exception:
            raise Exception("Could not parse input")

        return text
