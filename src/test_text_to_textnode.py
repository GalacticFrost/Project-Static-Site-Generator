import unittest
from textnode import *

class TestTextToTextNodes(unittest.TestCase):

    def test_blockquote_markdown(self):
        text = "> This is a blockquote"
        expected = [
            TextNode("This is a blockquote", 'blockquote')
        ]
        result = text_to_textnodes(text)
        self.assertEqual(result, expected)

    def test_bold_and_link_combined(self):
        text = "**bold [link](https://example.com)**"
        expected = [
            TextNode("bold ", 'bold'),
            TextNode("link", 'link', "https://example.com"),
            TextNode("", 'bold')
        ]
        result = text_to_textnodes(text)
        self.assertEqual(result, expected)

    def test_escaped_asterisk_within_text(self):
        text = "This is a \\*literal asterisk*"
        expected = [
            TextNode("This is a *literal asterisk*", 'text')
        ]
        result = text_to_textnodes(text)
        self.assertEqual(result, expected)

    def test_escaped_backticks_within_text(self):
        text = "This is a \\`literal backtick`"
        expected = [
            TextNode("This is a `literal backtick`", 'text')
        ]
        result = text_to_textnodes(text)
        self.assertEqual(result, expected)

    def test_heading_markdowns(self):
        text = "# Heading 1\n## Heading 2\n### Heading 3"
        expected = [
        TextNode("Heading 1", "heading1", None),
        TextNode("Heading 2", "heading2", None),
        TextNode("Heading 3", "heading3", None)
        ]
        result = text_to_textnodes(text)
        self.assertEqual(result, expected)

    def test_incomplete_bold_pair(self):
        text = "This is **bold text without ending"
        expected = [
            TextNode("This is **bold text without ending", 'text')
        ]
        result = text_to_textnodes(text)
        self.assertEqual(result, expected)

    def test_incomplete_italic_pair(self):
        text = "This is *italic text without ending"
        expected = [
            TextNode("This is *italic text without ending", 'text')
        ]
        result = text_to_textnodes(text)
        self.assertEqual(result, expected)

    def test_italic_and_image_combined(self):
        text = "*italic ![image](https://example.com/image.png)*"
        expected = [
            TextNode("italic ", 'italic'),
            TextNode("image", 'image', "https://example.com/image.png"),
            TextNode("", 'italic')
        ]
        result = text_to_textnodes(text)
        self.assertEqual(result, expected)

    def test_italic_with_underscores(self):
        text = "_italic_ text with underscores"
        expected = [
            TextNode("italic", 'italic'),
            TextNode(" text with underscores", 'text')
        ]
        result = text_to_textnodes(text)
        self.assertEqual(result, expected)

    def test_link_with_italic_and_bold(self):
        text = "[**bold and _italic_**](https://example.com)"
        expected = [
            TextNode("bold and ", 'bold'),
            TextNode("italic", 'italic'),
            TextNode("", 'bold', "https://example.com")
        ]
        result = text_to_textnodes(text)
        self.assertEqual(result, expected)

    def test_mixed_content_with_escaped_chars(self):
        text = "Mixed content with **escaped \\*bold\\***, *italic*, and `code`."
        expected = [
            TextNode("Mixed content with ", 'text'),
            TextNode("escaped *bold*", 'bold'),
            TextNode(", ", 'text'),
            TextNode("italic", 'italic'),
            TextNode(", and ", 'text'),
            TextNode("code", 'code'),
            TextNode(".", 'text')
        ]
        result = text_to_textnodes(text)
        self.assertEqual(result, expected)

    def test_mixed_markdown(self):
        text = "This is **bold**, *italic*, `code`, and ![image](https://example.com/image.png)"
        expected = [
            TextNode("This is ", 'text'),
            TextNode("bold", 'bold'),
            TextNode(", ", 'text'),
            TextNode("italic", 'italic'),
            TextNode(", ", 'text'),
            TextNode("code", 'code'),
            TextNode(", and ", 'text'),
            TextNode("image", 'image', "https://example.com/image.png")
        ]
        result = text_to_textnodes(text)
        self.assertEqual(result, expected)

    def test_multiple_markdown(self):
        text = "This is **bold** and *italic* text"
        expected = [
            TextNode("This is ", 'text'),
            TextNode("bold", 'bold'),
            TextNode(" and ", 'text'),
            TextNode("italic", 'italic'),
            TextNode(" text", 'text')
        ]
        result = text_to_textnodes(text)
        self.assertEqual(result, expected)

    def test_multiple_links(self):
        text = "Check out these [links](https://boot.dev) and [more links](https://example.com)!"
        expected = [
            TextNode("Check out these ", 'text'),
            TextNode("links", 'link', "https://boot.dev"),
            TextNode(" and ", 'text'),
            TextNode("more links", 'link', "https://example.com"),
            TextNode("!", 'text')
        ]
        result = text_to_textnodes(text)
        self.assertEqual(result, expected, "The link node split function did not handle multiple links correctly.")

    def test_multiple_images(self):
        text = "Here are multiple ![first image](https://example.com/first.png) and ![second image](https://example.com/second.png)."
        expected = [
            TextNode("Here are multiple ", 'text'),
            TextNode("first image", 'image', "https://example.com/first.png"),
            TextNode(" and ", 'text'),
            TextNode("second image", 'image', "https://example.com/second.png"),
            TextNode(".", 'text')
        ]
        result = text_to_textnodes(text)
        self.assertEqual(result, expected, "The image node split function did not handle multiple images correctly.")

    def test_multiple_markdown_types_with_text(self):
        text = "Sample **bold text**, *italic text*, `code` and [link](https://example.com)."
        expected = [
            TextNode("Sample ", 'text'),
            TextNode("bold text", 'bold'),
            TextNode(", ", 'text'),
            TextNode("italic text", 'italic'),
            TextNode(", ", 'text'),
            TextNode("code", 'code'),
            TextNode(" and ", 'text'),
            TextNode("link", 'link', "https://example.com"),
            TextNode(".", 'text')
        ]
        result = text_to_textnodes(text)
        self.assertEqual(result, expected)

    def test_nested_markdown(self):
        text = "**bold *italic* text**"
        expected = [
            TextNode("bold ", 'bold'),
            TextNode("italic", 'italic'),
            TextNode(" text", 'bold')
        ]
        result = text_to_textnodes(text)
        self.assertEqual(result, expected)

    def test_only_bold_text(self):
        text = "**bold**"
        expected = [
            TextNode("bold", 'bold')
        ]
        result = text_to_textnodes(text)
        self.assertEqual(result, expected)

    def test_only_italic_text(self):
        text = "*italic*"
        expected = [
            TextNode("italic", 'italic')
        ]
        result = text_to_textnodes(text)
        self.assertEqual(result, expected)

    def test_single_bold_markdown(self):
        text = "This is **bold** text"
        expected = [
            TextNode("This is ", 'text'),
            TextNode("bold", 'bold'),
            TextNode(" text", 'text')
        ]
        result = text_to_textnodes(text)
        self.assertEqual(result, expected)

    def test_single_italic_markdown(self):
        text = "This is *italic* text"
        expected = [
            TextNode("This is ", 'text'),
            TextNode("italic", 'italic'),
            TextNode(" text", 'text')
        ]
        result = text_to_textnodes(text)
        self.assertEqual(result, expected)

    def test_split_text_to_link_nodes_with_text(self):
        text = "This is a [link](https://boot.dev) with text."
        expected = [
            TextNode("This is a ", 'text'),
            TextNode("link", 'link', "https://boot.dev"),
            TextNode(" with text.", 'text')
        ]
        result = text_to_textnodes(text)
        self.assertEqual(result, expected, "The link node split function did not produce the expected result with surrounding text.")

    def test_split_text_to_image_nodes_with_text(self):
        text = "Here is an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) in the middle."
        expected = [
            TextNode("Here is an ", 'text'),
            TextNode("image", 'image', "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" in the middle.", 'text')
        ]
        result = text_to_textnodes(text)
        self.assertEqual(result, expected, "The image node split function did not produce the expected result with surrounding text.")

if __name__ == '__main__':
    unittest.main()
