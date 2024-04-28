import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a different text node", "bold")
        self.assertNotEqual(node, node2)

    def test_format_not_eq(self):
        node = TextNode("This is a text node", None)
        node2 = TextNode("This is a text node", "bold")
        self.assertNotEqual(node, node2)

    def test_eq_with_url(self):
        node = TextNode("This is a text node", "bold", "/assets/monkey.png")
        node2 = TextNode("This is a text node", "bold", "/assets/monkey.png")
        self.assertEqual(node, node2)

    def test_not_eq_with_url(self):
        node = TextNode("This is a text node", "bold", "/assets/banana.png")
        node2 = TextNode("This is a text node", "bold", "/assets/monkey.png")
        self.assertNotEqual(node, node2)

    def test_not_eq_url_not_none(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold", "/assets/monkey.png")
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
