import os
import shutil

from copystatic import copy_files_recursive
from gencontent import generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_template = "./template.html"
dir_path_content = "./content"


def main():
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_public)

    print("Starting site generation...")
    generate_pages_recursive(dir_path_content, dir_path_template, dir_path_public)
    print("Site generation complete!")


if __name__ == "__main__":
    main()
