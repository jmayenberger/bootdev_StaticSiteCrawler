from enum import Enum

#allowed text types
class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "url"

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

