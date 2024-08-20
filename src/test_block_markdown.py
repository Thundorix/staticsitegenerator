import unittest

from block_markdown import (
    block_type_paragraph,
    block_type_heading,
    block_type_code,
    block_type_quote,
    block_type_unordered_list,
    block_type_ordered_list,
    markdown_to_blocks, 
    block_to_block_type,
    markdown_to_html_node,
    extract_title
)

from htmlnode import (
    ParentNode,
    LeafNode
)




class TestMarkdownToBlocks(unittest.TestCase):

    # Test markdown to blocks
    def test_markdown_to_blocks(self):
        markdown = "# Heading\n\nParagraph\n\n* List item"
        result = markdown_to_blocks(markdown)
        expected = [
            "# Heading",
            "Paragraph",
            "* List item"
        ]
        self.assertEqual(result, expected)

    # Test markdown to blocks - empty lines
    def test_markdown_to_blocks_empty_lines(self):
        markdown = "\n\n# Heading\n\n\n\nParagraph\n\n\n\n* List item\n\n"
        result = markdown_to_blocks(markdown)
        expected = [
            "# Heading",
            "Paragraph",
            "* List item"
        ]
        self.assertEqual(result, expected)

    # Test markdown to blocks - no blocks
    def test_makrdown_to_blocks_no_blocks(self):
        markdown = "\n\n\n"
        expected = []
        self.assertEqual(markdown_to_blocks(markdown), expected)

    # Test markdown to blocks - single block
    def test_markdown_to_blocks_single_block(self):
        markdown = "# Heading"
        result = markdown_to_blocks(markdown)
        expected = ["# Heading"]
        self.assertEqual(result, expected)
    



class TestBlockToBlockType(unittest.TestCase):

    # Test block to block types - heading
    def test_block_to_block_type_heading(self):
        result = block_to_block_type("# Heading")
        self.assertEqual(result, block_type_heading)

    # Test block to block types - code block
    def test_block_to_block_type_code(self):
        result = block_to_block_type("```code```")
        self.assertEqual(result, block_type_code)

    # Test block to block types - quote block
    def test_block_to_block_type_quote(self):
        result = block_to_block_type("> Quote")
        self.assertEqual(result, block_type_quote)

    # Test block to block types - unordered list
    def test_unordered_block_to_block_type_list(self):
        result = block_to_block_type("* item\n* item")
        self.assertEqual(result, block_type_unordered_list)

    # Test block to block types - ordered list
    def test_block_to_block_type_ordered_list(self):
        result = block_to_block_type("1. First\n2. Second")
        self.assertEqual(result, block_type_ordered_list)

    # Test block to block types - paragraph
    def test_block_to_block_type_paragraph(self):
        result = block_to_block_type("Just some text.")
        self.assertEqual(result, block_type_paragraph)
    



class TestMarkdownToHtmlNode(unittest.TestCase):

    # Test markdown to html node - heading
    def test_markdown_to_html_node_heading(self):
        markdown = "# Heading"
        result = markdown_to_html_node(markdown)
        expected = ParentNode("div", children=[LeafNode("h1", "Heading")])
        self.assertEqual(result, expected)

    # Test markdown to html node - code
    def test_markdown_to_html_node_code(self):
        markdown = "```\ncode line 1\ncode line 2\n```"
        result = markdown_to_html_node(markdown)
        expected = ParentNode("div", children=[
            ParentNode("pre", children=[
                LeafNode("code", "code line 1\ncode line 2")
            ])
        ])
        self.assertEqual(result, expected)

    # Test markdown to html node - quote
    def test_markdown_to_html_node_quote(self):
        markdown = "> This is a quote\n> that spans multiple lines."
        result = markdown_to_html_node(markdown)
        expected = ParentNode(tag="div", children=[
            ParentNode(tag="blockquote", children=[
                LeafNode(None, "This is a quote"),
                LeafNode(None, "that spans multiple lines.")
            ])
        ])
        self.assertEqual(result, expected)

    # Test markdown for html node - unordered list
    def test_markdown_for_html_node_unordered_list(self):
        markdown = "* Item 1\n* Item 2\n* Item 3"
        result = markdown_to_html_node(markdown)
        expected = ParentNode("div", children=[
            ParentNode("ul", children=[
                ParentNode("li", children=[LeafNode(None, "Item 1")]),
                ParentNode("li", children=[LeafNode(None, "Item 2")]),
                ParentNode("li", children=[LeafNode(None, "Item 3")])
            ])
        ])
        self.assertEqual(result, expected)

    # Test markdown to html node - ordered list
    def test_markdown_to_html_node_ordered_list(self):
        markdown = "1. First item\n2. Second item\n3. Third item"
        result = markdown_to_html_node(markdown)
        expected = ParentNode("div", children=[
            ParentNode("ol", children=[
                ParentNode("li", children=[LeafNode(None, "First item")]),
                ParentNode("li", children=[LeafNode(None, "Second item")]),
                ParentNode("li", children=[LeafNode(None, "Third item")])
            ])
        ])
        self.assertEqual(result, expected)

    # Test markdown to html node - mixed list
    def test_markdown_to_html_node_mixed_list(self):
        markdown = "- Bullet 1\n- Bullet 2\n* Bullet 3\n\n\n1. Step 1\n2. Step 2\n3. Step 3\n"
        result = markdown_to_html_node(markdown)
        expected = ParentNode("div", children=[
            ParentNode("ul", children=[
                ParentNode("li", children=[LeafNode(None, "Bullet 1")]),
                ParentNode("li", children=[LeafNode(None, "Bullet 2")]),
                ParentNode("li", children=[LeafNode(None, "Bullet 3")])
            ]),
            ParentNode("ol", children=[
                ParentNode("li", children=[LeafNode(None, "Step 1")]),
                ParentNode("li", children=[LeafNode(None, "Step 2")]),
                ParentNode("li", children=[LeafNode(None, "Step 3")])
            ])
        ])
        self.assertEqual(result, expected)
   
    # Test markdown to html node - paragraph
    def test_markdown_to_html_node_paragraph(self):
        markdown  = "This is a simple paragraph"
        result = markdown_to_html_node(markdown)
        expected = ParentNode("div", children=[
            ParentNode("p", children=[
                LeafNode(None, "This is a simple paragraph")
            ])
        ])
        self.assertEqual(result, expected)

    # Test markdown to html node - paragraph with inline markdown
    def test_markdown_to_html_node_paragraph_with_inline_markdown(self):
        markdown = "This is **bold** text and this is *italic* text."
        result = markdown_to_html_node(markdown)
        expected = ParentNode("div", children=[
            ParentNode("p", children=[
                LeafNode(None, "This is "),
                LeafNode("b", "bold"),
                LeafNode(None, " text and this is "),
                LeafNode("i", "italic"),
                LeafNode(None, " text.")
            ])
        ])
        self.assertEqual(result, expected)

    # Test markdown to html node - complex markdown
    def test_markdown_to_html_node_complex_markdown(self):
        markdown = """
# This is my heading.

## This is my sub heading

Here I am testing **bold** and *italic* in line markup
as well as a code block:

```print("Hello world!")
print("Bye bye")```

I should also test for quotes:

> Tokumei is **AMAZING**!!
> He knows all there is to know about nothing.

In addition, let's look at some bullet points:

* Bullet 1
* Bullet 2
* Bullet 3
* Bullet 4

1. Step 1
2. Step 2
3. Step 3

And there we have it, all done, I hope...
"""
        result = markdown_to_html_node(markdown)
        expected = ParentNode(tag="div", children=[
            LeafNode("h1", "This is my heading."),
            LeafNode("h2", "This is my sub heading"),
            ParentNode("p", children=[
                LeafNode(None, "Here I am testing "),
                LeafNode("b", "bold"),
                LeafNode(None, " and "),
                LeafNode("i", "italic"),
                LeafNode(None, " in line markup\nas well as a code block:")
            ]),
            ParentNode("pre", children=[
                LeafNode("code", 'print("Hello world!")\nprint("Bye bye")')
            ]),
            ParentNode("p", children=[
                LeafNode(None, "I should also test for quotes:")
            ]),
            ParentNode("blockquote", children=[
                LeafNode(None, "Tokumei is "),
                LeafNode("b", "AMAZING"),
                LeafNode(None, "!!"),
                LeafNode(None, "He knows all there is to know about nothing.")
            ]),
            ParentNode("p", children=[
                LeafNode(None, "In addition, let's look at some bullet points:")
            ]),
            ParentNode("ul", children=[
                ParentNode("li", children=[LeafNode(None, "Bullet 1")]),
                ParentNode("li", children=[LeafNode(None, "Bullet 2")]),
                ParentNode("li", children=[LeafNode(None, "Bullet 3")]),
                ParentNode("li", children=[LeafNode(None, "Bullet 4")])
            ]),
            ParentNode("ol", children=[
                ParentNode("li", children=[LeafNode(None, "Step 1")]),
                ParentNode("li", children=[LeafNode(None, "Step 2")]),
                ParentNode("li", children=[LeafNode(None, "Step 3")])
            ]),
            ParentNode("p", children=[
                LeafNode(None, "And there we have it, all done, I hope...")
            ])
        ])
        self.assertEqual(result, expected)



    
class TestExtractTitle(unittest.TestCase):
    # Test extract title
    def test_extract_title(self):
        markdown = "# This is my title"
        result = extract_title(markdown)
        expected = "This is my title"
        self.assertEqual(result, expected)
    
    # Test extract title - whitespace
    def test_extract_title_whitespace(self):
        markdown = "#       This is my title          "
        result = extract_title(markdown)
        expected = "This is my title"
        self.assertEqual(result, expected)

    # Test extract title - no title
    def test_extract_title_no_title(self):
        markdown = "This is not my title"
        with self.assertRaises(ValueError):
            extract_title(markdown)




if __name__ == "__main__":
    unittest.main()