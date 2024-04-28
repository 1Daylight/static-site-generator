import unittest

from htmlnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_html(self):
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(node.to_html(), '<p>This is a paragraph of text.</p>')

    def test_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')
                        
    def test_no_tag(self):
        node = LeafNode(None, "woobawub")
        self.assertEqual(node.to_html(), 'woobawub')

if __name__ == "__main__":
    unittest.main()
