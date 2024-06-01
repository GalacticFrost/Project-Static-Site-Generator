import unittest
from markdown_text_to_textnode import markdown_text_to_textnode

class TestTextToTextNode(unittest.TestCase):

    def test_default_version(self):
        # code = markdown_text_to_textnode('This is a `code` piece.', '`')
        ital = markdown_text_to_textnode('This is an *italic word*.', '*')
        # bold = markdown_text_to_textnode('**This is a bold sentence.**', '**')

        self.assertEqual(ital, 'HTML()')