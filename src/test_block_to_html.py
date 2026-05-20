import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode
from block_markdown import BlockType, markdown_to_blocks, block_to_block_type
from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node
from block_to_html import markdown_to_html_node


class TestHTMLNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_headings(self):
        md = """
##### Look

#### at

### this

## tiny

# heading
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h5>Look</h5><h4>at</h4><h3>this</h3><h2>tiny</h2><h1>heading</h1></div>",
        )

    def test_quote(self):
        md = """
> Look!
> A
> thoughtful
> quote!

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>Look! A thoughtful quote!</blockquote></div>",
        )

    def test_unordered_list(self):
        md = """
- First
- Something else
- Third
- Fourth

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>First</li><li>Something else</li><li>Third</li><li>Fourth</li></ul></div>",
        )

    def test_ordered_list(self):
        md = """
1. First
2. Second
3. Third
4. Fourth

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First</li><li>Second</li><li>Third</li><li>Fourth</li></ol></div>",
        )

    def test_mixed(self):
        md = """
### Important

1. First
2. Second

- Third
- Fourth

> Thoughtful
> quote

``` 
Some code 
to consider
```

Just text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h3>Important</h3><ol><li>First</li><li>Second</li></ol><ul><li>Third</li><li>Fourth</li></ul><blockquote>Thoughtful quote</blockquote><pre><code>\nSome code \nto consider\n</code></pre><p>Just text</p></div>",
        )

    def test_empty(self):
        md = ""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div></div>",
        )

    def test_mixed_with_inline(self):
        md = """
### _Important_

1. **First**
2. _Second_

- Third
- Fourth

> Thoughtful
> quote

``` **Some code** ```

Just text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h3><i>Important</i></h3><ol><li><b>First</b></li><li><i>Second</i></li></ol><ul><li>Third</li><li>Fourth</li></ul><blockquote>Thoughtful quote</blockquote><pre><code>**Some code** </code></pre><p>Just text</p></div>",
        )