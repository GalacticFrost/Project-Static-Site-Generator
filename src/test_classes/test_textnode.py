import unittest
from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):

        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        node3 = TextNode("Text", "strike", None)
        node4 = TextNode("Text", "strike", None)
        node5 = TextNode("Text","strike", None)
        node6 = TextNode("Text ", " bold", "boot.dev")
        node7 = TextNode("Text ", " bold", "boot.dev")

        try:

            self.assertEqual(node, node2)
            self.assertEqual(node3,node5)
            self.assertEqual(node6,node7)
            self.assertEqual(node3,node4)

        except AssertionError:

            print("TextNodes do not match")


if __name__ == "__main__":
    unittest.main()
