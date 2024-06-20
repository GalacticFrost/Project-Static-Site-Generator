import unittest
from textnode import TextNode
from textnode import split_nodes_heading

class TestSplitNodesHeading(unittest.TestCase):

    def test_single_heading(self):
        text = "# Heading 1"
        expected_nodes = [
            TextNode("Heading 1", "heading1")
        ]
        nodes = split_nodes_heading(text)
        self.assertEqual([(n.text, n.text_type) for n in nodes], [(n.text, n.text_type) for n in expected_nodes])

    def test_multiple_headings(self):
        text = "# Heading 1\n## Heading 2\n### Heading 3"
        expected_nodes = [
            TextNode("Heading 1", "heading1"),
            TextNode("Heading 2", "heading2"),
            TextNode("Heading 3", "heading3")
        ]
        nodes = split_nodes_heading(text)
        self.assertEqual([(n.text, n.text_type) for n in nodes], [(n.text, n.text_type) for n in expected_nodes])

    def test_heading_with_text(self):
        text = "# Heading with text\nSome content here."
        expected_nodes = [
            TextNode("Heading with text", "heading1"),
            TextNode("Some content here.", "text")
        ]
        nodes = split_nodes_heading(text)
        self.assertEqual([(n.text, n.text_type) for n in nodes], [(n.text, n.text_type) for n in expected_nodes])

    def test_no_heading(self):
        text = "No heading here."
        expected_nodes = [
            TextNode("No heading here.", "text")
        ]
        nodes = split_nodes_heading(text)
        self.assertEqual([(n.text, n.text_type) for n in nodes], [(n.text, n.text_type) for n in expected_nodes])

if __name__ == '__main__':
    unittest.main()