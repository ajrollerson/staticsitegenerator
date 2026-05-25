import unittest
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes, extract_title
from textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):
    def test_code_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_bold_delimiter(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_italic_delimiter(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_multiple_delimiters(self):
        node = TextNode("This is text with a **bold** and **bolder** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("bolder", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_no_change(self):
        node = TextNode("_In italics_", TextType.ITALIC)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected = [
            TextNode("_In italics_", TextType.ITALIC)
        ]
        self.assertEqual(new_nodes, expected)

    def test_unclosed_delimiter(self):
        node = TextNode("This has an **unclosed bold", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_mixed_nodes_delimiter(self):
        italic_node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        text_node = TextNode("This is just text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([italic_node, text_node], "_", TextType.ITALIC)
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
            TextNode("This is just text", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected)

    def test_multiple_similar_nodes_delimiter(self):
        italic_node1 = TextNode("This is text with an _italic_ word", TextType.TEXT)
        italic_node2 = TextNode("This is more text with another _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([italic_node1, italic_node2], "_", TextType.ITALIC)
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
            TextNode("This is more text with another ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)


    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link to [to youtube](https://www.youtube.com)"
        )
        self.assertListEqual([("to youtube", "https://www.youtube.com")], matches)

    def test_extract_multiple_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with two links to [youtube](https://www.youtube.com) and [facebook](http://www.facebook.com)"
        )
        self.assertListEqual([("youtube", "https://www.youtube.com"), ("facebook", "http://www.facebook.com")], matches)

    def test_extract_multiple_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with two images: ![image](https://i.imgur.com/zjjcJKZ.png) and ![rick roll](https://i.imgur.com/aKaOqIh.gif)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png"), ("rick roll","https://i.imgur.com/aKaOqIh.gif")], matches)

    def test_extract_only_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an image and a link: ![image](https://i.imgur.com/zjjcJKZ.png) and [youtube](https://www.youtube.com)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_only_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an image and a link: ![image](https://i.imgur.com/zjjcJKZ.png) and [youtube](https://www.youtube.com)"
        )
        self.assertListEqual([("youtube", "https://www.youtube.com")], matches)

    def test_no_images(self):
        matches = extract_markdown_images(
            "This is just text"
        )
        self.assertListEqual([], matches)

    def test_no_links(self):
        matches = extract_markdown_links(
            "This is just text"
        )
        self.assertListEqual([], matches)

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

    def test_split_links(self):
        node = TextNode(
            "This is text with two links to [youtube](https://www.youtube.com) and [facebook](http://www.facebook.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with two links to ", TextType.TEXT),
                TextNode("youtube", TextType.LINK, "https://www.youtube.com"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "facebook", TextType.LINK, "http://www.facebook.com"
                ),
            ],
            new_nodes,
        )

    def test_just_a_text_node_links(self):
        node = TextNode("This is just pure text. No images. No links.", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("This is just pure text. No images. No links.", TextType.TEXT)], new_nodes)

    def test_just_a_text_node_images(self):
        node = TextNode("This is just pure text. No images. No links.", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("This is just pure text. No images. No links.", TextType.TEXT)], new_nodes)

    def test_not_a_textnode_links(self):
        node = TextNode("This is bold", TextType.BOLD)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("This is bold", TextType.BOLD)], new_nodes)

    def test_not_a_textnode_images(self):
        node = TextNode("This is bold", TextType.BOLD)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("This is bold", TextType.BOLD)], new_nodes)

    def test_link_start(self):
        node = TextNode("[youtube](https://www.youtube.com) at the start", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("youtube", TextType.LINK, "https://www.youtube.com"),
                TextNode(" at the start", TextType.TEXT),
            ],
            new_nodes
        )

    def test_image_start(self):
        node = TextNode("![image](https://i.imgur.com/zjjcJKZ.png) at the start", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" at the start", TextType.TEXT),
            ],
            new_nodes
        )

    def test_accidental_image(self):
        node = TextNode("This is text is supposed to have a link! ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text is supposed to have a link! ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_accidental_link(self):
        node = TextNode("This is text is supposed to have an image! [youtube](https://www.youtube.com)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text is supposed to have an image! [youtube](https://www.youtube.com)", TextType.TEXT),
            ],
            new_nodes,
        )
    
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
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
            ],
            new_nodes
        )

    def test_text_to_just_text(self):
        text = "This is just text. Nothing more. Nothing less."
        new_nodes = text_to_textnodes(text)
        self.assertListEqual([TextNode("This is just text. Nothing more. Nothing less.", TextType.TEXT)], new_nodes)

    def test_text_to_only_one_type(self):
        text = "This is text with a **bold** word."
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" word.", TextType.TEXT),
            ],
            new_nodes
        )

    def test_leading_type(self):
        text = "**This** is text with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This", TextType.BOLD),
                TextNode(" is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes
        )
    
    def test_extract_title(self):
        text = "# This is a H1 Header."
        self.assertListEqual([extract_title(text)], ["This is a H1 Header."])

    def test_extract_title_error(self):
        text = "This is NOT a H1 Header."
        with self.assertRaises(Exception):
            self.assertListEqual([extract_title(text)], ["This is NOT a H1 Header."])

if __name__ == "__main__":
    unittest.main()