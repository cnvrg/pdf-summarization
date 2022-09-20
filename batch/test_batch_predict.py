import unittest

from extractor import _process_file_ocr
from extractor import _process_file_pdf
from extractor import extract

from summarizer import breakup
from summarizer import summarize


class Test_batch(unittest.TestCase):
    """ Defining the sample data and files to carry out the testing """

    def setUp(self):
        self.pdf = "sample.pdf"
        with open("sample.txt") as f:
            self.text = f.read()


class Test_extractor(Test_batch):
    """ Testing the extractor code used to extract text from pdfs"""

    def test_pdf(self):
        result = _process_file_pdf(self.pdf)
        self.assertIsInstance(result, dict)
        self.assertEqual(result[0], "This is the sample digital pdf page.")
        self.assertEqual(result[1], "")

    def test_ocr(self):
        result = _process_file_ocr(self.pdf, [1], {})
        self.assertIsInstance(result, dict)
        self.assertEqual(result[1], "This is a sample scanned page. ")

    def test_extract(self):
        result = extract(self.pdf)
        self.assertIsInstance(result, dict)


class Test_summarizer(Test_batch):
    """ Testing the summarizer used to summarize the text """

    def test_breakup(self):
        result = breakup(self.text)
        self.assertIsInstance(result, list)

    def test_summarize_full(self):
        result = summarize({0: self.text[:512], 1: self.text[:512]}, False)
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), 1)

    def test_summarize_pagewise(self):
        result = summarize({0: self.text[:512], 1: self.text[:512]}, True)
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), 2)


if __name__ == "__main__":
    unittest.main()
