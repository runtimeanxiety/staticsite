import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


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
    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com">Click me!</a>'
        )
    
    def test_leaf_to_html_with_multiple_props(self):
        node = LeafNode("img", "alt text", {"src": "image.png", "width": "100"})
        self.assertEqual(
            node.to_html(),
            '<img src="image.png" width="100">alt text</img>'
        )

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_with_one_child(self):
        child = LeafNode("span", "child")
        parent = ParentNode("div", [child])
        self.assertEqual(parent.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_multiple_children(self):
        children = [
            LeafNode("li", "one"),
            LeafNode("li", "two"),
        ]
        parent = ParentNode("ul", children)
        self.assertEqual(parent.to_html(), "<ul><li>one</li><li>two</li></ul>")

    def test_to_html_with_grandchildren(self):
        grandchild = LeafNode("b", "grandchild")
        child = ParentNode("span", [grandchild])
        parent = ParentNode("div", [child])
        self.assertEqual(parent.to_html(), "<div><span><b>grandchild</b></span></div>")

    def test_to_html_mixed_children(self):
        children = [
            LeafNode("b", "Bold"),
            LeafNode(None, " and normal"),
        ]
        parent = ParentNode("p", children)
        self.assertEqual(parent.to_html(), "<p><b>Bold</b> and normal</p>")

    def test_to_html_raises_no_tag(self):
        child = LeafNode("span", "child")
        parent = ParentNode(None, [child])
        with self.assertRaises(ValueError):
            parent.to_html()

    def test_to_html_raises_no_children(self):
        parent = ParentNode("div", [])
        with self.assertRaises(ValueError):
            parent.to_html()

    def test_to_html_with_props(self):
        child = LeafNode("span", "child")
        parent = ParentNode("div", [child], {"class": "container"})
        self.assertEqual(parent.to_html(), '<div class="container"><span>child</span></div>')



if __name__ == "__main__":
    unittest.main()
