import unittest
from textnode import TextNode, TextType


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


if __name__ == "__main__":
    unittest.main()