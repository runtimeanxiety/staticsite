import unittest
from inline_markdown import extract_markdown_images, extract_markdown_links, split_nodes_delimiter
from textnode import TextNode, TextType

class TestInlineMarkdown(unittest.TestCase):
    def test_code_basic(self):
        node = TextNode("This is `code` text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "code")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text, " text")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

    def test_no_delimiter(self):
        node = TextNode("Plain text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "Plain text")

    def test_multiple_delimiters(self):
        node = TextNode("`one` and `two`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 5)
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[3].text_type, TextType.CODE)

    def test_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        self.assertEqual(nodes[1].text_type, TextType.BOLD)
        self.assertEqual(nodes[3].text_type, TextType.ITALIC)

    def test_unbalanced_delimiters(self):
        node = TextNode("This is `broken", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE)
    
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdown_images_single(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(
            [("image", "https://i.imgur.com/zjjcJKZ.png")],
            matches
        )

    def test_extract_markdown_images_multiple(self):
        matches = extract_markdown_images(
            "![one](url1.png) and ![two](url2.jpg)"
        )
        self.assertListEqual(
            [("one", "url1.png"), ("two", "url2.jpg")],
            matches
        )

    def test_extract_markdown_images_none(self):
        matches = extract_markdown_images("Just plain text")
        self.assertListEqual([], matches)
    
    def test_extract_markdown_links_single(self):
        matches = extract_markdown_links(
            "This is a [link](https://example.com)"
        )
        self.assertListEqual(
            [("link", "https://example.com")],
            matches
        )

    def test_extract_markdown_links_multiple(self):
        matches = extract_markdown_links(
            "Go [here](url1) or [there](url2)"
        )
        self.assertListEqual(
            [("here", "url1"), ("there", "url2")],
            matches
        )

    def test_extract_markdown_links_none(self):
        matches = extract_markdown_links("No links here!")
        self.assertListEqual([], matches)

if __name__ == "__main__":
    unittest.main()
