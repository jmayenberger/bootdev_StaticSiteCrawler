from textnode import TextNode, TextType
from htmlnode import LeafNode

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href" : text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src" : text_node.url, "alt" : text_node.text})
        case _:
            raise ValueError(f"invalid text type for TextNode: {text_node.text_type}")

# takes a list of "old nodes", a delimiter, and a text type. returns a new list of nodes, where any "text" type nodes in the input list are (potentially) split into multiple nodes based on the syntax        
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    match text_type:
        case TextType.TEXT:
            if delimiter != "":
                raise ValueError(f"delimiter \"{delimiter}\" does not match text_type \"{text_type.value}\"")
        case TextType.BOLD:
            if delimiter != "**":
                raise ValueError(f"delimiter \"{delimiter}\" does not match text_type \"{text_type.value}\"")
        case TextType.ITALIC:
            if delimiter != "_":
                raise ValueError(f"delimiter \"{delimiter}\" does not match text_type \"{text_type.value}\"")
        case TextType.CODE:
            if delimiter != "`":
                raise ValueError(f"delimiter \"{delimiter}\" does not match text_type \"{text_type.value}\"")
        case _:
            raise NotImplementedError(f"{text_type} not implemented")
    
    if text_type == TextType.TEXT:
        return old_nodes
    
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        split_lst = node.text.split(delimiter)
        if len(split_lst) % 2 == 0:
            raise ValueError(f"Wrong number of delimiter \"{delimiter}\" in \"{node.text}\"")
        for i in range(0, len(split_lst)):
                if split_lst[i] == "":
                    continue
                elif i % 2 == 0:
                    new_nodes.append(TextNode(split_lst[i], TextType.TEXT))
                else:
                    new_nodes.append(TextNode(split_lst[i], text_type))
    return new_nodes


