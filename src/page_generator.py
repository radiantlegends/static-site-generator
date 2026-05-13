import shutil
import os
import re
from block_parser import markdown_to_html_node

def extract_title(markdown):
    match = re.search(r"^# (.+)", markdown)
    if(match):
        return match.group(1).strip()
    else:
        raise Exception("No h1 header found.")

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}...")
    # Get markdown and template HTML from files.
    with open(from_path, "r") as f:
        md = f.read()
    with open(template_path, "r") as f:
        template = f.read()
    # Convert the markdown to HTML content.
    node = markdown_to_html_node(md)
    html_content = node.to_html()
    # Extract the title from the markdown.
    title = extract_title(md)
    # Replace the template title and content.
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html_content)
    # Update basepath for href and src.
    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')
    # Create the full HTML page at the destination.
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(template)

def generate_pages_recursive(dir_path, template_path, dest_dir_path, basepath):
    items = os.listdir(dir_path)
    for item in items:
        src_path = os.path.join(dir_path, item)
        if item.endswith(".md"):
            dest_path = item.replace(".md", ".html")
        else:
            dest_path = item
        dest_path = os.path.join(dest_dir_path, dest_path)

        if os.path.isdir(src_path):
            generate_pages_recursive(src_path, template_path, dest_path, basepath)
        elif os.path.isfile(src_path):
            generate_page(src_path, template_path, dest_path, basepath)