from enum import Enum
from htmlnode import HTMLNode, ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import text_to_text_nodes

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
    
def markdown_to_blocks(markdown):
    raw_blocks = markdown.split("\n\n")
    blocks = []
    for block in raw_blocks:
        lines = block.split("\n")
        cleaned_lines = []
        for line in lines:
            line = line.strip()
            if line != "":
                cleaned_lines.append(line)
        if cleaned_lines:
            blocks.append("\n".join(cleaned_lines))
    return blocks

def block_to_block_type(markdown):

    # check for heading
    if markdown.startswith("#"):
        parts = markdown.split(" ", 1)
        if len(parts) == 2:
            hashes, text = parts
            if 1 <= len(hashes) <= 6 and hashes == "#" * len(hashes):
                return BlockType.HEADING

    # check if code        
    if markdown.startswith("```") and markdown.endswith("```"):
        return BlockType.CODE
    
    # check if quote, ordered_list, or unordered_list
    lines = markdown.split("\n")
    is_quote = True
    is_unordered = True
    is_ordered = True

    for index, line in enumerate(lines):
        if not line.startswith(">"):
            is_quote = False
        if not line.startswith("- "):
            is_unordered = False
        expected_number = index + 1
        expected_start = f"{expected_number}. "
        if not line.startswith(expected_start):
            is_ordered = False

    if is_quote:
        return BlockType.QUOTE
    if is_unordered:
        return BlockType.UNORDERED_LIST
    if is_ordered:
        return BlockType.ORDERED_LIST
    
    # all else fails
    return BlockType.PARAGRAPH

def text_to_children(text):
    text_nodes = text_to_text_nodes(text)
    children = []
    for node in text_nodes:
        html_node = text_node_to_html_node(node)
        children.append(html_node)
    return children


def handle_paragraph(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    return ParentNode("p", children=text_to_children(paragraph))

def handle_heading(block):
    hashes, text = block.split(" ", 1)
    level = min(len(hashes), 6)
    return ParentNode(f"h{level}", children=text_to_children(text))

def handle_code(block):
    if not (block.startswith("```") and block.endswith("```")):
        raise ValueError("Invalid code block")
    code_content = block[3:-3].strip("\n")
    raw_text_node = TextNode(code_content, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code_node = ParentNode("code", [child])
    return ParentNode("pre", [code_node])

def handle_quote(block):
    lines = []
    for line in block.split("\n"):
        if not line.startswith(">"):
            raise ValueError("Invalid blockquote line: " + line)
        cleaned = line[1:].strip()
        lines.append(cleaned)

    quote_text = " ".join(lines)
    return HTMLNode("blockquote", children=text_to_children(quote_text))

def handle_unordered_list(block):
    lines = block.split("\n")
    items = []
    for line in lines:
        cleaned = line.lstrip("*- ").strip()
        items.append(cleaned)
    li_nodes = []
    for item in items:
        children = text_to_children(item)
        li_node = ParentNode("li", children=children)
        li_nodes.append(li_node)
    return ParentNode("ul", children=li_nodes)


def handle_ordered_list(block):
    lines = block.split("\n")
    items = []
    for line in lines:
        parts = line.split(". ", 1)
        if len(parts) < 2:
            raise ValueError(f"Invalid ordered list item: {line}")
        item_text = parts[1].strip()
        items.append(item_text)
    li_nodes = []
    for item in items:
        children = text_to_children(item)
        li_node = ParentNode("li", children=children)
        li_nodes.append(li_node)
    return ParentNode("ol", children=li_nodes)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return handle_paragraph(block)
    elif block_type == BlockType.HEADING:
        return handle_heading(block)
    elif block_type == BlockType.CODE:
        return handle_code(block)
    elif block_type == BlockType.QUOTE:
        return handle_quote(block)
    elif block_type == BlockType.UNORDERED_LIST:
        return handle_unordered_list(block)
    elif block_type == BlockType.ORDERED_LIST:
        return handle_ordered_list(block)
    else:
        raise Exception(f"Unknown block type: {block_type}")

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        child = block_to_html_node(block)
        children.append(child)
    return ParentNode("div", children, None)

