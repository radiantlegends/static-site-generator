import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        nodes = [
            TextNode("This is a text node", TextType.BOLD),
            TextNode("This is another text node", TextType.ITALIC),
            TextNode("This is a link node", TextType.LINK, "https://www.boot.dev/"),
            TextNode("This is a link node", TextType.LINK)
        ]
        
        self.assertEqual(nodes[0], nodes[0])
        self.assertNotEqual(nodes[0], nodes[1])
        self.assertNotEqual(nodes[0], nodes[2])
        self.assertNotEqual(nodes[2], nodes[3])

if __name__ == "__main__":
    unittest.main()