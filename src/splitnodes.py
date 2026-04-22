from textnode import TextType, TextNode
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type is not TextType.TEXT:
            new_nodes.append(old_node)
        text_split = old_node.text.split(delimiter)
        if len(text_split) < 3:
            raise Exception("Invalid Markdown syntax - matching delimiter not found.")
        nodes = [
            TextNode(text_split[0], TextType.TEXT),
            TextNode(text_split[1], text_type),
            TextNode(text_split[2], TextType.TEXT)
        ]
        new_nodes.extend(nodes)
    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"[^!]\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")