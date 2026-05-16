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

def split_nodes_image(old_nodes):
    results = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            results.append(node)
            continue
        else:
            images = extract_markdown_images(node.text)
        if len(images) == 0:
            results.append(node)
            continue
        remaining_text = node.text
        for alt, url in images:
            parts = remaining_text.split(f"![{alt}]({url})", 1)
            if parts[0]:
                results.append(TextNode(parts[0], TextType.TEXT))
            results.append(TextNode(alt, TextType.IMAGE, url))
            remaining_text = parts[1]
        if remaining_text:
            results.append(TextNode(remaining_text, TextType.TEXT))
    return results

def split_nodes_link(old_nodes):
    results = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            results.append(node)
            continue
        else:
            links = extract_markdown_links(node.text)
        if len(links) == 0:
            results.append(node)
            continue
        remaining_text = node.text
        for anchor_text, link in links:
            parts = remaining_text.split(f"[{anchor_text}]({link})", 1)
            if parts[0]:
                results.append(TextNode(parts[0], TextType.TEXT))
            results.append(TextNode(anchor_text, TextType.LINK, link))
            remaining_text = parts[1]
        if remaining_text:
            results.append(TextNode(remaining_text, TextType.TEXT))
    return results

def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    nodes = [node]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes