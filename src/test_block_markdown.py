import unittest
from block_markdown import BlockType, markdown_to_blocks, block_to_block_type

class TestHTMLNode(unittest.TestCase):
    def test_markdown_to_blocks(self):
            md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ],
            )

    def test_markdown_with_many_empty_lines(self):
            md = """
This is a paragraph.







Truly.
"""
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is a paragraph.",
                    "Truly.",
                ],
            )

    def test_markdown_with_trailing_spaces(self):
            md = """
     This is a paragraph with trailing spaces.







Truly.    
"""
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is a paragraph with trailing spaces.",
                    "Truly.",
                ],
            )

    def test_empty_markdown(self):
            md = """
      
"""
            blocks = markdown_to_blocks(md)
            self.assertEqual(blocks, [],)

    def test_paragraph(self):
            block = "This is just a paragraph block."  
            result = block_to_block_type(block)
            self.assertEqual(result, BlockType.PARAGRAPH)

    def test_heading(self):
            block = "# This is a header block."  
            result = block_to_block_type(block)
            self.assertEqual(result, BlockType.HEADING)

    def test_code(self):
            block = "```\nsome code here\n```"  
            result = block_to_block_type(block)
            self.assertEqual(result, BlockType.CODE)
    
    def test_quote(self):
            block = "> This is quote paragraph.\n> Hear ye.\n> Hear ye."  
            result = block_to_block_type(block)
            self.assertEqual(result, BlockType.QUOTE)

    def test_invalid_quote(self):
            block = "> This is quote paragraph.\n< Hear ye.\n> Hear ye."  
            result = block_to_block_type(block)
            self.assertEqual(result, BlockType.PARAGRAPH)

    def test_unordered_list(self):
            block = "- First item.\n- Next item.\n- Third item."  
            result = block_to_block_type(block)
            self.assertEqual(result, BlockType.UNORDERED_LIST)
    
    def test_invalid_unordered_list(self):
            block = "- First item.\n? Next item.\n- Third item."  
            result = block_to_block_type(block)
            self.assertEqual(result, BlockType.PARAGRAPH)

    def test_ordered_list(self):
            block = "1. First item.\n2. Second item.\n3. Third item."  
            result = block_to_block_type(block)
            self.assertEqual(result, BlockType.ORDERED_LIST)
    
    def test_invalid_ordered_list(self):
            block = "1. First item.\n?. Second item.\n3. Third item."  
            result = block_to_block_type(block)
            self.assertEqual(result, BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()