import unittest

from blocks import *
from convert import markdown_to_html_node, extract_title


class Test_MD_to_BlockType(unittest.TestCase):
    def test_heading(self):
        MDText = "### Hello world"
        MDType = block_to_block_type(MDText)
        self.assertEqual(MDType, BlockType.HEADING)

    def test_code(self):
        MDText = "``` code ```"
        MDType = block_to_block_type(MDText)
        self.assertEqual(MDType, BlockType.CODE)

    def test_quote(self):
        MDText = "> quotes"
        MDType = block_to_block_type(MDText)
        self.assertEqual(MDType, BlockType.QUOTE)

    def test_text(self):
        MDText = "Sup"
        MDType = block_to_block_type(MDText)
        self.assertEqual(MDType, BlockType.PARAGRAPH)

    def test_ord_list(self):
        MDText = "1. Hi\n2.Hello\n3.G'morning"
        MDType = block_to_block_type(MDText)
        self.assertEqual(MDType, BlockType.ORDERED_LIST)

    def test_unord_list(self):
        MDText = "- Hi\n- Hello\n- G'morning"
        MDType = block_to_block_type(MDText)
        self.assertEqual(MDType, BlockType.UNORDERED_LIST)


class Test_MD_to_HTML_Node(unittest.TestCase):
    def test_heading(self):
        md = """

# Tolkien Fan Club

## Tolkien Fan Club 2

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        print(html)
        self.assertEqual(
            html,
            "<div><h1>Tolkien Fan Club</h1><h2>Tolkien Fan Club 2</h2></div>",
        )

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

    def test_quoteblock(self):
        md = """

> The power of love is bullsh*t. Swords and violence. That's where the money is.
> There's no need to wonder where your god is. Cause he's right here and he's fresh out of mercy. 

Kirito from the Kirito is Always Right Foundation
"""

        node = markdown_to_html_node(md)
        html = node.to_html()

        print(html)

    def test_ordered_list(self):
        md = """

1. The power of love is bullsh*t. Swords and violence. That's where the money is.
2. There's no need to wonder where your god is. Cause he's right here and he's fresh out of mercy. 

Brought to you by Kirito from the Kirito is Always Right Foundation
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        print(f"\n\n\nHTML:{html}\n\n\n")
        self.assertEqual(
            html,
            "<div><ol><li>The power of love is bullsh*t. Swords and violence. That's where the money is.</li><li>There's no need to wonder where your god is. Cause he's right here and he's fresh out of mercy.</li></ol><p>Brought to you by Kirito from the Kirito is Always Right Foundation</p></div>",
        )

    def test_unordered_list(self):
        md = """

- The power of love is bullsh*t. Swords and violence. That's where the money is.
- There's no need to wonder where your god is. Cause he's right here and he's fresh out of mercy. 

Brought to you by Kirito from the Kirito is Always Right Foundation
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        print(f"\n\n\nHTML:{html}\n\n\n")
        self.assertEqual(
            html,
            "<div><ul><li>The power of love is bullsh*t. Swords and violence. That's where the money is.</li><li>There's no need to wonder where your god is. Cause he's right here and he's fresh out of mercy.</li></ul><p>Brought to you by Kirito from the Kirito is Always Right Foundation</p></div>",
        )


class Test_Extract_Title(unittest.TestCase):
    def test_extract_title(self):
        md = """
# title is title

"""
        title = extract_title(md)
        self.assertEqual("title is title", title)
