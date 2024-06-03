import unittest
from textnode import *

class TestSplitNodesHeadingAndBlockquote(unittest.TestCase):

    def test_blockquotes_with_multiple_lines(self):
        content = "> Blockquote with multiple lines.\n> Continuation of blockquote.\n> Another line."
        new_nodes = split_nodes_heading_and_blockquote(content)
        expected_nodes = [
            TextNode("Blockquote with multiple lines.\nContinuation of blockquote.\nAnother line.\n", "blockquote")
        ]
        self.assertEqual([(n.text, n.text_type) for n in new_nodes], [(n.text, n.text_type) for n in expected_nodes])

    def test_blockquotes_without_headings(self):
        content = "> Blockquote line 1\n> Blockquote line 2\nNormal text."
        new_nodes = split_nodes_heading_and_blockquote(content)
        expected_nodes = [
            TextNode("Blockquote line 1\nBlockquote line 2\n", "blockquote"),
            TextNode("Normal text.", "text")
        ]
        self.assertEqual([(n.text, n.text_type) for n in new_nodes], [(n.text, n.text_type) for n in expected_nodes])

    def test_headings_and_blockquotes_combined(self):
        content = "# Heading 1\n> Blockquote 1\n## Heading 2\n> Blockquote 2\nSome text."
        new_nodes = split_nodes_heading_and_blockquote(content)
        expected_nodes = [
            TextNode("Heading 1\n", "heading1"),
            TextNode("Blockquote 1\n", "blockquote"),
            TextNode("Heading 2\n", "heading2"),
            TextNode("Blockquote 2\n", "blockquote"),
            TextNode("Some text.", "text")
        ]
        self.assertEqual([(n.text, n.text_type) for n in new_nodes], [(n.text, n.text_type) for n in expected_nodes])

    def test_mixed_content(self):
        content = "Start with text.\n## Heading\nText > within heading\n> Blockquote here.\nMore text."
        new_nodes = split_nodes_heading_and_blockquote(content)
        expected_nodes = [
            TextNode("Start with text.\n", "text"),
            TextNode("Heading\n", "heading2"),
            TextNode("Text > within heading\n", "text"),
            TextNode("Blockquote here.\n", "blockquote"),
            TextNode("More text.", "text")
        ]
        self.assertEqual([(n.text, n.text_type) for n in new_nodes], [(n.text, n.text_type) for n in expected_nodes])

    def test_mixed_headings_and_blockquotes(self):
        content = "# Heading 1\n> Blockquote under heading 1\nText under heading and blockquote."
        new_nodes = split_nodes_heading_and_blockquote(content)
        expected_nodes = [
            TextNode("Heading 1\n", "heading1"),
            TextNode("Blockquote under heading 1\n", "blockquote"),
            TextNode("Text under heading and blockquote.", "text")
        ]
        self.assertEqual([(n.text, n.text_type) for n in new_nodes], [(n.text, n.text_type) for n in expected_nodes])

    def test_only_headings(self):
        content = "# Heading 1\n## Heading 2\n### Heading 3"
        new_nodes = split_nodes_heading_and_blockquote(content)
        expected_nodes = [
            TextNode("Heading 1\n", "heading1"),
            TextNode("Heading 2\n", "heading2"),
            TextNode("Heading 3\n", "heading3")
        ]
        self.assertEqual([(n.text, n.text_type) for n in new_nodes], [(n.text, n.text_type) for n in expected_nodes])

    def test_only_blockquotes(self):
        content = "> Blockquote 1\n> Blockquote 2\n> Blockquote 3"
        new_nodes = split_nodes_heading_and_blockquote(content)
        expected_nodes = [
            TextNode("Blockquote 1\nBlockquote 2\nBlockquote 3\n", "blockquote")
        ]
        self.assertEqual([(n.text, n.text_type) for n in new_nodes], [(n.text, n.text_type) for n in expected_nodes])

if __name__ == '__main__':
    unittest.main()
