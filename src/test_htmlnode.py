import unittest
from src.htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_to_html_not_equal(self):
        node = HTMLNode(props={"href": "https://www.facebook.com"})
        node2 = HTMLNode(props={"href": "https://www.facebook.com", "target": "_blank"})
        self.assertNotEqual(node.props_to_html(), node2.props_to_html())
    
    def test_to_html(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        result = node.props_to_html()
        self.assertEqual(result, ' href="https://www.google.com" target="_blank"')

    def test_to_html_equal(self):
        node = HTMLNode(props={"href": "https://www.github.com", "target": "_blank"})
        node2 = HTMLNode(props={"href": "https://www.github.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), node2.props_to_html())
        

if __name__ == "__main__":
    unittest.main()