# Static Site Generator

This project is a simple static site generator written in Python. It converts Markdown files into HTML pages using a customizable template.

## Project Structure

- **content/**: Contains the Markdown files that will be converted into HTML.
  - **index.md**: Main page of the site.
  - **majesty/index.md**: A subpage with content about "The Lord of the Rings."
  
- **static/**: Contains static files (CSS, images) that are copied directly into the `public` directory.
  - **images/**: Contains image assets.
  - **index.css**: The main stylesheet for the site.

- **template.html**: The HTML template used for generating the pages. It includes placeholders `{{ Title }}` and `{{ Content }}` which are replaced with the page title and content.

- **public/**: The output directory where the generated HTML files and copied static files are stored. This directory is recreated each time the site is generated.

- **src/**: Contains all the Python source code for the project.
  - **main.py**: The main script that runs the site generation process.
  - **copy_static.py**: Handles copying the static files to the `public` directory.
  - **generate_page.py**: Contains functions for generating individual pages and recursively generating all pages from the `content` directory.
  - **htmlnode.py**: Defines classes for representing HTML elements (`HTMLNode`, `LeafNode`, `ParentNode`).
  - **inline_markdown.py**: Handles processing inline markdown elements like bold, italic, links, and images.
  - **block_markdown.py**: Handles processing markdown blocks like headings, paragraphs, lists, and quotes.
  - **textnode.py**: Defines the `TextNode` class and functions for converting text nodes to HTML nodes.
  
- **test/**: Contains unit tests for the various components of the project.

- **main.sh**: A shell script for running the static site generator and serving the generated site using a simple HTTP server.

## How to Use

1. **Add Content**: Place your Markdown files in the `content` directory. Subdirectories are allowed and will be mirrored in the `public` output.

2. **Run the Generator**: Execute the `./main.sh` script to generate the site. The generated HTML files will be placed in the `public` directory, maintaining the directory structure of `content`.

3. **View the Site**: After generating the site, the script will automatically serve it using a simple HTTP server. You can view it in your browser at `http://localhost:8888`.

## Dependencies

- Python 3.x

## Running Tests

To run the unit tests, navigate to the `src` directory and execute the following command:

```bash
./test.sh
```