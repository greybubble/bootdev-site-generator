import unittest
from parentnode import ParentNode
from leafnode import LeafNode

class testParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        print("********")
        print("test_to_html_with_children")
        print("********")
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        print("********")
        print("test_to_html_with_grandchildren")
        print("********")
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )