import os

from block_markdown import (
    markdown_to_html_node,
    extract_title
)

## Generates HTML page from content
def generate_page(source_path, template_path, destination_path):
    """
    Generate an HTML page from a markdown file using a specified template.

    :param source_path:             Path to the markdown file
    :param template_path:           Path to the HTML template file
    :param destination_path:        Path to save the generated HTML file
    """
    print(f"Generating page from {source_path} to {destination_path} using {template_path}")

    with open(source_path, "r") as f:
        markdown_content = f.read()
    
    with open(template_path, "r") as f:
        template_content = f.read()

    html_content = markdown_to_html_node(markdown_content).to_html()
    title = extract_title(markdown_content)

    full_html = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_content)

    os.makedirs(os.path.dirname(destination_path), exist_ok=True)

    with open(destination_path, "w") as f:
        f.write(full_html)



## Recursively generates HTML pages from content
def generate_page_recursive(dir_path_content, template_path, dest_dir_path):
    """
    Recursively generate HTML pages from markdown files in a directory.

    :param dir_path_content:        Path to the directory containing markdown files
    :param template_path:           Path to the HTML template file
    :param dest_dir_path:           Path to the destination directory for generated HTML files
    """
    for root, dirs, files in os.walk(dir_path_content):
        for file in files:
            if file.endswith(".md"):
                from_path = os.path.join(root, file)
                relative_path = os.path.relpath(root, dir_path_content)
                dest_dir = os.path.join(dest_dir_path, relative_path)
                os.makedirs(dest_dir, exist_ok=True)
                dest_path = os.path.join(dest_dir, file.replace(".md", ".html"))
                generate_page(from_path, template_path, dest_path)