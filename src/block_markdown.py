from enum import Enum

def markdown_to_blocks(markdown):
    blocks = markdown.strip().split("\n\n")
    return [block for block in blocks if block]

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(markdown_block):
    lines = markdown_block.split("\n")
    if markdown_block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    elif lines[0].startswith("```") and lines[-1].endswith("```"):
        return BlockType.CODE
    elif markdown_block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    elif markdown_block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    elif markdown_block.startswith("1. "):
        for i, line in enumerate(lines, start=1):
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
    