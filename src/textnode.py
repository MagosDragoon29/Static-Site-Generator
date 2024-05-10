from htmlnode import LeafNode
import copy

text_type_text = "text" #no delimiter
text_type_bold = "bold" #double asterisk delimiter
text_type_italic = "italic" #single asterisk delimiter
text_type_code = "code" #delimiter: ``
text_type_link = "link" #delimiter is []
text_type_image = "image" #delimiter is ![title](link)

class  TextNode:
    def __init__(self, TEXT, TEXT_TYPE, URL=None):
        self.text = TEXT
        self.text_type = TEXT_TYPE
        self.url = URL
   
    def __repr__(self):
        if self.url is None: 
            return f"Textnode({self.text}, {self.text_type})"
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
   
    def __eq__(self, other):
        if isinstance(other, TextNode):
            return (self.text == other.text and
                    self.text_type == other.text_type and
                    self.url == other.url)
            return False

def text_node_to_html_node(text_node):
    if text_node.text_type == text_type_text:
        return LeafNode(None, text_node.text)
    if text_node.text_type == text_type_bold:
        return LeafNode("b", text_node.text)
    if text_node.text_type == text_type_italic:
        return LeafNode("i", text_node.text)
    if text_node.text_type == text_type_code:
        return LeafNode("code", text_node.text)
    if text_node.text_type == text_type_link:
        return LeafNode("a", text_node.text, {"href" : text_node.url})
    if text_node.text_type == text_type_image:
        return LeafNode("img", "", {"src":text_node.url, "alt":text_node.text})
    else:
        raise Exception (f"unsupported text type: {text_node.text_type}")       
    


        