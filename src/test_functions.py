import unittest
from my_types import TextType, BlockType
from nodes import LeafNode, TextNode
from functions import (
    text_node_to_html_node, split_nodes_delimiter, extract_markdown_images,
    extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes,
    markdown_to_blocks, block_to_blocktype, markdown_to_html_node, extract_title)



class TestFunctions(unittest.TestCase):
    def test_extract_title(self):
        markdowns = []
        expects = []
        markdowns.append("# ")
        expects.append("")
        markdowns.append("# this is a title")
        expects.append("this is a title")
        markdowns.append("# #hello hello")
        expects.append("#hello hello")
        markdowns.append("# title\n# ignore this")
        expects.append("title")
        markdowns.append("first nothing\n# only now comes the title\n# not here")
        expects.append("only now comes the title")


        error_markdowns = []
        error_expects = []
        error_markdowns.append("this is not a title")
        error_expects.append(ValueError)
        error_markdowns.append("#this is also not a title")
        error_expects.append(ValueError)
        error_markdowns.append("## this is not the right title")
        error_expects.append(ValueError)

        for (i, markdown) in enumerate(markdowns):
            self.assertEqual(extract_title(markdown), expects[i])
        for (i, error_input) in enumerate(error_markdowns):
            self.assertRaises(error_expects[i], extract_title, error_input)

    def test_markdown_to_html_node(self):
        lst_markdown = []
        lst_expects = []
        lst_markdown.append("""
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

## This is a **bold** heading

```
This is text that _should_ remain
the **same** even with inline stuff
```

>I **hate**
> HTML so much.
>It is _dogshit_

- this **is** my
- my `unordered` list

1. this **is** my
2. my `ordered` list

""")
        lst_expects.append("<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p><h2>This is a <b>bold</b> heading</h2><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre><blockquote>I <b>hate</b> HTML so much. It is <i>dogshit</i></blockquote><ul><li>this <b>is</b> my</li><li>my <code>unordered</code> list</li></ul><ol><li>this <b>is</b> my</li><li>my <code>ordered</code> list</li></ol></div>")
        lst_markdown.append("")
        lst_expects.append("<div></div>")
        lst_markdown.append("###### a")
        lst_expects.append("<div><h6>a</h6></div>")
        lst_markdown.append("``````")
        lst_expects.append("<div><pre><code></code></pre></div>")
        lst_markdown.append(">")
        lst_expects.append("<div><blockquote></blockquote></div>")
        lst_markdown.append("- \n- a")
        lst_expects.append("<div><ul><li></li><li>a</li></ul></div>")
        lst_markdown.append("1. \n2. a")
        lst_expects.append("<div><ol><li></li><li>a</li></ol></div>")


        for (i, markdown) in enumerate(lst_markdown):
            self.assertEqual(markdown_to_html_node(markdown).to_html(), lst_expects[i])

    def test_block_to_blocktype(self):
        lst_blocks = []
        lst_expected = []
        lst_blocks.append("")
        lst_expected.append(BlockType.PARAGRAPH)
        lst_blocks.append("nothing here\nor here")
        lst_expected.append(BlockType.PARAGRAPH)
        lst_blocks.append("######not a heading")
        lst_expected.append(BlockType.PARAGRAPH)
        lst_blocks.append("##not a heading either")
        lst_expected.append(BlockType.PARAGRAPH)
        lst_blocks.append("####### also not a heading")
        lst_expected.append(BlockType.PARAGRAPH)
        lst_blocks.append("```not a code block``")
        lst_expected.append(BlockType.PARAGRAPH)
        lst_blocks.append("`not a code block```")
        lst_expected.append(BlockType.PARAGRAPH)
        lst_blocks.append("`````a")
        lst_expected.append(BlockType.PARAGRAPH)
        lst_blocks.append(">not\na\n>quote block")
        lst_expected.append(BlockType.PARAGRAPH)
        lst_blocks.append(">also\n\n>not a quote block")
        lst_expected.append(BlockType.PARAGRAPH)
        lst_blocks.append("-")
        lst_expected.append(BlockType.PARAGRAPH)
        lst_blocks.append("- this\n-is\n- not a list")
        lst_expected.append(BlockType.PARAGRAPH)
        lst_blocks.append("- this\n\n- is also not a list")
        lst_expected.append(BlockType.PARAGRAPH)
        lst_blocks.append("- this is\nnot a list")
        lst_expected.append(BlockType.PARAGRAPH)
        lst_blocks.append("2. this\n3. list is not\n4. ordered")
        lst_expected.append(BlockType.PARAGRAPH)
        lst_blocks.append("1. this\n3. list is unordered")
        lst_expected.append(BlockType.PARAGRAPH)
        lst_blocks.append("1. this\n2. list is also\n3.unordered")
        lst_expected.append(BlockType.PARAGRAPH)
        lst_blocks.append("# ")
        lst_expected.append(BlockType.HEADING)
        lst_blocks.append("### ")
        lst_expected.append(BlockType.HEADING)
        lst_blocks.append("###### ")
        lst_expected.append(BlockType.HEADING)
        lst_blocks.append("# this is a heading")
        lst_expected.append(BlockType.HEADING)
        lst_blocks.append("###### this is another heading")
        lst_expected.append(BlockType.HEADING)
        lst_blocks.append("``````")
        lst_expected.append(BlockType.CODE)
        lst_blocks.append("```this is a code block```")
        lst_expected.append(BlockType.CODE)
        lst_blocks.append("```this is another\ncode block```")
        lst_expected.append(BlockType.CODE)
        lst_blocks.append(">this is a quote block")
        lst_expected.append(BlockType.QUOTE)
        lst_blocks.append(">")
        lst_expected.append(BlockType.QUOTE)
        lst_blocks.append(">\n>\n>")
        lst_expected.append(BlockType.QUOTE)
        lst_blocks.append(">this are\n>multiple lines\n>in a quote block")
        lst_expected.append(BlockType.QUOTE)
        lst_blocks.append("- ")
        lst_expected.append(BlockType.UNORDERED_LIST)
        lst_blocks.append("- \n- \n- ")
        lst_expected.append(BlockType.UNORDERED_LIST)
        lst_blocks.append("- unorderd list")
        lst_expected.append(BlockType.UNORDERED_LIST)
        lst_blocks.append("- this\n- is an\n- unordered list")
        lst_expected.append(BlockType.UNORDERED_LIST)
        lst_blocks.append("1. ")
        lst_expected.append(BlockType.ORDERED_LIST)
        lst_blocks.append("1. \n2. \n3. ")
        lst_expected.append(BlockType.ORDERED_LIST)
        lst_blocks.append("1. ordered list")
        lst_expected.append(BlockType.ORDERED_LIST)
        lst_blocks.append("1. this\n2. is a\n3. ordered list")
        lst_expected.append(BlockType.ORDERED_LIST)

        for (i, block) in enumerate(lst_blocks):
            self.assertEqual(block_to_blocktype(block), lst_expected[i])

    def test_markdown_to_blocks(self):
        lst_markdowns = []
        lst_expects = []
        lst_markdowns.append("""
This is **bolded** paragraph

                             
    This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line    

- This is a list
- with items
""")
        lst_expects.append([
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ])
        lst_markdowns.append("single paragraph")
        lst_expects.append(["single paragraph"])
        lst_markdowns.append("")
        lst_expects.append([])
        lst_markdowns.append("\n\n\n\n\n   \n  \n\n  \n   \n      \n \n\n     ")
        lst_expects.append([])

        for (i, markdown) in enumerate(lst_markdowns):
            self.assertEqual(markdown_to_blocks(markdown), lst_expects[i])

    def test_text_to_textnodes(self):
        lst_texts = []
        lst_expects = []
        lst_texts.append("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        lst_expects.append([
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev")
        ])
        lst_texts.append("**bold**")
        lst_expects.append([TextNode("bold", TextType.BOLD)])
        lst_texts.append("_italic_")
        lst_expects.append([TextNode("italic", TextType.ITALIC)])
        lst_texts.append("`code`")
        lst_expects.append([TextNode("code", TextType.CODE)])
        lst_texts.append("[link](here)")
        lst_expects.append([TextNode("link", TextType.LINK, "here")])
        lst_texts.append("![image](here)")
        lst_expects.append([TextNode("image", TextType.IMAGE, "here")])
        lst_texts.append("![first](image) then **bold** _and then _[a](link)")
        lst_expects.append([
            TextNode("first", TextType.IMAGE, "image"),
            TextNode(" then ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" ", TextType.TEXT),
            TextNode("and then ", TextType.ITALIC),
            TextNode("a", TextType.LINK, "link")
        ])

        for (i, text) in enumerate(lst_texts):
            self.assertEqual(text_to_textnodes(text), lst_expects[i])

        lst_error_texts = []
        lst_errors_expects = []
        lst_error_texts.append("**bold but not delimiter")
        lst_errors_expects.append(ValueError)

        for (i, error_text) in enumerate(lst_error_texts):
            self.assertRaises(lst_errors_expects[i], text_to_textnodes, error_text)

    def test_text_node_to_html_node(self):
        node0 = text_node_to_html_node(TextNode("This is a text node", TextType.TEXT))
        expect0 = LeafNode(None, "This is a text node")
        node1 = text_node_to_html_node(TextNode("This is a bold node", TextType.BOLD))
        expect1 = LeafNode("b", "This is a bold node")
        node2 = text_node_to_html_node(TextNode("This is an italic node", TextType.ITALIC))
        expect2 = LeafNode("i", "This is an italic node")
        node3 = text_node_to_html_node(TextNode("This is a code node", TextType.CODE))
        expect3 = LeafNode("code", "This is a code node")
        node4 = text_node_to_html_node(TextNode("This is a link node", TextType.LINK, "https://www.google.com"))
        expect4 = LeafNode("a", "This is a link node", {"href" : "https://www.google.com"})
        node5 = text_node_to_html_node(TextNode("This is an image node", TextType.IMAGE, "path/is/here.png"))
        expect5 = LeafNode("img", "", {"src" : "path/is/here.png", "alt" : "This is an image node"})
        
        self.assertRaises(ValueError, text_node_to_html_node, TextNode("This is an invalid text node", 5))


        nodes_lst = [node0, node1, node2, node3, node4, node5]
        expect_lst = [expect0, expect1, expect2, expect3, expect4, expect5]
        for i in range(0, len(nodes_lst)):
            self.assertEqual(expect_lst[i], nodes_lst[i])
            for j in range(i, len(nodes_lst)):
                if i == j:
                    self.assertEqual(nodes_lst[i], nodes_lst[j])
                else:
                    self.assertNotEqual(nodes_lst[i], nodes_lst[j])

    def test_split_nodes_delimiter(self):
        lst_inputs = []
        lst_expects = []
        lst_inputs.append([[TextNode("This is text with a `code block` word", TextType.TEXT)], "`", TextType.CODE])
        lst_expects.append([
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ])
        lst_inputs.append([[TextNode("This is text with a **bold** word", TextType.TEXT)], "**", TextType.BOLD])
        lst_expects.append([
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ])
        lst_inputs.append([[TextNode("This is text with an _italic_ word", TextType.TEXT)], "_", TextType.ITALIC])
        lst_expects.append([
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ])
        lst_inputs.append([[TextNode("This is text without a delimiter", TextType.TEXT)], "", TextType.TEXT])
        lst_expects.append([
            TextNode("This is text without a delimiter", TextType.TEXT),
        ])
        lst_inputs.append([[TextNode("`code block`", TextType.TEXT)], "`", TextType.CODE])
        lst_expects.append([TextNode("code block", TextType.CODE)])
        lst_inputs.append([[TextNode("**bold**", TextType.TEXT)], "**", TextType.BOLD])
        lst_expects.append([TextNode("bold", TextType.BOLD)])
        lst_inputs.append([[TextNode("_italic_", TextType.TEXT)], "_", TextType.ITALIC])
        lst_expects.append([TextNode("italic", TextType.ITALIC)])
        lst_inputs.append([[lst_inputs[0][0][0], lst_inputs[4][0][0]], "`", TextType.CODE])
        lst_expects.append(lst_expects[0].copy())
        lst_expects[7].extend(lst_expects[4])
        lst_inputs.append([[lst_inputs[1][0][0], lst_inputs[5][0][0]], "**", TextType.BOLD])
        lst_expects.append(lst_expects[1].copy())
        lst_expects[8].extend(lst_expects[5])
        lst_inputs.append([[lst_inputs[2][0][0], lst_inputs[6][0][0]], "_", TextType.ITALIC])
        lst_expects.append(lst_expects[2].copy())
        lst_expects[9].extend(lst_expects[6])
        lst_inputs.append([[TextNode("there is no code here", TextType.TEXT)], lst_inputs[0][1], lst_inputs[0][2]])
        lst_expects.append([TextNode("there is no code here", TextType.TEXT)])
        lst_inputs.append([[TextNode("there is the wrong **delimiter** here", TextType.TEXT)], lst_inputs[0][1], lst_inputs[0][2]])
        lst_expects.append([TextNode("there is the wrong **delimiter** here", TextType.TEXT)])
        #todo: add double delimiter inupt here
        lst_inputs.append([[TextNode("**so** much **bold**", TextType.TEXT),
                            TextNode("text **in** here **I**", TextType.TEXT),
                            TextNode("**am** going **to** suffocate", TextType.TEXT)],
                           "**", TextType.BOLD])
        lst_expects.append([
            TextNode("so", TextType.BOLD),
            TextNode(" much ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode("text ", TextType.TEXT),
            TextNode("in", TextType.BOLD),
            TextNode(" here ", TextType.TEXT),
            TextNode("I", TextType.BOLD),
            TextNode("am", TextType.BOLD),
            TextNode(" going ", TextType.TEXT),
            TextNode("to", TextType.BOLD),
            TextNode(" suffocate", TextType.TEXT),
        ])
        for i in range(0, len(lst_inputs)):
            self.assertEqual(split_nodes_delimiter(*lst_inputs[i]), lst_expects[i])

        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )
        
        lst_error_inputs = []
        lst_error_expects = []
        lst_error_inputs.append([lst_inputs[0][0], lst_inputs[0][1], lst_inputs[1][2]])
        lst_error_expects.append(ValueError)
        lst_error_inputs.append([lst_inputs[0][0], lst_inputs[1][1], lst_inputs[0][2]])
        lst_error_expects.append(ValueError)
        lst_error_inputs.append([lst_inputs[0][0], lst_inputs[0][1], TextType.LINK])
        lst_error_expects.append(NotImplementedError)
        lst_error_inputs.append([[TextNode("there are `too few delimiters here", TextType.TEXT)], lst_inputs[0][1], lst_inputs[0][2]])
        lst_error_expects.append(ValueError)
        lst_error_inputs.append([[TextNode("there `are` too many `delimiters here", TextType.TEXT)], lst_inputs[0][1], lst_inputs[0][2]])
        lst_error_expects.append(ValueError)
        for i in range(0, len(lst_error_inputs)):
            self.assertRaises(lst_error_expects[i], split_nodes_delimiter, *lst_error_inputs[i])

    def test_split_nodes_image(self):
        lst_nodes = []
        lst_expects = []
        lst_nodes.append([TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) and following text",TextType.TEXT)])
        lst_expects.append([
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            TextNode(" and following text", TextType.TEXT)
        ])
        lst_nodes.append([TextNode("![image](https://i.imgur.com/zjjcJKZ.png) and the same again ![image](https://i.imgur.com/zjjcJKZ.png)",TextType.TEXT)])
        lst_expects.append([
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and the same again ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")
        ])
        lst_nodes.append([TextNode("![image](https://i.imgur.com/zjjcJKZ.png)![image](https://i.imgur.com/zjjcJKZ.png)",TextType.TEXT)])
        lst_expects.append([
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")
        ])
        lst_nodes.append([TextNode("",TextType.TEXT)])
        lst_expects.append([])
        lst_nodes.append([TextNode("only text", TextType.TEXT)])
        lst_expects.append([TextNode("only text", TextType.TEXT)])

        for (i, node) in enumerate(lst_nodes):
            self.assertEqual(split_nodes_image(node), lst_expects[i])

    def test_split_nodes_link(self):
        lst_nodes = []
        lst_expects = []
        lst_nodes.append([TextNode("This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png) and following text",TextType.TEXT)])
        lst_expects.append([
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
            TextNode(" and following text", TextType.TEXT)
        ])
        lst_nodes.append([TextNode("[link](https://i.imgur.com/zjjcJKZ.png) and the same again [link](https://i.imgur.com/zjjcJKZ.png)",TextType.TEXT)])
        lst_expects.append([
            TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and the same again ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png")
        ])
        lst_nodes.append([TextNode("[link](https://i.imgur.com/zjjcJKZ.png)[link](https://i.imgur.com/zjjcJKZ.png)",TextType.TEXT)])
        lst_expects.append([
            TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png")
        ])
        lst_nodes.append([TextNode("",TextType.TEXT)])
        lst_expects.append([])
        lst_nodes.append([TextNode("only text", TextType.TEXT)])
        lst_expects.append([TextNode("only text", TextType.TEXT)])

        for (i, node) in enumerate(lst_nodes):
            self.assertEqual(split_nodes_link(node), lst_expects[i])

    def test_extract_markdown_images(self):
        lst_texts = []
        lst_expects = []
        lst_texts.append("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")
        lst_expects.append([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])
        lst_texts.append("![edge]()![](case)")
        lst_expects.append([("edge", ""), ("","case")])
        lst_texts.append("![wrong]!(syntax)(all)![over]the(place)and[here](a link)")
        lst_expects.append([])
        
        for (i, text) in enumerate(lst_texts):
            self.assertEqual(extract_markdown_images(text), lst_expects[i])

    def test_extract_markdown_links(self):
        lst_texts = []
        lst_expects = []
        lst_texts.append("This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")
        lst_expects.append([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])
        lst_texts.append("[edge]()[](case)")
        lst_expects.append([("edge", ""), ("","case")])
        lst_texts.append("[wrong]!(syntax)(all)[over](the(place)and![here](an image)")
        lst_expects.append([])
        
        for (i, text) in enumerate(lst_texts):
            self.assertEqual(extract_markdown_links(text), lst_expects[i])


if __name__ == "__main__":
    unittest.main()