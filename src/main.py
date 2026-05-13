import shutil
import os
import re
import sys
from page_generator import generate_pages_recursive

def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    if os.path.exists("docs"):
        shutil.rmtree("docs")
    os.makedirs("docs")

    copy_files("static", "docs")

    generate_pages_recursive("content", "template.html", "docs", basepath)

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