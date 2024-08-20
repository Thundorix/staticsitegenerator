import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):

    def test_htmlnode_values(self):
        # Test node properties
        node = HTMLNode("div", "I wish I could read")
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "I wish I could read")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_htmlnode_props_to_html(self):
        # Test with multiple props
        html_node = HTMLNode(tag="a", value="Link", props={"href": "https://www.google.com", "target": "_blank"})
        expected_output = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(html_node.props_to_html(), expected_output)

        # Test with no props
        html_node_no_props = HTMLNode(tag="a", value="Link", props=None)
        expected_output_no_props = ''
        self.assertEqual(html_node_no_props.props_to_html(), expected_output_no_props)
    
        # Test with a single prop
        html_node_single_prop = HTMLNode(tag="img", props={"src": "image.png"})
        expected_output_single_prop = ' src="image.png"'
        self.assertEqual(html_node_single_prop.props_to_html(), expected_output_single_prop)

    def test_htmlnode_repr(self):
        # Test repr for HTMLNode
        node = HTMLNode("p", "What a strange world", None, {"class": "primary"})
        self.assertEqual(repr(node), "HTMLNode(tag='p', value='What a strange world', children=None, props={'class': 'primary'})")




class TestLeafNode(unittest.TestCase):

    def test_leafnode_to_html(self):
        # Test LeafNode with tag
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(node.to_html(), "<p>This is a paragraph of text.</p>")

        # Test LeafNode without tag
        no_tag_node = LeafNode(value="Just some text")
        self.assertEqual(no_tag_node.to_html(), "Just some text")

        # Test LeafNode with props
        props_node = LeafNode("a", "Click me!", {"href": "https://example.com"})
        self.assertEqual(props_node.to_html(), '<a href="https://example.com">Click me!</a>')

    def test_leafnode_repr(self):
        # Test repr for LeafNode with tag
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(repr(node), "LeafNode(tag='p', value='This is a paragraph of text.', props=None)")

        # Test repr for LeafNode without tag
        no_tag_node = LeafNode(value="Just some text")
        self.assertEqual(repr(no_tag_node), "LeafNode(tag=None, value='Just some text', props=None)")





class TestParentNode(unittest.TestCase):

    def test_parentnode_without_tag(self):
        # Test ValueError for ParentNode without tag
        with self.assertRaises(ValueError) as context:
            ParentNode(None, [LeafNode("b", "Bold text")]).to_html()
        self.assertEqual(str(context.exception), "Invalid HTML: Parent node must have a tag")

    def test_parentnode_without_children(self):
        # Test ValueError for ParentNode without children
        with self.assertRaises(ValueError) as context:
            ParentNode("p", []).to_html()
        self.assertEqual(str(context.exception), "Invalid HTML: Parent node must have children")

    def test_parentnode_with_children(self):
        # Test ParentNode for multiple children
        node = ParentNode("p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text")
            ]
        )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_parentnode_nested(self):
        # Test ParentNode with nested nodes
        node = ParentNode("div",
            [
                ParentNode("p",
                    [
                        LeafNode("b", "Bold text"),
                        LeafNode(None, "Normal text")
                    ]
                ),
                LeafNode("i", "italic text")
            ]
        )
        self.assertEqual(node.to_html(), "<div><p><b>Bold text</b>Normal text</p><i>italic text</i></div>")

    def test_parentnode_repr(self):
        # Test repr for ParentNode
        node = ParentNode("div",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text")
            ]
        )
        self.assertEqual(repr(node), "ParentNode(tag='div', children=[LeafNode(tag='b', value='Bold text', props=None), LeafNode(tag=None, value='Normal text', props=None)], props=None)")




if __name__ == "__main__":
    unittest.main()