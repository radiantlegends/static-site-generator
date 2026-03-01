import unittest

from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        nodes = [
            TextNode("This is a text node.", TextType.BOLD),
            TextNode("This is another text node.", TextType.ITALIC),
            TextNode("This is a link node.", TextType.LINK, "https://www.boot.dev/"),
            TextNode("This is a link node.", TextType.LINK)
        ]
        
        self.assertEqual(nodes[0], nodes[0])
        self.assertNotEqual(nodes[0], nodes[1])
        self.assertNotEqual(nodes[0], nodes[2])
        self.assertNotEqual(nodes[2], nodes[3])

    def test_text(self):
        node = TextNode("This is a text node.", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node.")

if __name__ == "__main__":
    unittest.main()