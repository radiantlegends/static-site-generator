import unittest
from textnode import TextNode, TextType
from splitnodes import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_node_bold(self):
        node = TextNode("This is text with a **bold** word.", TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node], "**", TextType.BOLD),
        [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word.", TextType.TEXT)
        ])
    
    def test_split_node_italic(self):
        node = TextNode("This is text with an _italic_ word.", TextType.TEXT)
        node2 = TextNode("This is text with another _italicized_ word.", TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node, node2], "_", TextType.ITALIC),
        [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word.", TextType.TEXT),
            TextNode("This is text with another ", TextType.TEXT),
            TextNode("italicized", TextType.ITALIC),
            TextNode(" word.", TextType.TEXT)
        ])
    
    def test_split_node_error_syntax(self):
        with self.assertRaises(Exception) as context:
            node = TextNode("This is **invalid Markdown syntax.", TextType.TEXT)
            split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertIn("Invalid Markdown syntax - matching delimiter not found.", str(context.exception))

class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_invalid_markdown(self):
        matches = extract_markdown_images(
            "This is ![] not valid markdown for an image."
        )
        self.assertListEqual([], matches)

    def test_multiple_images(self):
        matches = extract_markdown_images(
            "This is text with ![image1](https://i.imgur.com/zjjcJKZ.png) and ![image2](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image1", "https://i.imgur.com/zjjcJKZ.png"), ("image2", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_image_and_links(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and [link](https://www.boot.dev)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_invalid_markdown(self):
        matches = extract_markdown_links(
            "This is [] not valid markdown for links."
        )
        self.assertListEqual([], matches)

    def test_image_and_links(self):
        matches = extract_markdown_links(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and [link](https://www.boot.dev)"
        )
        self.assertListEqual([("link", "https://www.boot.dev")], matches)

class TestSplitNodesImage(unittest.TestCase):
    def test_single_image(self):
        node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) in the middle.", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        assertion = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" in the middle.", TextType.TEXT)
        ]
        self.assertListEqual(assertion, new_nodes)
    
    def test_multiple_images(self):
        node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        assertion = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png")
        ]
        self.assertListEqual(assertion, new_nodes)
    
    def test_image_start(self):
        node = TextNode("![image](https://i.imgur.com/zjjcJKZ.png) comes first.", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        assertion = [
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" comes first.", TextType.TEXT)
        ]
        self.assertListEqual(assertion, new_nodes)

    def test_image_end(self):
        node = TextNode("Image comes last ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        assertion = [
            TextNode("Image comes last ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")
        ]
        self.assertListEqual(assertion, new_nodes)

    def test_no_images(self):
        node = TextNode("This has no images.", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(new_nodes, [node])
    
    def test_empty_text(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(new_nodes, [node])
    
    def test_non_text_type(self):
        node = TextNode("This is bold.", TextType.BOLD)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(new_nodes, [node])
    
    def test_empty_alt_text(self):
        node = TextNode("This image is missing the alt text: ![](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        assertion = [
            TextNode("This image is missing the alt text: ", TextType.TEXT),
            TextNode("", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")
        ]
        self.assertListEqual(new_nodes, assertion)

    def test_adjacent_images(self):
        node = TextNode("![image](https://i.imgur.com/zjjcJKZ.png)![second image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        assertion = [
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png")
        ]
        self.assertListEqual(new_nodes, assertion)

    def test_image_with_link(self):
        node = TextNode("This image is accompanied by a [link](https://www.google.com/). ![Image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        assertion = [
            TextNode("This image is accompanied by a [link](https://www.google.com/). ", TextType.TEXT),
            TextNode("Image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")
        ]
        self.assertListEqual(new_nodes, assertion)

class TestSplitNodesLink(unittest.TestCase):
    def test_single_link(self):
        node = TextNode("This is text with a [link](https://www.google.com/) in the middle.", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        assertion = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://www.google.com/"),
            TextNode(" in the middle.", TextType.TEXT)
        ]
        self.assertListEqual(new_nodes, assertion)

    def test_multiple_links(self):
        node = TextNode("This is text with a [link](https://www.google.com/) and another [second link](https://www.youtube.com/)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        assertion = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://www.google.com/"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second link", TextType.LINK, "https://www.youtube.com/")
        ]
        self.assertListEqual(new_nodes, assertion)
    
    def test_link_start(self):
        node = TextNode("[Link](https://www.google.com/) comes first.", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        assertion = [
            TextNode("Link", TextType.LINK, "https://www.google.com/"),
            TextNode(" comes first.", TextType.TEXT)
        ]
        self.assertListEqual(new_nodes, assertion)

    def test_link_end(self):
        node = TextNode("Link comes [last](https://www.google.com/)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        assertion = [
            TextNode("Link comes ", TextType.TEXT),
            TextNode("last", TextType.LINK, "https://www.google.com/")
        ]
        self.assertListEqual(new_nodes, assertion)

    def test_no_links(self):
        node = TextNode("This has no links.", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(new_nodes, [node])
    
    def test_empty_text(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(new_nodes, [node])
    
    def test_non_text_type(self):
        node = TextNode("This is bold.", TextType.BOLD)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(new_nodes, [node])
    
    def test_empty_alt_text(self):
        node = TextNode("This link is missing the text: [](https://www.google.com/)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        assertion = [
            TextNode("This link is missing the text: ", TextType.TEXT),
            TextNode("", TextType.LINK, "https://www.google.com/")
        ]
        self.assertListEqual(new_nodes, assertion)

    def test_adjacent_links(self):
        node = TextNode("[Link1](https://www.google.com/)[Link2](https://www.youtube.com/)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        assertion = [
            TextNode("Link1", TextType.LINK, "https://www.google.com/"),
            TextNode("Link2", TextType.LINK, "https://www.youtube.com/")
        ]
        self.assertListEqual(new_nodes, assertion)
    
    def test_links_with_images(self):
        node = TextNode("This [link](https://www.google.com/) is accompanied by an image. ![Image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        assertion = [
            TextNode("This ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://www.google.com/"),
            TextNode(" is accompanied by an image. ![Image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        ]
        self.assertListEqual(new_nodes, assertion)

class TestTextToTextNode(unittest.TestCase):
    def test_text_to_text_node(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ]
        )

if __name__ == "main":
    unittest.main()