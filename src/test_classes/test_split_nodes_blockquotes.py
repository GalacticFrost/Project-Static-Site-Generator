import unittest
from textnode import TextNode
from textnode import split_nodes_blockquote

class TestSplitNodesBlockquote(unittest.TestCase):

    def test_single_blockquote(self):
        text = "> Blockquote 1"
        expected_nodes = [
            TextNode("Blockquote 1", "quote")
        ]
        nodes = split_nodes_blockquote([TextNode(text)])
        self.assertEqual([(n.text, n.text_type) for n in nodes], [(n.text, n.text_type) for n in expected_nodes])

    def test_multiple_blockquotes(self):
        text = "> Blockquote 1\n> Blockquote 2\n> Blockquote 3"
        expected_nodes = [
            TextNode("Blockquote 1", "quote"),
            TextNode("Blockquote 2", "quote"),
            TextNode("Blockquote 3", "quote")
        ]
        nodes = split_nodes_blockquote([TextNode(text)])
        self.assertEqual([(n.text, n.text_type) for n in nodes], [(n.text, n.text_type) for n in expected_nodes])

    def test_blockquote_with_text(self):
        text = "> Blockquote with text\nSome content here."
        expected_nodes = [
            TextNode("Blockquote with text", "quote"),
            TextNode("Some content here.", "text")
        ]
        nodes = split_nodes_blockquote([TextNode(text)])
        self.assertEqual([(n.text, n.text_type) for n in nodes], [(n.text, n.text_type) for n in expected_nodes])

    def test_no_blockquote(self):
        text = "No blockquote here."
        expected_nodes = [
            TextNode("No blockquote here.", "text")
        ]
        nodes = split_nodes_blockquote([TextNode(text)])
        self.assertEqual([(n.text, n.text_type) for n in nodes], [(n.text, n.text_type) for n in expected_nodes])

if __name__ == '__main__':
    unittest.main()