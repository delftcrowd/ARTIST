import unittest
import application_logic.textprocessing.input_types.doc as doc
import application_logic.textprocessing.input_types.epub as epub
import application_logic.textprocessing.input_types.pdf as pdf
import application_logic.textprocessing.input_types.txt as txt
from application_logic.textprocessing.input_types.input_type import InputType
import os
from difflib import SequenceMatcher

'''
if self.content_type == ".pdf":
            self.processor = pdf.PDF()
        elif self.content_type == ".docx" or self.content_type == ".doc":
            self.processor = doc.DOC()
        elif self.content_type == ".epub":
            self.processor = epub.EPUB()
        elif self.content_type == ".txt":
            self.processor = txt.PlainText()

            '''

class TestStringMethods(unittest.TestCase):
    """
    TestStringMethods is the class used to test the file processing methods

    """

    def test_doc2txt(self):
        processor = doc.DOC()
        file_path = "application_logic/textprocessing/TestFiles/test_doc.docx"
        expected_result_path = "application_logic/textprocessing/TestFiles/expected_doc.txt"
        result = processor.to_text(file_path)
        with open(expected_result_path) as f:
            expectedResult = f.read()
        assert(SequenceMatcher(None, result, expectedResult).ratio()>0.95)


    def test_pdf(self):
        processor = pdf.PDF()
        file_path = "application_logic/textprocessing/TestFiles/test_pdf.pdf"
        expected_result_path = "application_logic/textprocessing/TestFiles/expected_pdf.txt"
        result = processor.to_text(file_path)
        with open(expected_result_path) as f:
            expectedResult = f.read()
        assert(SequenceMatcher(None, result, expectedResult).ratio()>0.95)


    def test_txt(self):
        processor = txt.PlainText()
        file_path = "application_logic/textprocessing/TestFiles/test_txt.txt"
        expected_result_path = "application_logic/textprocessing/TestFiles/expected_txt.txt"
        result = processor.to_text(file_path)
        with open(expected_result_path) as f:
            expectedResult = f.read()
        assert(SequenceMatcher(None, result, expectedResult).ratio()>0.95)


    


if __name__ == '__main__':
    unittest.main()