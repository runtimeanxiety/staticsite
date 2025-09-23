import unittest
from inline_markdown import extract_markdown_images, extract_markdown_links, split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_text_nodes
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
    
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_single_image(self):
        node = TextNode("Here is ![alt](url.png)", TextType.TEXT)
        result = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Here is ", TextType.TEXT),
                TextNode("alt", TextType.IMAGE, "url.png"),
            ],
            result,
        )

    def test_multiple_images(self):
        node = TextNode("![one](url1) and ![two](url2)", TextType.TEXT)
        result = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("", TextType.TEXT),
                TextNode("one", TextType.IMAGE, "url1"),
                TextNode(" and ", TextType.TEXT),
                TextNode("two", TextType.IMAGE, "url2"),
            ],
            result,
        )

    def test_single_link(self):
        node = TextNode("Click [here](url.com)", TextType.TEXT)
        result = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Click ", TextType.TEXT),
                TextNode("here", TextType.LINK, "url.com"),
            ],
            result,
        )

    def test_no_links_or_images(self):
        node = TextNode("Just plain text", TextType.TEXT)
        self.assertEqual(split_nodes_image([node]), [node])
        self.assertEqual(split_nodes_link([node]), [node])
    
    def test_full_markdown(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_text_nodes(text)
        self.assertListEqual(
            nodes,
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
            ],
        )


if __name__ == "__main__":
    unittest.main()
