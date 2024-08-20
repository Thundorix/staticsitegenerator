class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        """
        Initialize an HTMLNode object.

        :param tag:         The HTML tag (e.g., 'div', 'p', 'i')
        :param value:       The text content (for leaf nodes)
        :param children:    List of child nodes (for parent nodes)
        :param probs:       Dictionary of HTML attributes
        """
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        """
        Converts the HTMLNode object to an HTML string.

        This method should be overwritten by subclasses.
        """
        raise NotImplementedError("Still needs to be imlemented")
    
    def props_to_html(self):
        """
        Converts the proberties dictionary to an HTML string.

        :return:        A string of HTML attributes
        """
        if self.props is None:
            return ""
        prop_string = "".join(f' {key}="{value}"' for key, value in self.props.items())
        return prop_string

    def __repr__(self):
        """
        Privdes a string representation of the HTMLNode object.
        """
        return f"HTMLNode(tag={self.tag!r}, value={self.value!r}, children={self.children!r}, props={self.props!r})"




class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        """
        Initialize a LeafNode object, a subclass of HTMLNode for leaf elements.

        :param tag:         The HTML tag.
        :param value:       The text content.
        :param props:       Dictionary of HTML attributes.
        """
        if value is None:
            raise ValueError("Invalid HTML: no value")
        super().__init__(tag, value, None, props)
        self.props = props
    
    def __eq__(self, other):
        """
        Define equality between two LeafNode objects.
        """
        if isinstance(other, LeafNode):
            return (
                self.tag == other.tag 
                and self.value == other.value 
                and self.props == other.props
            )
        return False

    def to_html(self):
        """
        Convert the LeafNode to an HTML string.
        """
        if self.value is None:
            raise ValueError("Invalid HTML: no value")
        elif self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        """
        Provide a string representation of the LeafNode object.
        """
        return f"LeafNode(tag={self.tag!r}, value={self.value!r}, props={self.props!r})"
    


    
class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        """
        Initialize a ParentNode object, a subclass of HTMLNode for parent elements.

        :param tag:         The HTML tag
        :param children:    List of child nodes
        :param props:       Dictionary of HTML attributes
        """
        if tag is None:
            raise ValueError("Invalid HTML: Parent node must have a tag")
        if not children:
            raise ValueError("Invalid HTML: Parent node must have children")
        super().__init__(tag, None, children, props)

    def __eq__(self, other):
        """
        Define equality between two ParentNode objects.
        """
        if isinstance(other, ParentNode):
            return (
                self.tag == other.tag 
                and self.children == other.children 
                and self.props == other.props
            )
        return False

    def to_html(self):
        """
        Convert the ParentNode and its children to an HTML string.
        """
        chilren_string = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}{self.props_to_html()}>{chilren_string}</{self.tag}>"


    def __repr__(self):
        """
        Provide a string representation of the ParentNode object.
        """
        return f"ParentNode(tag={self.tag!r}, children={self.children!r}, props={self.props!r})"
