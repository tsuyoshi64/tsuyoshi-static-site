import os
import shutil
import sys

from copystatic import copy_files_recursive
from gencontent import generate_pages_recursive

dir_path_static = "./static"
dir_path_docs = "./docs"
dir_path_template = "./template.html"
dir_path_content = "./content"


def main():
    basepath: str = "/"
    if len(sys.argv) > 1:
        basepath: str = sys.argv[1]

    print("Deleting doc directory...")
    if os.path.exists(dir_path_docs):
        shutil.rmtree(dir_path_docs)

    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_docs)

    print("Starting site generation...")
    generate_pages_recursive(dir_path_content, dir_path_template, dir_path_docs, basepath)
    print("Site generation complete!")


if __name__ == "__main__":
    main()
