import unittest

from htmlnode import HtmlNode


class TestTextNode(unittest.TestCase):
    def test_props(self):
        node = HtmlNode("p", "this is a node", None, {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_props_is_none(self):
        node = HtmlNode("p", "this is a node", None, None)
        self.assertEqual(node.props_to_html(), '')


if __name__ == "__main__":
    unittest.main()
