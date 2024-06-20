from htmlnode import HTMLNode

class LeafNode(HTMLNode):

    def __init__(self, tag=None, value=None, props=None):
        
        super().__init__(tag=tag, value=value, props=props)
        
    def to_html(self):

        if not self.value and self.tag != 'img':
            raise ValueError ('Value is required for all tags except \'img\'')
        
        if not self.tag:
            return self.value
        
        # Process props if there are any
        if self.props:
            props_str = " ".join(f'{key}="{value}"' for key, value in self.props.items())
            props_str = f" {props_str}"  # Adds leading space for the props string
        else:
            props_str = ""  # Empty string if no props

        # Check for 'img' tag to handle it separately
        if self.tag == 'img':
            return f'<{self.tag}{props_str}></{self.tag}>'
        
        if self.tag == 'blockquote':
            return f'<{self.tag}{props_str}>\n   {self.value}\n</{self.tag}>'
        
        if self.tag in {'ul', 'ol'}:
            if not isinstance(self.value, list):
                raise ValueError(f"Value for {self.tag} tag must be a list")
            list_items = ''.join(f'<li>{item}</li>' for item in self.value)
            return f'<{self.tag}{props_str}>{list_items}</{self.tag}>'

        # General case for all other tags
        return f'<{self.tag}{props_str}>{self.value}</{self.tag}>'
