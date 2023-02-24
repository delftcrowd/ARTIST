# from PyPDF2 import PdfReader
import os
import random

import application_logic.textprocessing.input_types.doc as doc
import application_logic.textprocessing.input_types.epub as epub
import application_logic.textprocessing.input_types.pdf as pdf
import application_logic.textprocessing.input_types.txt as txt


class InputProcessor(object):
    def __init__(self, content_type):
        """
        Initializes the a processor which can parse well defined inputs

        :param content_type: the content type with which the processor work.
        """
        self.content_type = content_type

        if self.content_type == ".pdf":
            self.processor = pdf.PDF()
        elif self.content_type == ".docx" or self.content_type == ".doc":
            self.processor = doc.DOC()
        elif self.content_type == ".epub":
            self.processor = epub.EPUB()
        elif self.content_type == ".txt":
            self.processor = txt.PlainText()
        else:
            raise ValueError("Invalid input type")

    def to_str(self, request_input):
        """
        Gets the text from the input and returns it as str

        :param request_input: unparsed input
        :return: the parsed text element from the unparsed input as a string
        """
        extension = os.path.splitext(str(request_input))[1]
        file_path = "temp" + str(random.randint(10000, 99999)) + extension
        try:

            with open(file_path, 'wb') as out:
                out.write(request_input.file.read())
            result = self.processor.to_text(file_path)
            
        except Exception as e:
            raise e

        finally:
            if(os.path.exists(file_path)):
                os.remove(file_path)
        return result


def get_supported_files():
    return [".txt", ".pdf", ".epub", ".doc", ".docx"]
