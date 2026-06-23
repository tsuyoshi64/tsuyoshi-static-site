import os
import shutil

from copystatic import copy_files_recursive
from textnode import TextNode, TextType

dir_path_static = "./static"
dir_path_public = "./public"


def main():
    textnode = TextNode(
        "This is my github", TextType.LINK, "https://github.com/tsuyoshi64"
    )
    # print(textnode)

    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_public)


if __name__ == "__main__":
    main()
