import shutil
import os
import re
from page_generator import generate_pages_recursive

def main():
    if os.path.exists("public"):
        shutil.rmtree("public")
    os.makedirs("public")
    copy_files("static", "public")
    generate_pages_recursive("content", "template.html", "public")

def copy_files(src_dir, dest_dir):
    for item in os.listdir(src_dir):
        src_path = os.path.join(src_dir, item)
        dest_path = os.path.join(dest_dir, item)

        if os.path.isfile(src_path):
            shutil.copy(src_path, dest_path)
        elif os.path.isdir(src_path):
            os.makedirs(dest_path, exist_ok=True)
            copy_files(src_path, dest_path)

if __name__ == "__main__":
    main()