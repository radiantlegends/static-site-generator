import unittest
from src.html_node import HTMLNode, LeafNode, ParentNode

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



class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click here!", {"href": "https://www.boot.dev/"})
        self.assertEqual(node.to_html(), '<a href="https://www.boot.dev/">Click here!</a>')
    def test_leaf_to_html_img(self):
        node = LeafNode("img", "This is a picture.", {"src": "https://www.boot.dev/img/bootdev-logo-full-small.webp"})



class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
    
    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span><b>grandchild</b></span></div>")


        
if __name__ == "main":
    unittest.main()