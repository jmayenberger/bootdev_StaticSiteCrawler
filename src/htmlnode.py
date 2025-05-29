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