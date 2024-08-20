import unittest

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
    text_node_to_html_node
)
from htmlnode import LeafNode




class TestTextNode(unittest.TestCase):
    
    # Test for equality in TextNode text
    def test_textnode_equality(self):
        node = TextNode("This is a text node", text_type_bold)
        node2 = TextNode("This is a text node", text_type_bold)
        self.assertEqual(node, node2)

    # Test for inequality in TextNode text
    def test_textnode_inequality_different_text(self):
        node = TextNode("This is a text node", text_type_bold, "https://www.boot.dev")
        node2 = TextNode("This is a different text node", text_type_bold, "https://boot.dev")
        self.assertNotEqual(node, node2)

    # Test for inequality in TextNode text type
    def test_textnode_inequality_different_text_type(self):
        node = TextNode("This is a text node", text_type_bold, "https://www.boot.dev")
        node2 = TextNode("This is a text node", text_type_italic, "https://www.boot.dev")
        self.assertNotEqual(node, node2)
    
    # Test for inequality in TextNode URL
    def test_textnode_inequality_different_url(self):
        node = TextNode("This is a text node", text_type_bold, "https://boot.dev")
        node2 = TextNode("This is a text node", text_type_bold, "https://google.com")
        self.assertNotEqual(node, node2)
    
    # Test for equlity in TextNode with no URL
    def test_textnode_equality_no_url(self):
        node = TextNode("This is a text node", text_type_bold, None)
        node2 = TextNode("This is a text node", text_type_bold, None)
        self.assertEqual(node, node2)
    
    # Test repr for TextNode
    def test_textbode_repr(self):
        node = TextNode("This is a text node", text_type_bold, "https://boot.dev")
        self.assertEqual(repr(node), "TextNode(This is a text node, bold, https://boot.dev)")




class TestTextNodeToHtmlNode(unittest.TestCase):

    # Test TextNode to HTMLNode - text
    def test_textnode_to_htmlnode_text(self):
        text_node = TextNode("Just some text", text_type_text)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "Just some text")
        expected_html_node = LeafNode(None, "Just some text")
        self.assertEqual(html_node.to_html(), expected_html_node.to_html())

    # Test TextNode to HTMLNode - bold
    def test_textnode_to_htmlnode_bold(self):
        text_node = TextNode("Bold text", text_type_bold)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")
        expected_html_node = LeafNode("b", "Bold text")
        self.assertEqual(html_node.to_html(), expected_html_node.to_html())

    # Test TextNode to HTMLNode - italic
    def test_textnode_to_htmlnode_italic(self):
        text_node = TextNode("Italic text", text_type_italic)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")
        expected_html_node = LeafNode("i", "Italic text")
        self.assertEqual(html_node.to_html(), expected_html_node.to_html())
    
    # Test TextNode to HTMLNode - code block
    def test_textnode_to_htmlnode_code(self):
        text_node = TextNode("print('Hello world!')", text_type_code)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('Hello world!')")
        expected_html_node = LeafNode("code", "print('Hello world!')")
        self.assertEqual(html_node.to_html(), expected_html_node.to_html())

    # Test TextNode to HTMLNode - link
    def test_textnode_to_htmlnode_link(self):
        text_node = TextNode("Click me!", text_type_link, "https://www.example.com")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click me!")
        self.assertEqual(html_node.props, {"href": "https://www.example.com"})
        expected_html_node = LeafNode("a", "Click me!", {"href": "https://www.example.com"})
        self.assertEqual(html_node.to_html(), expected_html_node.to_html())

    # Test TextNode to HTMLNode - image
    def test_textnode_to_htmlnode_image(self):
        text_node = TextNode("This is a nice image", text_type_image, "https://www.example.com/image.png")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://www.example.com/image.png", "alt": "This is a nice image"})
        expected_html_node = LeafNode("img", "", {"src": "https://www.example.com/image.png", "alt": "This is a nice image"})
        self.assertEqual(html_node.to_html(), expected_html_node.to_html())

    # Test TextNode to HTMLNode - invalid type
    def test_textnode_to_htmlnode_invalid_type(self):
        text_node = TextNode("Unsupported text", "unsupported")
        with self.assertRaises(ValueError):
            text_node_to_html_node(text_node)




if __name__ == "__main__":
    unittest.main()
