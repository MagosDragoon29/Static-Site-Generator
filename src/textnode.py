class  TextNode:
    def __init__(self, TEXT, TEXT_TYPE, URL):
        self.text = TEXT
        self.text_type = TEXT_TYPE
        self.url = URL
   
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
   
    def __eq__(self, other):
        if isinstance(other, TextNode):
            return (self.text == other.text and
                    self.text_type == other.text_type and
                    self.url == other.url)
            return False
        
    def text_node_to_html_node(text_node):
        pass