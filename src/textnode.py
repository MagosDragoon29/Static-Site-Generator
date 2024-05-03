class  TextNode:
    def __init__(self, TEXT, TEXT_TYPE, URL):
        self.text = TEXT
        self.text_type = TEXT_TYPE
        self.url = URL
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"