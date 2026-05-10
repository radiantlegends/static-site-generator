import shutil
import os
import re
from block_parser import markdown_to_html_node

def main():
    if os.path.exists("public"):
        shutil.rmtree("public")
    os.makedirs("public")
    copy_files("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")

def copy_files(src_dir, dest_dir):
    for item in os.listdir(src_dir):
        src_path = os.path.join(src_dir, item)
        dest_path = os.path.join(dest_dir, item)

        if os.path.isfile(src_path):
            shutil.copy(src_path, dest_path)
        elif os.path.isdir(src_path):
            os.makedirs(dest_path, exist_ok=True)
            copy_files(src_path, dest_path)

def extract_title(markdown):
    match = re.search(r"^# (.+)", markdown)
    if(match):
        return match.group(1).strip()
    else:
        raise Exception("No h1 header found.")

def generate_page(from_path, template_path, dest_path):
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
    # Create the full HTML page at the destination.
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(template)

if __name__ == "__main__":
    main()