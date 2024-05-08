class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props is None:
            return ""
        x = self.props.items()
        prop_list = []
        for item in x:
            prop_list.append(f' {item[0]}="{item[1]}"')
        res = "".join(prop_list)
        return res

    def __str__(self):
        return f"This HTMLNode has tag: {self.tag}, value: {self.value}, children: {self.children} and props: {self.props}."
    
    def __eq__(self, other):
        if isinstance(other, HTMLNode):
            return (self.tag == other.tag and
                    self.value == other.value and
                    self.children == other.children and
                    self.props == other.props)
            return False
        
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value == None:
            raise ValueError("All leaf nodes require a value")
        if self.tag == None:
            return f"{self.value}"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
        
        
    def to_html(self):
        if self.tag == None:
            raise ValueError("a tag is requried for a ParentNode")
        if self.children == None:
            raise ValueError("children are required for a ParentNode")
        props_html = self.props_to_html()
        children_html = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}{props_html}>{children_html}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
        