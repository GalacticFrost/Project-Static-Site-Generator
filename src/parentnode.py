from htmlnode import HTMLNode

class ParentNode(HTMLNode):

    def __init__ (self, tag = None, children = None):

        super().__init__(tag=tag, children=children)

        if not self.tag:
            raise ValueError("ParentNode requires a tag.")
        if not self.children:
            raise ValueError("Parent node must have children.")
        
    def to_html (self):
        
        html_text = f'<{self.tag}>'

        for child in self.children:
            
            html_text += child.to_html()

        return f'{html_text}</{self.tag}>'