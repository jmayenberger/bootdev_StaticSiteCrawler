
class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text #The text content of the node
        self.text_type = text_type #The type of text this node contains, which is a member of the TextType enum
        self.url = url #The URL of the link or image, if the text is a link. Default to None if nothing is passed in.
    
    def __eq__(self, other): #True if all of the properties of two TextNode objects are equal
        if (
            self.text == other.text and self.text_type == other.text_type and self.url == other.url
        ):
            return True
        else:
            return False
    
    def __repr__(self): #returns a string representation of the TextNode object
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag #A string representing the HTML tag name (e.g. "p", "a", "h1", etc.)
        self.value = value # string representing the value of the HTML tag (e.g. the text inside a paragraph)
        self.children = children #A list of HTMLNode objects representing the children of this node
        self.props = props #A dictionary of key-value pairs representing the attributes of the HTML tag. For example, a link (<a> tag) might have {"href": "https://www.google.com"}

    def to_html(self): #Child classes will override this method to render themselves as HTML
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self): #returns a string that represents the HTML attributes of the node
        output = ""
        if self.props is None:
            return output
        for key in self.props:
            output += f" {key}=\"{self.props[key]}\""
        return output
    
    def __eq__(self, other): #True if all of the properties of two HTMLNode objects are equal
        if (
            self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props
        ):
            return True
        else:
            return False
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"
    

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None): #It should not allow for any children, The value data member should be required
        super().__init__(tag, value, None, props)

    def to_html(self): #method that renders a leaf node as an HTML string (by returning a string)
        if self.value is None: #f the leaf node has no value, it should raise a ValueError. All leaf nodes must have a value.
            raise ValueError("invalid HTML for LeafNode: no value")
        if self.tag is None: #If there is no tag (e.g. it's None), the value should be returned as raw text.
            return self.value #Otherwise, it should render an HTML tag
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("invalid HTML for ParentNode: no tag")
        if self.children is None:
            raise ValueError("invalid HTML for ParentNode: no children")
        html_string = ""
        for child in self.children:
            html_string += child.to_html()
        return f"<{self.tag}>{html_string}</{self.tag}>"
    
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
