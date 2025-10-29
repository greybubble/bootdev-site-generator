from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("Error: Parent Node doesn't have a tag!")
        
        if not self.children:
            raise ValueError("Error: Parent Node doesn't have any children!")
        
        output = ""
        print(self)
        for child in self.children:
            print(child)
            output += child.to_html()

        return f'<{self.tag}{self.props_to_html()}>{output}</{self.tag}>'
    
    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"