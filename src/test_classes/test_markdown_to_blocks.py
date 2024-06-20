import unittest
from textnode import *

class TestMarkdownToBlocks(unittest.TestCase):
    def test_simple_document(self):
        markdown_1 = """
        This is **bolded** paragraph

        This is another paragraph with *italic* text and `code` here
        This is the same paragraph on a new line

        * This is a list
        * with items
        """
        expected_1 = ["This is **bolded** paragraph",
                      "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                      "* This is a list\n* with items"]
        self.assertEqual(markdown_to_blocks(markdown_1), expected_1)

    def test_multiple_blank_lines(self):
        markdown_2 = """
        This is a **bold** line


        This is another paragraph


        * List item 1

        * List item 2
        """
        expected_2 = ["This is a **bold** line",
                      "This is another paragraph",
                      "* List item 1",
                      "* List item 2"]
        self.assertEqual(markdown_to_blocks(markdown_2), expected_2)

    def test_leading_trailing_whitespace(self):
        markdown_3 = """
     
        This is a paragraph with leading whitespace     
     

        with trailing whitespaces     
  
  
        """
        expected_3 = ["This is a paragraph with leading whitespace", "with trailing whitespaces"]
        self.assertEqual(markdown_to_blocks(markdown_3), expected_3)

    def test_only_blank_lines(self):
        markdown_4 = """


        """
        expected_4 = []
        self.assertEqual(markdown_to_blocks(markdown_4), expected_4)

    def test_no_blank_lines(self):
        markdown_5 = """This is a single block with no empty lines at all."""
        expected_5 = ["This is a single block with no empty lines at all."]
        self.assertEqual(markdown_to_blocks(markdown_5), expected_5)

    def test_single_line_blocks(self):
        markdown_6 = """
        First block

        Second block

        Third block
        """
        expected_6 = ["First block", "Second block", "Third block"]
        self.assertEqual(markdown_to_blocks(markdown_6), expected_6)

if __name__ == '__main__':
    unittest.main()