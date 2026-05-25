from textnode import TextNode, TextType
from copy_static import copy_static, copy_recursive, generate_pages_recursive
import os
import shutil
import sys

basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
basepath = basepath if basepath.endswith("/") else basepath + "/"

src = "static"
dst = "docs"
from_path = 'content'
template_path = 'template.html'
dest_path = 'docs'


def main():
    copy_static(src, dst)
    generate_pages_recursive(from_path, template_path, dest_path, basepath)

if __name__ == "__main__":
    main()