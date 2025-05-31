import unittest
from textnode import TextNode, TextType
from htmlnode import LeafNode
from functions import text_node_to_html_node



class TestTextNodeToHTMLNode(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()