from enum import Enum
from block_markdown import markdown_to_blocks

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

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