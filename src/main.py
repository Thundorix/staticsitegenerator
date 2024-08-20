import os
import shutil

from copy_static import copy_directory
from generate_page import generate_page_recursive


def main():
    # Source and Destination Directories
    static_src_dir = os.path.join(os.path.dirname(__file__), "../static")
    public_dest_dir = os.path.join(os.path.dirname(__file__), "../public")
    content_src_dir = os.path.join(os.path.dirname(__file__), "../content")
    template_src = os.path.join(os.path.dirname(__file__), "../template.html")
    
    # Delete public directory if it exists for a clean build
    print("Deleting public directory...")
    if os.path.exists(public_dest_dir):
        shutil.rmtree(public_dest_dir)

    # Copy static files to public directory
    print("Copying static files to public directory...")
    copy_directory(static_src_dir, public_dest_dir)

    # Generate HTML page from markdown content
    print("Generating page...")
    generate_page_recursive(content_src_dir, template_src, public_dest_dir)




if __name__ == "__main__":
    main()