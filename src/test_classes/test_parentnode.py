import unittest

from leafnode import LeafNode
from parentnode import ParentNode

class TestParentNode(unittest.TestCase):

    def test_basic_functionality(self):
        node = ParentNode("div", [LeafNode("p", "test")])
        self.assertEqual(node.to_html(), "<div><p>test</p></div>")
    
    def test_no_tag_provided(self):
        with self.assertRaises(ValueError) as context:
            node = ParentNode(None, [LeafNode("b", "bold text")])
            node.to_html()
        self.assertEqual(str(context.exception), "ParentNode requires a tag.")
    
    def test_no_children_provided(self):
        with self.assertRaises(ValueError) as context:
            node = ParentNode("div")
            node.to_html()
        self.assertEqual(str(context.exception), "Parent node must have children.")