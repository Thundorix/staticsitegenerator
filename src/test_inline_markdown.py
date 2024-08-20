import unittest
from inline_markdown import (
    split_nodes_delimiter, 
    extract_markdown_images, 
    extract_markdown_links,
    split_nodes_images,
    split_nodes_links,
    text_to_textnodes,
)
from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
)


class TestSplitDelimiter(unittest.TestCase):

    # Test split node delimiter - bold
    def test_split_node_delimiter_bold(self):
        node = TextNode("This is **bold** text", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        expected_nodes = [
            TextNode("This is ", text_type_text),
            TextNode("bold", text_type_bold),
            TextNode(" text", text_type_text)
        ]
        self.assertEqual([n.text for n in new_nodes], [n.text for n in expected_nodes])
        self.assertEqual([n.text_type for n in new_nodes], [n.text_type for n in expected_nodes])    

    # Test split node delimiter - italic
    def test_split_node_delimiter_italic(self):
        node = TextNode("This is *italic* text", text_type_text)
        new_nodes = split_nodes_delimiter([node], "*", text_type_italic)
        expected_nodes = [
            TextNode("This is ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" text", text_type_text)
        ]
        self.assertEqual([n.text for n in new_nodes], [n.text for n in expected_nodes])
        self.assertEqual([n.text_type for n in new_nodes], [n.text_type for n in expected_nodes])

    # Test split node delimiter - code
    def test_split_node_delimiter_code(self):
        node = TextNode("This is text with a 'code block' word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "'", text_type_code)
        expected_nodes = [
            TextNode("This is text with a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" word", text_type_text)
        ]
        self.assertEqual([n.text for n in new_nodes], [n.text for n in expected_nodes])
        self.assertEqual([n.text_type for n in new_nodes], [n.text_type for n in expected_nodes])

    # Test split node delimiter - double same delimiters
    def test_split_node_delimiter_double_bold(self):
        node = TextNode("This phrase has **two** words that are **bold** text", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        expected_nodes = [
            TextNode("This phrase has ", text_type_text),
            TextNode("two", text_type_bold),
            TextNode(" words that are ", text_type_text),
            TextNode("bold", text_type_bold),
            TextNode(" text", text_type_text)
        ]
        self.assertEqual([n.text for n in new_nodes], [n.text for n in expected_nodes])
        self.assertEqual([n.text_type for n in new_nodes], [n.text_type for n in expected_nodes])

    # Test split node delimiter - double diff delimiters
    def test_split_node_delimiter_double_bold_italic(self):
        node = TextNode("This phrase has both **bold text** and *italic text*", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        new_nodes = split_nodes_delimiter(new_nodes, "*", text_type_italic)
        expected_nodes = [
            TextNode("This phrase has both ", text_type_text),
            TextNode("bold text", text_type_bold),
            TextNode(" and ", text_type_text),
            TextNode("italic text", text_type_italic)
        ]
        self.assertEqual([n.text for n in new_nodes], [n.text for n in expected_nodes])
        self.assertEqual([n.text_type for n in new_nodes], [n.text_type for n in expected_nodes])

    # Test split node delimiter - no delimiter
    def test_split_node_delimiter_no_delimiter(self):
        node = TextNode("No delimiters here", text_type_text)
        new_nodes = split_nodes_delimiter([node], "*", text_type_italic)
        expected_nodes = [node]
        self.assertEqual(new_nodes, expected_nodes)

    # Test split ndoe delimiter - invalid syntax
    def test_split_node_delimiter_invalid_syntax(self):
        node = TextNode("Invalid *italic syntac", text_type_text)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "*", text_type_italic)
    



class TestExtractMarkdownImagesAndLinks(unittest.TestCase):

    # Test extract markdown images
    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(extract_markdown_images(text), expected)

    # Test extract markdown images - no image
    def test_extract_markdown_images_no_image(self):
        text = "No image to see here"
        expected = []
        self.assertEqual(extract_markdown_images(text), expected)

    # Test extract markdown images - malformed input
    def test_extract_markdown_images_malformed(self):
        text = "This is a malformed ![rick roll]https://i.imgur/aKaOqIh.gif) image"
        expected = []
        self.assertEqual(extract_markdown_images(text), expected)

    # Test extract markdown links
    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        expected = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertEqual(extract_markdown_links(text), expected)

    # Test extract markdown links - no link
    def test_extract_markdown_links_no_link(self):
        text = "No links here"
        expected = []
        self.assertEqual(extract_markdown_links(text), expected)

    # Test extract markdown links - malformed input
    def test_extract_markdown_links_malformed(self):
        text = "This is text with a malformed [to boot dev]https://www.boot.dev) link."
        expected = []
        self.assertEqual(extract_markdown_links(text), expected)

    # Test extract markdown - mixed image and link
    def test_extract_markdown_mixed_image_and_link(self):
        text = "Here is an ![image](https://example.com/image.png) and a [link](https://example.com)."
        expected_images = [("image", "https://example.com/image.png")]
        expected_links = [("link", "https://example.com")]
        self.assertEqual(extract_markdown_images(text), expected_images)
        self.assertEqual(extract_markdown_links(text), expected_links)
    
    # Test extract markdown - empty
    def test_extract_markdown_empty_image_and_link(self):
        text = ""
        expected_images = []
        expected_links = []
        self.assertEqual(extract_markdown_images(text), expected_images)
        self.assertEqual(extract_markdown_links(text), expected_links)




class TestSplitNodesImagesAndLinks(unittest.TestCase):
    
    # Test split nodes images
    def test_split_nodes_images(self):
        text = "This is text with an image ![alt text](https://example.com/image.png) here."
        node = TextNode(text, text_type_text)
        expected = [
            TextNode("This is text with an image ", text_type_text),
            TextNode("alt text", text_type_image, "https://example.com/image.png"),
            TextNode(" here.", text_type_text)
        ]
        result = split_nodes_images([node])
        self.assertEqual(result, expected)

    # Test split nodes images - only image
    def test_split_nodes_images_only(self):
        text = "![alt text](https://example.com/image.png)"
        node = TextNode(text, text_type_text)
        expected = [
            TextNode("alt text", text_type_image, "https://example.com/image.png")
        ]
        result = split_nodes_images([node])
        self.assertEqual(result, expected)

    # Test split nodes images - no image
    def test_split_nodes_images_no_image(self):
        text = "There is no image to see here"
        node = TextNode(text, text_type_text)
        expected = [node]
        result = split_nodes_images([node])
        self.assertEqual(result, expected)

    # Test split nodes images - multiple images
    def test_split_nodes_images_multiple(self):
        text = "Text with ![first](https://example.com/first.png) and ![second](https://example.com/second.png) images."
        node = TextNode(text, text_type_text)
        expected = [
            TextNode("Text with ", text_type_text),
            TextNode("first", text_type_image, "https://example.com/first.png"),
            TextNode(" and ", text_type_text),
            TextNode("second", text_type_image, "https://example.com/second.png"),
            TextNode(" images.", text_type_text)
        ]
        result = split_nodes_images([node])
        self.assertEqual(result, expected)

    # Test split nodes links
    def test_split_nodes_links(self):
        text = "This is text with a [link](https://example.com)."
        node = TextNode(text, text_type_text)
        expected = [
            TextNode("This is text with a ", text_type_text),
            TextNode("link", text_type_link, "https://example.com"),
            TextNode(".", text_type_text)
        ]
        result = split_nodes_links([node])
        self.assertEqual(result, expected)

    # Test split nodes links - only link
    def test_split_nodes_links_only(self):
        text = "[click me!](https://example.com)"
        node = TextNode(text, text_type_text)
        expected = [
            TextNode("click me!", text_type_link, "https://example.com")
        ]
        result = split_nodes_links([node])
        self.assertEqual(result, expected)

    # Test split nodes links - no link
    def test_split_nodes_links_no_link(self):
        text = "This text doesn't have a link."
        node = TextNode(text, text_type_text)
        expected = [node]
        result = split_nodes_links([node])
        self.assertEqual(result, expected)

    # Test split nodes links - multiple
    def test_split_nodes_links_multiple(self):
        text = "Text with [first](https://example.com/first) and [second](https://example.com/second) links."
        node = TextNode(text, text_type_text)
        expected = [
            TextNode("Text with ", text_type_text),
            TextNode("first", text_type_link, "https://example.com/first"),
            TextNode(" and ", text_type_text),
            TextNode("second", text_type_link, "https://example.com/second"),
            TextNode(" links.", text_type_text)
        ]
        result = split_nodes_links([node])
        self.assertEqual(result, expected)

    # Test split nodes - mixed image and link
    def test_split_nodes_mixed(self):
        text = "Here is an ![image](https://example.com/image.png) and a [link](https://example.com)."
        node = TextNode(text, text_type_text)
        expected_images = [
            TextNode("Here is an ", text_type_text),
            TextNode("image", text_type_image, "https://example.com/image.png"),
            TextNode(" and a [link](https://example.com).", text_type_text)
        ]
        expected_links = [
            TextNode("Here is an ![image](https://example.com/image.png) and a ", text_type_text),
            TextNode("link", text_type_link, "https://example.com"),
            TextNode(".", text_type_text)
        ]
        self.assertEqual(split_nodes_images([node]), expected_images)
        self.assertEqual(split_nodes_links([node]), expected_links)




class TestTextToTextNodes(unittest.TestCase):

    # Test text to textnodes
    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result_nodes = text_to_textnodes(text)
        expected_nodes = [
            TextNode("This is ", text_type_text),
            TextNode("text", text_type_bold),
            TextNode(" with an ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" word and a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" and an ", text_type_text),
            TextNode("obi wan image", text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", text_type_text),
            TextNode("link", text_type_link, "https://boot.dev"),
        ]
        self.assertEqual(result_nodes, expected_nodes)




if __name__ == "__main__":
    unittest.main()