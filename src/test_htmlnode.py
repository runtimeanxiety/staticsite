import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_multiple(self):
        node = HTMLNode(
            tag="a",
            value="link",
            props={
                "href": "https://google.com",
                "target": "_blank",
            },
        )
        self.assertEqual(
            node.props_to_html(), ' href="https://google.com" target="_blank"'
        )

    def test_props_to_html_empty(self):
        node = HTMLNode(tag="p", value="hello", props={})
        self.assertEqual(node.props_to_html(), "")

    def test_repr(self):
        node = HTMLNode(tag="p", value="hello", props={"class": "text-bold"})
        output = repr(node)
        self.assertIn("p", output)  # should show the tag
        self.assertIn("hello", output)  # should show the value
        self.assertIn("class", output)  # should show the props key
        self.assertIn("text-bold", output)  # should show the props value


if __name__ == "__main__":
    unittest.main()
