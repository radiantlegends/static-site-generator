import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        nodes = [
            HTMLNode(None, "This is raw text."),
            HTMLNode("p", "This is a paragraph."),
            HTMLNode("a", "This is a link.", None, {"href": "https://www.google.com", "target": "_blank"}),
            HTMLNode("a", "This is a link.", None, {"href": "https://www.boot.dev/"})
        ]

        self.assertEqual(nodes[0], nodes[0])
        self.assertNotEqual(nodes[0], nodes[1])
        self.assertNotEqual(nodes[2], nodes[3])

if __name__ == "main":
    unittest.main()