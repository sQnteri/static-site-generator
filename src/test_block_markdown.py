import unittest
from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items"
        ])

    def test_markdown_to_blocks_empty(self):
        md = """
        
        
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_no_newlines(self):
        md = "This is a single line of markdown with no newlines"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a single line of markdown with no newlines"])


    def test_markdown_to_blocks_multiple_newlines(self):
        md = """This is a paragraph with multiple newlines





        This is the next paragraph"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a paragraph with multiple newlines", "This is the next paragraph"])

class TestBlockToBlockType(unittest.TestCase):
    def test_block_to_block_type_heading_one(self):
        block = "# This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_block_to_block_type_heading_two(self):
        block = "## This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
    
    def test_block_to_block_type_heading_three(self):
        block = "### This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
    
    def test_block_to_block_type_heading_four(self):
        block = "#### This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_block_to_block_type_heading_five(self):
        block = "##### This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_block_to_block_type_heading_six(self):
        block = "###### This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_block_to_block_type_heading_seven(self):
        block = "####### This is not a heading"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)  

    def test_block_to_block_type_code(self):
        block = """```
This is a code block
```"""
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
    
    def test_block_to_block_type_quote(self):
        block = """> This is a quote
> that spans multiple lines"""
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_block_to_block_type_unordered_list(self):
        block = """- Item 1
- Item 2
- Item 3"""
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
    
    def test_block_to_block_type_ordered_list(self):
        block = """1. Item 1
2. Item 2
3. Item 3"""
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
    
    def test_block_to_block_type_paragraph(self):
        block = """This is a paragraph
that spans multiple lines
and has no special formatting"""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_false_ordered_list(self):
        block = """2. Item 1
3. Item 2
4. Item 3"""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    
    



if __name__ == "__main__":
    unittest.main() 