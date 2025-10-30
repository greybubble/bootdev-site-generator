from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("Error: Leaf Node doesn't have a value!")
        
        if self.children:
            raise ValueError("Error: Leaf Node shouldn't have children but does!")
        
        if not self.tag:    
            return self.value
        
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
    
 
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
