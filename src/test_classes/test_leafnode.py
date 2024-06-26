import unittest
from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):

    def test_no_self_value(self):
        with self.assertRaises(ValueError):
            node = LeafNode(tag="p")
            node.to_html()

    def test_no_self_tag(self):
        node = LeafNode(value='This is a text test')
        self.assertEqual(node.to_html(), 'This is a text test')

    def test_self_tag_h_p_b_i_code(self):
        node_p = LeafNode(tag='p', value='This is a paragraph')
        node_code = LeafNode(tag='code', value='This is a piece of code')
        node_bold = LeafNode(tag='b', value='This is bold text')
        
        self.assertEqual(node_p.to_html(), '<p>This is a paragraph</p>')
        self.assertEqual(node_code.to_html(), '<code>This is a piece of code</code>')
        self.assertEqual(node_bold.to_html(), '<b>This is bold text</b>')

    def test_self_tag_a(self):
        node = LeafNode(tag='a', value='Click the link!', props={'href': 'https://github.com/GalacticFrost'})
        self.assertEqual(node.to_html(), '<a href="https://github.com/GalacticFrost">Click the link!</a>')

    def test_self_tag_img(self):
        node = LeafNode(tag='img', props={'src': 'url/of/image.jpeg', 'alt': 'Figure heading'})
        self.assertEqual(node.to_html(), '<img src="url/of/image.jpeg" alt="Figure heading"></img>')

    def test_self_tag_blockquote(self):
        node = LeafNode(tag='blockquote', value='This is a quote')
        self.assertEqual(node.to_html(), '<blockquote>\n   This is a quote\n</blockquote>')

    def test_ul_list(self):
        node = LeafNode(tag='ul', value=['Item 1', 'Item 2', 'Item 3'])
        self.assertEqual(node.to_html(), '<ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul>')

    def test_ol_list(self):
        node = LeafNode(tag='ol', value=['First', 'Second', 'Third'])
        self.assertEqual(node.to_html(), '<ol><li>First</li><li>Second</li><li>Third</li></ol>')
        
if __name__ == "__main__":
    unittest
