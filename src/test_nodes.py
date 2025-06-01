import unittest
from nodes import TextNode, HTMLNode, LeafNode, ParentNode
from my_types import TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node0 = TextNode("This is a text node", TextType.BOLD)
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.TEXT)
        node3 = TextNode("This is another text", TextType.BOLD)
        node4 = TextNode("I am testing", TextType.LINK, "www.dummy.org")
        node5 = TextNode("I am testing", TextType.LINK, "www.otherdummy.org")
        node6 = TextNode("I am not testing", TextType.LINK, "www.dummy.org")
        node7 = TextNode("I am testing", TextType.LINK, "www.dummy.org")
        node8 = TextNode("This is a text node", TextType.BOLD, "www.dummy.org")
        node_lst = [node0, node1, node2, node3, node4, node5, node6, node7, node8]
        for i in range(0,len(node_lst)):
            for j in range(i,len(node_lst)):
                if i == j:
                    self.assertEqual(node_lst[i], node_lst[j])
                elif (i == 0 and j == 1):
                    self.assertEqual(node_lst[i], node_lst[j])
                elif (i == 4 and j == 7):
                    self.assertEqual(node_lst[i], node_lst[j])
                else:
                    self.assertNotEqual(node_lst[i], node_lst[j])


class TestHTMLNode(unittest.TestCase):
    def test_propstohtml(self):
        node0 = HTMLNode("this is tag", "this is value", ["list", "of", "children"], {"props" : "is", "this" : "here"})
        expect0 = ' props="is" this="here"'
        node1 = HTMLNode("this is tag", "this is value", ["list", "of", "children"])
        expect1 = ""
        node2 = HTMLNode("this is tag", "this is value", props={"props" : "is", "this" : "here"})
        expect2 = ' props="is" this="here"'
        node3 = HTMLNode("this is tag", props={"props" : "is", "this" : "here"}, children=["list", "of", "children"])
        expect3 = ' props="is" this="here"'
        node4 = HTMLNode(value="this is value", children=["list", "of", "children"],props={"props" : "is", "this" : "here"})
        expect4 = ' props="is" this="here"'
        node5 = HTMLNode("<p>", "text here", props={"href" : "https://www.google.com", "target" : "_blank", "bla" : "blubb"})
        expect5 = ' href="https://www.google.com" target="_blank" bla="blubb"'
        nodes_lst = [node0, node1, node2, node3, node4, node5]
        expect_lst = [expect0, expect1, expect2, expect3, expect4, expect5]
        for i in range(0, len(nodes_lst)):
            self.assertEqual(expect_lst[i], nodes_lst[i].props_to_html())
            self.assertRaises(NotImplementedError, nodes_lst[i].to_html)
            for j in range(i, len(nodes_lst)):
                if i == j:
                    self.assertEqual(nodes_lst[i], nodes_lst[j])
                else:
                    self.assertNotEqual(nodes_lst[i], nodes_lst[j])

    def test_leaf_to_html(self):
            node0 = LeafNode("p", "Hello, world!")
            expect0 = "<p>Hello, world!</p>"
            node1 = LeafNode("p", "This is a paragraph of text.")
            expect1 = "<p>This is a paragraph of text.</p>"
            node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
            expect2 = '<a href="https://www.google.com">Click me!</a>'
            node3 = LeafNode("a", "text here", props={"href" : "https://www.google.com", "target" : "_blank", "bla" : "blubb"})
            expect3 = '<a href="https://www.google.com" target="_blank" bla="blubb">text here</a>'
            node4 = LeafNode(None, "raw text")
            expect4 = "raw text"

            node5 = LeafNode(None, None)
            self.assertRaises(ValueError, node5.to_html)

            nodes_lst = [node0, node1, node2, node3, node4]
            expect_lst = [expect0, expect1, expect2, expect3, expect4]
            for i in range(0, len(nodes_lst)):
                self.assertEqual(expect_lst[i], nodes_lst[i].to_html())
                for j in range(i, len(nodes_lst)):
                    if i == j:
                        self.assertEqual(nodes_lst[i], nodes_lst[j])
                    else:
                        self.assertNotEqual(nodes_lst[i], nodes_lst[j])

    def test_parent_to_html(self):
            node0 = ParentNode("div", [LeafNode("span", "child")])
            expect0 = "<div><span>child</span></div>"
            node1 = ParentNode("div", [ParentNode("span", [LeafNode("b", "grandchild")])])
            expect1 = "<div><span><b>grandchild</b></span></div>"
            node2 = ParentNode(tag="div", 
                               children=[
                                   ParentNode(tag="span", children=[LeafNode("b", "grandchild")]),
                                   LeafNode(tag="a", value="text here", props={"href" : "https://www.google.com", "target" : "_blank", "bla" : "blubb"})]
                               )
            expect2 = '<div><span><b>grandchild</b></span><a href="https://www.google.com" target="_blank" bla="blubb">text here</a></div>'
            node3 = ParentNode("p",[LeafNode("b", "Bold text"), LeafNode(None, "Normal text"), LeafNode("i", "italic text"), LeafNode(None, "Normal text"),])
            expect3 ="<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
            
            node4 = ParentNode(None, [LeafNode("span", "child")])
            self.assertRaises(ValueError, node4.to_html)

            node5 = ParentNode("a", None)
            self.assertRaises(ValueError, node5.to_html)


            nodes_lst = [node0, node1, node2, node3]
            expect_lst = [expect0, expect1, expect2, expect3]
            for i in range(0, len(nodes_lst)):
                self.assertEqual(expect_lst[i], nodes_lst[i].to_html())
                for j in range(i, len(nodes_lst)):
                    if i == j:
                        self.assertEqual(nodes_lst[i], nodes_lst[j])
                    else:
                        self.assertNotEqual(nodes_lst[i], nodes_lst[j])
            

if __name__ == "__main__":
    unittest.main()