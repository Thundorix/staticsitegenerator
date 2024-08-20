import re

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link
)




def split_nodes_delimiter(old_nodes, deliminater, text_type):
    """
    Split text nodes based on a given delimiter (e.g., '**' for bold text).

    :param old_nodes:       List of TextNode objects
    :param delimiter:       The delimiter to split the text by
    :param text_type:       The type of text to assign to the split content
    :return:                A new list of TextNode objects
    """
    new_nodes = []
    
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        
        sections = node.text.split(deliminater)
        if len(sections) % 2 == 0:
            raise ValueError(f"Invalid markdown syntax: Unmached delimiter '{deliminater}' in text: '{node.text}'")
        
        for i, section in enumerate(sections):
            if not section:
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(section, text_type_text))
            else:
                new_nodes.append(TextNode(section, text_type))

    return new_nodes




def extract_markdown_images(text):
    """
    Extract markdown images from a given text.

    :param text:            The text to search for images
    :return:                A list of tuples (alt text, image URL)
    """
    pattern = r"!\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches




def extract_markdown_links(text):
    """
    Extract markdown links from a given text.

    :param text:            The text to search for links
    :return:                A list of tuples (link text, URL)
    """
    pattern = r"(?<!!)\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches




def split_nodes_images(old_nodes):
    """
    Split text nodes into images and regular text nodes.

    :param old_nodes:       List of TextNode objects.
    :return:                A new list of TextNode objects, with images extracted
    """
    new_nodes = []
    
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue

        images = extract_markdown_images(node.text)
        if not images:
            new_nodes.append(node)
            continue

        remaining_text = node.text
        for alt, url in images:
            sections = remaining_text.split(f"![{alt}]({url})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown: Link section not closed")
            if sections[0]:
                new_nodes.append(TextNode(sections[0], text_type_text))
            new_nodes.append(TextNode(alt, text_type_image, url))
            remaining_text = sections[1]

        if remaining_text:
            new_nodes.append(TextNode(remaining_text, text_type_text))
    
    return new_nodes




def split_nodes_links(old_nodes):
    """
    Split text nodes into links and regular text nodes.

    :param old_nodes:       List of TextNode objects
    :return:                A new list of TextNode objects, with links extracted
    """
    new_nodes = []
    
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue

        links = extract_markdown_links(node.text)
        if not links:
            new_nodes.append(node)
            continue

        remaining_text = node.text
        for text, url in links:
            sections = remaining_text.split(f"[{text}]({url})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown: Link section not closed")
            if sections[0]:
                new_nodes.append(TextNode(sections[0], text_type_text))
            new_nodes.append(TextNode(text, text_type_link, url))
            remaining_text = sections[1]
            
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, text_type_text))

    return new_nodes
    



def text_to_textnodes(text):
    """
    Convert raw text into a list of TextNode objects.

    :param text:            The raw text to convert
    :return:                A list of TextNode objects representing the text and its formatting
    """
    nodes = [TextNode(text, text_type_text)]
    nodes = split_nodes_delimiter(nodes, "**", text_type_bold)
    nodes = split_nodes_delimiter(nodes, "*", text_type_italic)
    nodes = split_nodes_delimiter(nodes, "`", text_type_code)
    nodes = split_nodes_images(nodes)
    nodes = split_nodes_links(nodes)
    return nodes
