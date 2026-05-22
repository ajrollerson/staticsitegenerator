from textnode import TextNode, TextType
from copy_static import copy_static, copy_recursive
import os
import shutil

src = "static"
dst = "public"

def main():
    copy_static(src, dst)

if __name__ == "__main__":
    main()