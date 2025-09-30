import unittest
from block_markdown import BlockType, markdown_to_blocks, block_to_block_type, markdown_to_html_node

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

    def test_markdown_to_blocks(self):
        md = "# Heading\n\nParagraph text\n\n- Item 1\n- Item 2"
        blocks = markdown_to_blocks(md)
        self.assertEqual(len(blocks), 3)
        self.assertEqual(blocks[0], "# Heading")
        self.assertEqual(blocks[1], "Paragraph text")
        self.assertEqual(blocks[2], "- Item 1\n- Item 2")

    def test_block_to_block_type(self):
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("```code```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("> Quote line"), BlockType.QUOTE)
        self.assertEqual(block_to_block_type("- Item"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("1. First\n2. Second"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("Just text"), BlockType.PARAGRAPH)

    def test_markdown_to_html_node_paragraph(self):
        md = "This is a paragraph."
        node = markdown_to_html_node(md)
        self.assertEqual(node.tag, "div")
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].tag, "p")

    def test_markdown_to_html_node_heading(self):
        md = "# Heading"
        node = markdown_to_html_node(md)
        self.assertEqual(node.children[0].tag, "h1")

    def test_markdown_to_html_node_code(self):
        md = "```code block```"
        node = markdown_to_html_node(md)
        self.assertEqual(node.children[0].tag, "pre")
        self.assertEqual(node.children[0].children[0].tag, "code")

    def test_markdown_to_html_node_quote(self):
        md = "> Quote line"
        node = markdown_to_html_node(md)
        self.assertEqual(node.children[0].tag, "blockquote")

    def test_markdown_to_html_node_unordered_list(self):
        md = "- Item 1\n- Item 2"
        node = markdown_to_html_node(md)
        self.assertEqual(node.children[0].tag, "ul")
        self.assertEqual(len(node.children[0].children), 2)
        self.assertEqual(node.children[0].children[0].tag, "li")

    def test_markdown_to_html_node_ordered_list(self):
        md = "1. First\n2. Second"
        node = markdown_to_html_node(md)
        self.assertEqual(node.children[0].tag, "ol")
        self.assertEqual(len(node.children[0].children), 2)
        self.assertEqual(node.children[0].children[0].tag, "li")

if __name__ == "__main__":
    unittest.main()