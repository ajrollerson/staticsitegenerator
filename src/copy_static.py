import shutil
import os
from inline_markdown import extract_title
from htmlnode import HTMLNode
from block_to_html import markdown_to_html_node

def copy_static(src, dst):
    if os.path.exists(dst):
        shutil.rmtree(dst)
        print("Destination deleted!")
    os.makedirs(dst, exist_ok=True)
    print("Destination remade!")
    copy_recursive(src, dst)

def copy_recursive(src, dst):
    for name in os.listdir(src):
        src_path = os.path.join(src, name)
        dst_path = os.path.join(dst, name)
        if os.path.isdir(src_path):
            os.mkdir(dst_path)
            print(f"Made {dst_path}!")
            copy_recursive(src_path, dst_path)
            print(f"Copied into {dst_path}!")
        elif os.path.isfile(src_path):
            shutil.copy(src_path, dst_path)
            print(f"File copied to {dst_path}!")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}.")
    with open(from_path, "r") as file:
        markdown_content = file.read()
    with open(template_path, "r") as file:
        template_content = file.read()
    markdown_html = markdown_to_html_node(markdown_content).to_html()
    title = extract_title(markdown_content)
    new_template = template_content.replace("{{ Title }}", title).replace("{{ Content }}", markdown_html)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as file:
        file.write(new_template)
   
    

        