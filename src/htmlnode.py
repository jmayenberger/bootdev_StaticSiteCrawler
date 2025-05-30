class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag #A string representing the HTML tag name (e.g. "p", "a", "h1", etc.)
        self.value = value # string representing the value of the HTML tag (e.g. the text inside a paragraph)
        self.children = children #A list of HTMLNode objects representing the children of this node
        self.props = props #A dictionary of key-value pairs representing the attributes of the HTML tag. For example, a link (<a> tag) might have {"href": "https://www.google.com"}

    def to_html(self): #Child classes will override this method to render themselves as HTML
        raise NotImplementedError("override with child classes")
    
    def props_to_html(self): #returns a string that represents the HTML attributes of the node
        output = ""
        if self.props is None:
            return output
        for key in self.props:
            output += f" {key}=\"{self.props[key]}\""
        return output
    
    def __repr__(self):
        return f"(tag={self.tag}\n value={self.value}\n children={self.children}\n props={self.props})"
    

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None): #It should not allow for any children, The value data member should be required
        super().__init__(tag, value, props=props)

    def to_html(self): #method that renders a leaf node as an HTML string (by returning a string)
        if self.value is None: #f the leaf node has no value, it should raise a ValueError. All leaf nodes must have a value.
            raise ValueError("All leaf nodes must have a value")
        if self.tag is None: #If there is no tag (e.g. it's None), the value should be returned as raw text.
            return self.value #Otherwise, it should render an HTML tag
        return f"<{self.tag}{self.props_to_html()}>{self.value}<\\{self.tag}>"
