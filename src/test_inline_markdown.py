import unittest
from src.textnode import TextNode, TextType
from src.inline_markdown import *

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
            ])
        
    def test_bold(self):
        node = TextNode("This is text with a **bold word**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold word", TextType.BOLD)
        ])

    def test_only_italic(self):
        node = TextNode("_this one only has italic text_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [TextNode("this one only has italic text", TextType.ITALIC)])

    def test_raises(self):
        node = TextNode("`this one has no ending delimiter", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_two_code_blocks(self):
        node = TextNode("`code` and some `more code` then some text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("code", TextType.CODE),
            TextNode(" and some ", TextType.TEXT),
            TextNode("more code", TextType.CODE),
            TextNode(" then some text", TextType.TEXT)
        ])
    def test_already_formatted(self):
        node = TextNode("**some bolded text**", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [node])

class testExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://www.link.com)"
        )
        self.assertListEqual(matches, [("link", "https://www.link.com")])
    
    def test_markdown_links_image(self):
        matches = extract_markdown_links(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(matches, [])

class testSplitNodesImage(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_returns_same_when_no_images(self):
        node = TextNode("This is text with no images", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(new_nodes, [node])
    
    def test_no_split_on_normal_links(self):
        node = TextNode("This is text with a [normal](https://link.com)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(new_nodes, [node])

    def test_no_split_on_non_text(self):
        node = TextNode("**This is bold text with ![dog][https://img.com/dog]**", TextType.BOLD)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(new_nodes, [node])

    def test_split_only_images(self):
        node = TextNode("![dog](src/dog.png)", TextType.TEXT)
        node2 = TextNode("![cat](src/cat.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node, node2])
        self.assertListEqual(
            [
                TextNode("dog", TextType.IMAGE, "src/dog.png"),
                TextNode("cat", TextType.IMAGE, "src/cat.png")
            ], new_nodes
        )

class testSplitNodesLink(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with a [Google](https://www.google.com) link and another [facebook](https://www.facebook.com) link", TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("Google", TextType.LINK, "https://www.google.com"),
                TextNode(" link and another ", TextType.TEXT),
                TextNode("facebook", TextType.LINK, "https://www.facebook.com"),
                TextNode(" link", TextType.TEXT)
            ],
            new_nodes
        )

    def test_no_split_images(self):
        node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(new_nodes, [node])

    def test_no_split_on_non_text(self):
        node = TextNode("_This is italic text with a [Google](https://www.google.com) link_", TextType.ITALIC)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(new_nodes, [node])

    def test_return_same_no_links(self):
        node = TextNode("This is text with no images", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(new_nodes, [node])

    def test_split_only_links(self):
        node = TextNode("[google](https://google.com)", TextType.TEXT)
        node2 = TextNode("[youtube](https://youtube.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node, node2])
        self.assertListEqual(
            [
                TextNode("google", TextType.LINK, "https://google.com"),
                TextNode("youtube", TextType.LINK, "https://youtube.com")
            ], new_nodes
        )

class testTextToTextNodes(unittest.TestCase):
    def test_split_text(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ], nodes
        )
    
    def test_empty_string(self):
        nodes = text_to_textnodes("")
        self.assertListEqual([], nodes)

    def test_no_markdown(self):
        text = "simple text"
        nodes = text_to_textnodes(text)
        self.assertListEqual([TextNode(text, TextType.TEXT)], nodes)

    def test_markdown_start_multiple_instances(self):
        text = "**this is bold text** and some more **bold text**"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("this is bold text", TextType.BOLD),
                TextNode(" and some more ", TextType.TEXT),
                TextNode("bold text", TextType.BOLD),
            ], nodes
        )

        
if __name__ == "__main__":
    unittest.main()