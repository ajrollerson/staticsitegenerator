from htmlnode import HTMLNode, LeafNode, ParentNode
from block_markdown import BlockType, markdown_to_blocks, block_to_block_type
from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node

def text_to_children(text):
    return [text_node_to_html_node(node) for node in text_to_textnodes(text)]

def paragraph_to_html_node(block):
    return ParentNode("p", text_to_children(block.replace("\n", " ")))

def heading_to_html_node(block):
    return ParentNode(f"h{len(block.split(" ", 1)[0])}", text_to_children(block.split(" ", 1)[1]))
    
def code_to_html_node(block):
    return ParentNode("pre", [ParentNode("code", [text_node_to_html_node(TextNode(block[4:-3], text_type=TextType.TEXT))])])

def quote_to_html_node(block):
    return ParentNode("blockquote", text_to_children(" ".join([line.removeprefix("> ") for line in block.split("\n")])))

def unordered_list_to_html_node(block):
    return ParentNode("ul", [ParentNode("li", text_to_children(line.removeprefix("- "))) for line in block.split("\n")])

def ordered_list_to_html_node(block):
    return ParentNode("ol", [ParentNode("li", text_to_children(line.split(". ", 1)[1])) for line in block.split("\n")])


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)

    dispatch = {
        BlockType.PARAGRAPH: paragraph_to_html_node,
        BlockType.HEADING: heading_to_html_node,
        BlockType.CODE: code_to_html_node,
        BlockType.QUOTE: quote_to_html_node,
        BlockType.UNORDERED_LIST: unordered_list_to_html_node,
        BlockType.ORDERED_LIST: ordered_list_to_html_node,
    }

    children = []
    for block in blocks:
        children.append(dispatch[block_to_block_type(block)](block))
    return ParentNode("div", children)



