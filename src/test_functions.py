import unittest
from textnode import TextNode, TextType
from htmlnode import LeafNode
from functions import text_node_to_html_node, split_nodes_delimiter



class TestFunctions(unittest.TestCase):
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
        input0 = [[TextNode("This is text with a `code block` word", TextType.TEXT)], "`", TextType.CODE]
        expect0 = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        input1 = [[TextNode("This is text with a **bold** word", TextType.TEXT)], "**", TextType.BOLD]
        expect1 = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ]
        input2 = [[TextNode("This is text with an _italic_ word", TextType.TEXT)], "_", TextType.ITALIC]
        expect2 = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ]
        input3 = [[TextNode("This is text without a delimiter", TextType.TEXT)], "", TextType.TEXT]
        expect3 = [
            TextNode("This is text without a delimiter", TextType.TEXT),
        ]
        input4 = [[TextNode("`code block`", TextType.TEXT)], "`", TextType.CODE]
        expect4 = [TextNode("code block", TextType.CODE)]
        input5 = [[TextNode("**bold**", TextType.TEXT)], "**", TextType.BOLD]
        expect5 = [TextNode("bold", TextType.BOLD)]
        input6 = [[TextNode("_italic_", TextType.TEXT)], "_", TextType.ITALIC]
        expect6 = [TextNode("italic", TextType.ITALIC)]
        input7 = [[input0[0][0], input4[0][0]], "`", TextType.CODE]
        expect7 = expect0.copy()
        expect7.extend(expect4)
        input8 = [[input1[0][0], input5[0][0]], "**", TextType.BOLD]
        expect8 = expect1.copy()
        expect8.extend(expect5)
        input9 = [[input2[0][0], input6[0][0]], "_", TextType.ITALIC]
        expect9 = expect2.copy()
        expect9.extend(expect6)
        lst_inputs = [input0, input1, input2, input3, input4, input5, input6, input7, input8, input9]
        lst_expects = [expect0, expect1, expect2, expect3, expect4, expect5, expect6, expect7, expect8, expect9]
        for i in range(0, len(lst_inputs)):
            self.assertEqual(split_nodes_delimiter(*lst_inputs[i]), lst_expects[i])
        
        error_input0 = [input0[0], input0[1], input1[2]]
        error_expect0 = ValueError
        error_input1 = [input0[0], input1[1], input0[2]]
        error_expect1 = ValueError
        error_input2 = [input0[0], input0[1], TextType.LINK]
        error_expect2 = NotImplementedError
        error_input3 = [[TextNode("there is no code here", TextType.TEXT)], input0[1], input0[2]]
        error_expect3 = ValueError
        error_input4 = [[TextNode("there is the wrong **delimiter** here", TextType.TEXT)], input0[1], input0[2]]
        error_expect4 = ValueError
        error_input5 = [[TextNode("there are `too few delimiters here", TextType.TEXT)], input0[1], input0[2]]
        error_expect5 = ValueError
        error_input6 = [[TextNode("there `are` too many `delimiters here", TextType.TEXT)], input0[1], input0[2]]
        error_expect6 = ValueError
        lst_error_inputs = [error_input0, error_input1, error_input2, error_input3, error_input4, error_input5, error_input6]
        lst_error_expects = [error_expect0, error_expect1, error_expect2, error_expect3, error_expect4, error_expect5, error_expect6]
        for i in range(0, len(lst_error_inputs)):
            self.assertRaises(lst_error_expects[i], split_nodes_delimiter, *lst_error_inputs[i])


if __name__ == "__main__":
    unittest.main()