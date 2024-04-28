import unittest

from textnode import TextNode
from main import split_nodes_delimiter, text_to_textnodes, markdown_to_blocks, Blocks, block_to_block_type


class TestTextNode(unittest.TestCase):
    def test_delimiter(self):
        node = TextNode("This is text with a `code block` word", "text")           
        new_nodes = split_nodes_delimiter([node], "`", "code")

        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", "text"),
            TextNode("code block", "code"),
            TextNode(" word", "text"),
        ])
    
    def test_node_splitter(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
        self.assertEqual(text_to_textnodes(text), [
                TextNode("This is ", "text"),
                TextNode("text", "bold"),
                TextNode(" with an ", "text"),
                TextNode("italic", "italic"),
                TextNode(" word and a ", "text"),
                TextNode("code block", "code"),
                TextNode(" and an ", "text"),
                TextNode("image", "image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                TextNode(" and a ", "text"),
                TextNode("link", "link", "https://boot.dev")])
        
    def test_block_splitter(self):
        text = '''This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items'''
        self.assertEqual(len(markdown_to_blocks(text)), 3)

    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), Blocks.Heading)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), Blocks.Code)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), Blocks.Quote)
        block = "* list\n* items"
        self.assertEqual(block_to_block_type(block), Blocks.Unordered_List)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), Blocks.Ordered_List)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), Blocks.Paragraph)


if __name__ == "__main__":
    unittest.main()
