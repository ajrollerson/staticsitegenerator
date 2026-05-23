from textnode import TextNode, TextType
from copy_static import copy_static, copy_recursive, generate_pages_recursive
import os
import shutil

src = "static"
dst = "public"
from_path = 'content'
template_path = 'template.html'
dest_path = 'public'


def main():
    copy_static(src, dst)
    generate_pages_recursive(from_path, template_path, dest_path)
if __name__ == "__main__":
    main()