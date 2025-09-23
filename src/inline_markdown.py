from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            parts = node.text.split(delimiter)

            # Must have odd number of parts → balanced delimiters
            if len(parts) % 2 == 0:
                raise Exception("Invalid Markdown syntax")

            for i, part in enumerate(parts):
                if i % 2 == 0:
                    new_nodes.append(TextNode(part, TextType.TEXT))
                else:
                    new_nodes.append(TextNode(part, text_type))
        else:
            new_nodes.append(node)
    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\]]*)\]\(([^)]+)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", text)
    return matches
