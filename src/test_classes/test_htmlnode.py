import unittest
from htmlnode import *

class TestHTMLNode(unittest.TestCase):

    def test_props_to_html_no_props (self):

        node = HTMLNode(tag="a")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_with_props(self):

        node1 = HTMLNode(props={"herf": "google.com"})
        node2 = HTMLNode(props={"alt": "Image"})
        node3 = HTMLNode(props={"title" : "Sentence"})

        self.assertEqual(node1.props_to_html(), " herf=\"google.com\"")
        self.assertEqual(node2.props_to_html(), " alt=\"Image\"")
        self.assertEqual(node3.props_to_html(), " title=\"Sentence\"")

if __name__ == "__main__":
    unittest.main()