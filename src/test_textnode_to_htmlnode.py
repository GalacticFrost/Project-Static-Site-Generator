import unittest
from textnode import TextNode
from textnode_to_htmlnode import textnode_to_htmlnode

class TestTextNodeToHTMLNode(unittest.TestCase):

    def setUp(self):
        self.text1 = TextNode("This is a bold text", "bold")
        self.text2 = TextNode("This is plain text", 'text')
        self.text3 = TextNode("This is a link", "link", "boot.dev")
        self.text4 = TextNode("This is an image", "image", "boot.dev")

    def test_bold_text(self):
        result = textnode_to_htmlnode(self.text1)
        self.assertEqual(result.to_html(), "<b>This is a bold text</b>")

    def test_plain_text(self):
        result = textnode_to_htmlnode(self.text2)
        self.assertEqual(result.to_html(), "This is plain text")

    def test_link(self):
        result = textnode_to_htmlnode(self.text3)
        self.assertEqual(result.to_html(), '<a href="boot.dev">This is a link</a>')

    def test_image(self):
        result = textnode_to_htmlnode(self.text4)
        self.assertEqual(result.to_html(), '<img src="boot.dev" alt="This is an image"></img>')

if __name__ == '__main__':
    unittest.main()
