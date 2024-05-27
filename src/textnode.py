class TextNode:

    def __init__ (self, text, text_type, url=None):

        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__ (self, second_textnode):

        if self.text == second_textnode.text and self.text_type == second_textnode.text_type and self.url == second_textnode.url:
            return True
        return False
        
    def __repr__ (self):

        return f"TextNode({self.text}, {self.text_type}, {self.url})"
