import unittest
from textnode import *

class TestMarkdownTextToTextNode(unittest.TestCase):

    def test_single_delimiter(self):
        sentence = "This is text with `code block` word"
        delimiter = "`"
        expected_output = [
            TextNode("This is text with ", "text"),
            TextNode("code block", "code"),
            TextNode(" word", "text")
        ]
        result = split_nodes_delimiter(sentence, [delimiter])
        self.assertEqual(result, expected_output)

    def test_multiple_delimiters(self):
        sentence = "This is *italic* and **bold** text"
        delimiters = ["*", "**"]
        expected_output = [
            TextNode("This is ", "text"),
            TextNode("italic", "italic"),
            TextNode(" and ", "text"),
            TextNode("bold", "bold"),
            TextNode(" text", "text")
        ]
        result = split_nodes_delimiter(sentence, delimiters)
        self.assertEqual(result, expected_output)

    def test_nested_delimiters(self):
        sentence = "This is `code` and **bold** and *italic* text"
        delimiters = ["`", "**", "*"]
        expected_output = [
            TextNode("This is ", "text"),
            TextNode("code", "code"),
            TextNode(" and ", "text"),
            TextNode("bold", "bold"),
            TextNode(" and ", "text"),
            TextNode("italic", "italic"),
            TextNode(" text", "text")
        ]
        result = split_nodes_delimiter(sentence, delimiters)
        self.assertEqual(result, expected_output)

    def test_unmatched_delimiter_raises_exception(self):
        sentence = "This is `unmatched code block"
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter(sentence, ["`"])
        self.assertTrue('Unmatched' in str(context.exception))

    def test_invalid_delimiter_raises_exception(self):
        sentence = "This is text with ^invalid^ delimiter"
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter(sentence, ["^"])
        self.assertTrue('is not a valid markdown syntax' in str(context.exception))

    def test_empty_string(self):
        sentence = ""
        delimiters = ["`", "**", "*"]
        expected_output = []
        result = split_nodes_delimiter(sentence, delimiters)
        self.assertEqual(result, expected_output)
    
    def test_no_delimiter_in_text(self):
        sentence = "This is a plain text with no markdown"
        delimiters = ["`", "**", "*"]
        expected_output = [
            TextNode("This is a plain text with no markdown", "text")
        ]
        result = split_nodes_delimiter(sentence, delimiters)
        self.assertEqual(result, expected_output)

    def test_split_nodes_delimiter_start_with_single_delimiter(self):
        sentence = "*italic text* and normal text"
        delimiters = ["*", "`", "**"]
        nodes = split_nodes_delimiter(sentence, delimiters)
        expected = [
            TextNode("italic text", "italic"),
            TextNode(" and normal text", "text")
        ]
        self.assertEqual(nodes, expected)
    
    def test_split_nodes_delimiter_start_with_double_delimiter(self):
        sentence = "**bold text** and normal text"
        delimiters = ["*", "`", "**"]
        nodes = split_nodes_delimiter(sentence, delimiters)
        expected = [
            TextNode("bold text", "bold"),
            TextNode(" and normal text", "text")
        ]
        self.assertEqual(nodes, expected)
    
if __name__ == "__main__":
    unittest.main()