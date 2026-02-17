import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_dif_text_type(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_dif_url(self):
        node = TextNode("This is a link node", TextType.LINK, "https://google.com")
        node2 = TextNode("This is a link node", TextType.LINK, "https://facebook.com")
        self.assertNotEqual(node, node2)
    def test_url_none(self):
        node = TextNode("lol", TextType.LINK, None)
        node2 = TextNode("lol", TextType.LINK)
        self.assertEqual(node, node2)

if __name__ == "__main__":
    unittest.main()