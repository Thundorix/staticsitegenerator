import re

from htmlnode import (
    ParentNode,
    LeafNode
)

from textnode import text_node_to_html_node
from inline_markdown import text_to_textnodes




# Define constants for block types
block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"




def markdown_to_blocks(markdown):
    """
    Split markdown text into blocks separated by 2 or more newlines.

    :param markdown:        The raw markdown text
    :return:                A list of block strings
    """
    block_strings = []
    temp = re.split(r"\n{2,}", markdown)
    for line in temp:
        cleaned_text = re.sub(r"\n\s+", "\n", line).strip()
        if cleaned_text:
            block_strings.append(cleaned_text)
    return block_strings




def block_to_block_type(block):
    """
    Determine the type of a markdown block based on its content.

    :param block:           A single markdown block
    :return:                The type of the block (e.g., heading, quote, list)
    """
    if re.match(r"^#{1,6}\s", block):
        return block_type_heading
    
    if re.match(r"^`{3}[\s\S]*`{3}$", block):
        return block_type_code
    
    lines = block.split("\n")

    if all(re.match(r"^\s*>", line) for line in lines):
        return block_type_quote 
    
    if all(line.startswith(("* ", "- ")) for line in lines):
        return block_type_unordered_list
    
    if all(re.match(r"^\d+\.\s", line) for line in lines):
        order_num = [int(line.split(".")[0]) for line in lines]
        if order_num == list(range(1, len(lines) + 1)):
            return block_type_ordered_list
        else:
            return block_type_paragraph
        
    else:
        return block_type_paragraph




def markdown_to_html_node(markdown):
    """
    Convert markdown text into an HTML node structure.

    :param markdown:        The raw markdown text
    :return:                A ParentNode object representing the HTML structure
    """
    blocks = markdown_to_blocks(markdown)
    child_nodes = []

    for block in blocks:
        block_type = block_to_block_type(block)
        child_node = None

        if block_type == block_type_heading:
            level = block.count("#", 0, block.index(" "))
            if level > 6:
                raise ValueError("Invalid HTML: Heading can only between 1 and 6.")
            heading_text = block.strip("# ")
            child_node = LeafNode(f"h{level}", heading_text)

        elif block_type == block_type_code:
            code_content = block.strip("`\n")
            child_node = ParentNode("pre", children=[LeafNode("code", code_content)])

        elif block_type == block_type_quote:
            quote_lines = [line.lstrip("> ").strip() for line in block.split("\n")]
            quote_children = []
            for line in quote_lines:
                quote_children.extend(text_to_textnodes(line))
            child_node = ParentNode("blockquote", children=[text_node_to_html_node(node) for node in quote_children])

        elif block_type == block_type_unordered_list:
            list_items = []
            for item in block.split("\n"):
                if item.startswith("*"):
                    item_text_nodes = text_to_textnodes(item.lstrip("* ").strip())
                elif item.startswith("-"):
                    item_text_nodes = text_to_textnodes(item.lstrip("- ").strip())
                
                list_items.append(ParentNode("li", children=[text_node_to_html_node(node) for node in item_text_nodes]))
            child_node = ParentNode("ul", children=list_items)

        elif block_type == block_type_ordered_list:
            list_items = []
            for item in block.split("\n"):
                item_text_nodes = text_to_textnodes(item.split(". ", 1)[1].strip())
                list_items.append(ParentNode("li", children=[text_node_to_html_node(node) for node in item_text_nodes]))
            child_node = ParentNode("ol", children=list_items)

        elif block_type == block_type_paragraph:
            paragraph_text = block.strip()
            paragraph_children = text_to_textnodes(paragraph_text)
            child_node = ParentNode("p", children=[text_node_to_html_node(node) for node in paragraph_children])

        if child_node:
            child_nodes.append(child_node)

    if not child_nodes:
        raise ValueError("Invalid HTML: No valid blocks found to create an HTML node structure.")
    
    return ParentNode("div", children=child_nodes)




def extract_title(markdown):
    """
    Extract the title (h1 header) from the markdown.

    :param markdown:        The raw markdown text
    :return:                The title string
    """
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line.lstrip("# ").strip()
    raise ValueError("No H1 header found")
