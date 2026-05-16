import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    results = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            results.append(node)
        else:
            split_node = node.text.split(delimiter)
            if len(split_node) % 2 == 0:
                raise Exception(f"Invalid markdown: no closing '{delimiter}' in '{node.text}'")
            else:
                for i, string in enumerate(split_node):
                    if not string:
                        continue
                    elif i % 2 == 0:
                        results.append(TextNode(string, TextType.TEXT))
                    else:
                        results.append(TextNode(string, text_type))
    return results           

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)