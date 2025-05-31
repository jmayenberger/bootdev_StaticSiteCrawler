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


if __name__ == "__main__":
    unittest.main()