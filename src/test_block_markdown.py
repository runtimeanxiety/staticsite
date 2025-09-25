import unittest
from block_markdown import markdown_to_blocks
from blocknode import block_to_block_type, BlockType

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

    - This is a list
    - with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_empty_string(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_whitespace_and_newlines(self):
        md = "   \n\n\n   \n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_multiple_paragraphs(self):
        md = """
    First paragraph

    Second paragraph


    Third paragraph
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "First paragraph",
                "Second paragraph",
                "Third paragraph",
            ],
        )

    def test_strip_whitespace_in_block(self):
        md = """
    This is a paragraph with spaces around it    

    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a paragraph with spaces around it"])

    def test_paragraph_and_list(self):
        md = """
    This is a paragraph

    - Item one
    - Item two
    - Item three
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is a paragraph",
                "- Item one\n- Item two\n- Item three",
            ],
        )
    
    def test_heading(self):
        block = "# This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_code_block(self):
        block = """```
print("Hello, world!")
```"""
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_quote_block(self):
        block = "> This is a quote\n> Another line of quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_unordered_list(self):
        block = "- Item one\n- Item two\n- Item three"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_ordered_list(self):
        block = "1. First\n2. Second\n3. Third"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_paragraph(self):
        block = "This is just a normal paragraph of text."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_invalid_ordered_list(self):
        # Numbers must start at 1 and go up by 1 each line
        block = "1. First\n3. Wrong number"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_invalid_unordered_list(self):
        # Missing space after '-'
        block = "-Item one\n-Item two"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()