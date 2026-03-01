import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click here!", {"href": "https://www.boot.dev/"})
        self.assertEqual(node.to_html(), '<a href="https://www.boot.dev/">Click here!</a>')
    def test_leaf_to_html_img(self):
        node = LeafNode("img", "This is a picture.", {"src": "https://www.boot.dev/img/bootdev-logo-full-small.webp"})

if __name__ == "main":
    unittest.main()