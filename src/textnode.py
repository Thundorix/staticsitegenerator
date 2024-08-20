from htmlnode import LeafNode




# Define constants for text types
text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"




class TextNode:
    def __init__(self, text, text_type, url=None):
        """
        Initialize a TextNode object.

        :param text:        The text content
        :param text_type:   Type of text (e.g., bold, italic, code)
        :param url:         URL associated with text if applicable (e.g., links, images)
        """
        self.text = text
        self.text_type = text_type
        self.url = url 

    def __eq__(self, other):
        """
        Define equality between two TextNode objects.
        """
        if isinstance(other, TextNode):
            return (
                self.text == other.text 
                and self.text_type == other.text_type 
                and self.url == other.url
            )
        return False
    
    def __repr__(self):
        """
        Privdes a string representation of the TextNode object.
        """
        return f"TextNode({self.text}, {self.text_type}, {self.url})"




def text_node_to_html_node(text_node):
    """
    Converts a TextNode to an HTMLNode.

    :param text_node:   The TextNode to convert
    :return:            A corresponding HTMLNode
    """
    if text_node.text_type == text_type_text:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == text_type_bold:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == text_type_italic:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == text_type_code:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == text_type_link:
        if text_node.url is None:
            raise ValueError("Link type requires a URL")
        return LeafNode("a", text_node.text, {"href": text_node.url})        
    elif text_node.text_type == text_type_image:
        if text_node.url is None:
            raise ValueError("Image type requires a URL")
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    else:
        raise ValueError("Unsupported text type")