import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_isNone(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_propsisOne(self):
        node = HTMLNode(props={"href": "https://google.com"})
        self.assertEqual(node.props_to_html(), ' href="https://google.com"')

    def test_propsisTwo(self):
        node = HTMLNode(props={"href": "https://google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://google.com" target="_blank"')
    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Hello, world!")
        self.assertEqual(node.to_html(), "<a>Hello, world!</a>")

    def test_lead_to_html_none(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_lead_to_html_withprop(self):
        node = LeafNode("a", "Hello, world!", props={"href": "https://google.com"})
        self.assertEqual(node.to_html(), '<a href="https://google.com">Hello, world!</a>')

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren1(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_nesting_depth(self):
        node = LeafNode("p", "Rhubarb")
        first_parent = ParentNode("a", [node])
        second_parent = ParentNode("b", [first_parent])
        third_parent = ParentNode("i", [second_parent])
        self.assertEqual(
            third_parent.to_html(),
            "<i><b><a><p>Rhubarb</p></a></b></i>",
        )

    def test_parent_props(self):
        node = LeafNode("a","Hello, world!", props={"href": "https://google.com"})
        first_parent = ParentNode("a", [node])
        second_parent = ParentNode("b", [first_parent])
        third_parent = ParentNode("i", [second_parent])
        self.assertEqual(
            third_parent.to_html(),
            '<i><b><a><a href="https://google.com">Hello, world!</a></a></b></i>'
        )

    def test_mixed_children(self):
        node = LeafNode("p", "Rhubarb")
        parent = ParentNode("b", [])
        children = ParentNode("a", [node, parent])
        self.assertEqual(
            children.to_html(),
            "<a><p>Rhubarb</p><b></b></a>",
        )

    def test_tag_value_error(self):
        node = LeafNode("p", "Rhubarb")
        first_parent = ParentNode(None, [node])
        second_parent = ParentNode("b", [first_parent])
        with self.assertRaises(ValueError):
            second_parent.to_html()

    def test_children_value_error(self):
        node = LeafNode("p", "Rhubarb")
        first_parent = ParentNode("a", None)
        second_parent = ParentNode("b", [first_parent])
        with self.assertRaises(ValueError):
            second_parent.to_html()


if __name__ == "__main__":
    unittest.main()