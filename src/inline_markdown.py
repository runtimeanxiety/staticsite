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

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        matches = extract_markdown_images(text)

        if not matches:
            new_nodes.append(node)
            continue

        pos = 0
        for alt, url in matches:
            pattern = f"![{alt}]({url})"
            idx = text.find(pattern, pos)

            # Add text before the image
            before = text[pos:idx]
            new_nodes.append(TextNode(before, TextType.TEXT))

            # Add the image node
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))

            # Move position to end of this match
            pos = idx + len(pattern)

        # Add any remaining text after the last image
        if pos < len(text):
            after = text[pos:]
            if after:
                new_nodes.append(TextNode(after, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        matches = extract_markdown_links(text)

        if not matches:
            new_nodes.append(node)
            continue

        pos = 0
        for anchor, url in matches:
            pattern = f"[{anchor}]({url})"
            idx = text.find(pattern, pos)

            # Text before the link
            before = text[pos:idx]
            new_nodes.append(TextNode(before, TextType.TEXT))

            # The link node
            new_nodes.append(TextNode(anchor, TextType.LINK, url))

            pos = idx + len(pattern)

        # Any trailing text
        if pos < len(text):
            after = text[pos:]
            if after:
                new_nodes.append(TextNode(after, TextType.TEXT))

    return new_nodes