import unittest
from textnode import *

class TestLinkAndImageMarkdownExtract(unittest.TestCase):

    def test_extract_markdown_link(self):
        # Test case 1: Simple link
        markdown_text = "[OpenAI](https://www.openai.com)"
        expected_output = [("OpenAI", "https://www.openai.com")]
        self.assertEqual(extract_markdown_links(markdown_text), expected_output)

        # Test case 2: Multiple links
        markdown_text = "[Google](https://www.google.com) and [Bing](https://www.bing.com)"
        expected_output = [("Google", "https://www.google.com"), ("Bing", "https://www.bing.com")]
        self.assertEqual(extract_markdown_links(markdown_text), expected_output)

        # Test case 3: Link with title
        markdown_text = "[GitHub](https://github.com \"GitHub Homepage\")"
        expected_output = [("GitHub", "https://github.com")]
        self.assertEqual(extract_markdown_links(markdown_text), expected_output)

        # Test case 4: Link with special characters
        markdown_text = "[Example](https://example.com/path?arg=value&arg2=value2)"
        expected_output = [("Example", "https://example.com/path?arg=value&arg2=value2")]
        self.assertEqual(extract_markdown_links(markdown_text), expected_output)

        # Test case 5: No links
        markdown_text = "This is a text without any links."
        expected_output = []
        self.assertEqual(extract_markdown_links(markdown_text), expected_output)

    def test_extract_markdown_image(self):
        # Test case 1: Simple image
        markdown_text = "![alt text](https://example.com/image.jpg)"
        expected_output = [("alt text", "https://example.com/image.jpg")]
        self.assertEqual(extract_markdown_images(markdown_text), expected_output)

        # Test case 2: Multiple images
        markdown_text = "![first image](https://example.com/image1.jpg) ![second image](https://example.com/image2.jpg)"
        expected_output = [("first image", "https://example.com/image1.jpg"), ("second image", "https://example.com/image2.jpg")]
        self.assertEqual(extract_markdown_images(markdown_text), expected_output)

        # Test case 3: Image with title
        markdown_text = "![alt text](https://example.com/image.jpg \"Image Title\")"
        expected_output = [("alt text", "https://example.com/image.jpg")]
        self.assertEqual(extract_markdown_images(markdown_text), expected_output)

        # Test case 4: Image with special characters
        markdown_text = "![special image](https://example.com/path/to/image?arg=value&arg2=value2.jpg)"
        expected_output = [("special image", "https://example.com/path/to/image?arg=value&arg2=value2.jpg")]
        self.assertEqual(extract_markdown_images(markdown_text), expected_output)

        # Test case 5: No images
        markdown_text = "This is a text without any images."
        expected_output = []
        self.assertEqual(extract_markdown_images(markdown_text), expected_output)

if __name__ == '__main__':
    unittest.main()