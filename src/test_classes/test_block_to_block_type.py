import unittest
from textnode import block_to_block_type

class TestBlockToBlockType(unittest.TestCase):

    def test_standard_examples(self):
        self.assertEqual(block_to_block_type("# Heading 1"), "heading")
        self.assertEqual(block_to_block_type("> This is a blockquote."), "quote")
        self.assertEqual(block_to_block_type("```python\nprint('Hello, world!')\n```"), "code")
        self.assertEqual(block_to_block_type("* Unordered list item"), "ulist")
        self.assertEqual(block_to_block_type("1. Ordered list item"), "olist")

    def test_nested_examples(self):
        self.assertEqual(block_to_block_type("## Heading 2"), "heading")
        self.assertEqual(block_to_block_type("> Nested blockquote."), "quote")
        self.assertEqual(block_to_block_type("* Nested unordered list item"), "ulist")
        self.assertEqual(block_to_block_type("1.1. Nested ordered list item"), "olist")

    def test_edge_cases(self):
        self.assertEqual(block_to_block_type(""), "paragraph")  # Empty string
        self.assertEqual(block_to_block_type("###"), "paragraph")  # Invalid heading without text
        self.assertEqual(block_to_block_type(">"), "paragraph")  # Invalid blockquote without text
        self.assertEqual(block_to_block_type("```"), "paragraph")  # Incomplete code block
        self.assertEqual(block_to_block_type("* "), "paragraph")  # Unordered list item without text
        self.assertEqual(block_to_block_type("1. "), "paragraph")  # Ordered list item without text
        self.assertEqual(block_to_block_type("1.5 Invalid ordered list item"), "paragraph")  # Invalid ordered list format

    def test_multiline_code_block(self):
        code_block = "```\nprint('Hello, world!')\nprint('Goodbye, world!')\n```"
        self.assertEqual(block_to_block_type(code_block), "code")

    def test_delimited_unordered_list(self):
        block = "* Item 1\n* Item 2\n* Item 3"
        self.assertEqual(block_to_block_type(block), "ulist")

    def test_delimited_unordered_list(self):
        block = "* Item 1\n* Item 2\n* Item 3"
        self.assertEqual(block_to_block_type(block), "ulist")

    def test_delimited_ordered_list(self):
        block = "1. Item 1\n2. Item 2\n3. Item 3"
        self.assertEqual(block_to_block_type(block), "olist")

    def test_multiline_blockquote(self):
        block = "> This is a blockquote.\n> And it continues here."
        self.assertEqual(block_to_block_type(block), "quote")

    def test_multiline_heading(self):
        block = "# Heading 1\n## Heading 2"
        self.assertEqual(block_to_block_type(block.split("\n")[0]), "heading")
        self.assertEqual(block_to_block_type(block.split("\n")[1]), "heading")

if __name__ == "__main__":
    unittest.main()
