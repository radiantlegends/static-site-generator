import re
from src.text_node import TextType, TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type is not TextType.TEXT:
            new_nodes.append(old_node)
            continue
        text_split = old_node.text.split(delimiter)
        if len(text_split) == 1:
            new_nodes.append(old_node)
            continue
        if len(text_split) % 2 == 0:
            raise Exception("Invalid Markdown syntax - matching delimiter not found.")
        nodes = []
        for i, part in enumerate(text_split):
            if part == "":
                continue
            if i % 2 == 0:
                nodes.append(TextNode(part, TextType.TEXT))
            else:
                nodes.append(TextNode(part, text_type))
        new_nodes.extend(nodes)
    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<![!])\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type is not TextType.TEXT:
            new_nodes.append(old_node)
            continue
        current_text = old_node.text
        images = extract_markdown_images(current_text)
        if (len(images) == 0):
            new_nodes.append(old_node)
            continue
        for (alt, url) in images:
            text_split = current_text.split(f"![{alt}]({url})")
            if text_split[0] != "":
                new_nodes.append(TextNode(text_split[0], TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            current_text = text_split[1]
        if (current_text != ""):
            new_nodes.append(TextNode(current_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type is not TextType.TEXT:
            new_nodes.append(old_node)
            continue
        current_text = old_node.text
        links = extract_markdown_links(current_text)
        if(len(links) == 0):
            new_nodes.append(old_node)
            continue
        for(text, url) in links:
            text_split = current_text.split(f"[{text}]({url})")
            if text_split[0] != "":
                new_nodes.append(TextNode(text_split[0], TextType.TEXT))
            new_nodes.append(TextNode(text, TextType.LINK, url))
            current_text = text_split[1]
        if current_text != "":
            new_nodes.append(TextNode(current_text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_link(new_nodes)
    new_nodes = split_nodes_image(new_nodes)
    return new_nodes