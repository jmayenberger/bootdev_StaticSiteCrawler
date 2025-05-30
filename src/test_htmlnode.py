import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

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
        expcect_lst = [expect0, expect1, expect2, expect3, expect4, expect5]
        for i in range(0, len(nodes_lst)):
            self.assertEqual(expcect_lst[i], nodes_lst[i].props_to_html())
            self.assertRaises(NotImplementedError, nodes_lst[i].to_html)

        def test_leaf_to_html(self):
            node0 = LeafNode("p", "Hello, world!")
            expect0 = "<p>Hello, world!</p>"
            node1 = LeafNode("p", "This is a paragraph of text.")
            expect1 = "<p>This is a paragraph of text.</p>"
            node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
            expect2 = '<a href="https://www.google.com">Click me!</a>'
            node3 = LeafNode("a", "text here", props={"href" : "https://www.google.com", "target" : "_blank", "bla" : "blubb"})
            expect3 = '<a href="https://www.google.com" target="_blank" bla="blubb">text here<a\\>'
            node4 = LeafNode(None, "raw text")
            expect4 = "raw text"

            node5 = LeafNode(None, None)
            self.assertRaises(ValueError, node5.to_html())

            nodes_lst = [node0, node1, node2, node3, node4]
            expcect_lst = [expect0, expect1, expect2, expect3, expect4]
            for i in range(0, len(nodes_lst)):
                self.assertEqual(expcect_lst[i], nodes_lst[i].to_html())

        def test_parent_to_html(self):
            node0 = ParentNode("div", [LeafNode("span", "child")])
            expect0 = "<div><span>child</span></div>"
            node1 = ParentNode("div", [ParentNode("span", [LeafNode("b", "grandchild")])])
            expect1 = "<div><span><b>grandchild</b></span></div>"
            node2 = ParentNode("div", [ParentNode("span", [LeafNode("b", "grandchild")]), LeafNode("a", "text here", props={"href" : "https://www.google.com", "target" : "_blank", "bla" : "blubb"})])
            expect2 = '<div><span><b>grandchild</b><a href="https://www.google.com">Click me!</a></span></div>'
            node3 = ParentNode("p",[LeafNode("b", "Bold text"), LeafNode(None, "Normal text"), LeafNode("i", "italic text"), LeafNode(None, "Normal text"),])
            expect3 ="<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
            
            node4 = ParentNode(None, [LeafNode("span", "child")])
            self.assertRaises(ValueError, node4.to_html())

            node5 = ParentNode("a", None)
            self.assertRaises(ValueError, node5.to_html())


            nodes_lst = [node0, node1, node2, node3]
            expcect_lst = [expect0, expect1, expect2, expect3]
            for i in range(0, len(nodes_lst)):
                self.assertEqual(expcect_lst[i], nodes_lst[i].to_html())
            

if __name__ == "__main__":
    unittest.main()