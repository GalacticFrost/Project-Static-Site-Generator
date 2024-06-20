import unittest
from textnode import *

class TestSplitNodesImagesLinks(unittest.TestCase):

    def test_no_images(self):
        input_text = [TextNode("This is just text.", "text")]
        expected_output = [TextNode("This is just text.", "text")]
        self.assertEqual(split_nodes_images(input_text), expected_output)
    
    def test_one_image(self):
        input_text = [TextNode("This is text with one ![image](http://example.com/image1.png).", "text")]
        expected_output = [
            TextNode("This is text with one ", "text"),
            TextNode("image", "image", "http://example.com/image1.png"),
            TextNode(".", "text")
        ]
        self.assertEqual(split_nodes_images(input_text), expected_output)

    def test_multiple_images(self):
        input_text = [TextNode("This is text with an ![image1](http://example.com/image1.png) and another ![image2](http://example.com/image2.png).", "text")]
        expected_output = [
            TextNode("This is text with an ", "text"),
            TextNode("image1", "image", "http://example.com/image1.png"),
            TextNode(" and another ", "text"),
            TextNode("image2", "image", "http://example.com/image2.png"),
            TextNode(".", "text")
        ]
        self.assertEqual(split_nodes_images(input_text), expected_output)
        
    def test_starts_with_image(self):
        input_text = [TextNode("![image](http://example.com/image.png) starts with an image.", "text")]
        expected_output = [
            TextNode("image", "image", "http://example.com/image.png"),
            TextNode(" starts with an image.", "text")
        ]
        self.assertEqual(split_nodes_images(input_text), expected_output)
        
    def test_no_links(self):
        input_text = [TextNode("This is just text.", "text")]
        expected_output = [TextNode("This is just text.", "text")]
        self.assertEqual(split_nodes_links(input_text), expected_output)
    
    def test_one_link(self):
        input_text = [TextNode("This is text with one [link](http://example.com).", "text")]
        expected_output = [
            TextNode("This is text with one ", "text"),
            TextNode("link", "link", "http://example.com"),
            TextNode(".", "text")
        ]
        self.assertEqual(split_nodes_links(input_text), expected_output)
        
    def test_multiple_links(self):
        input_text = [TextNode("This is text with a [link1](http://example1.com) and another [link2](http://example2.com).", "text")]
        expected_output = [
            TextNode("This is text with a ", "text"),
            TextNode("link1", "link", "http://example1.com"),
            TextNode(" and another ", "text"),
            TextNode("link2", "link", "http://example2.com"),
            TextNode(".", "text")
        ]
        self.assertEqual(split_nodes_links(input_text), expected_output)
        
    def test_starts_with_link(self):
        input_text = [TextNode("[link](http://example.com) starts with a link.", "text")]
        expected_output = [
            TextNode("link", "link", "http://example.com"),
            TextNode(" starts with a link.", "text")
        ]
        self.assertEqual(split_nodes_links(input_text), expected_output)

if __name__ == '__main__':
    unittest.main()
    
