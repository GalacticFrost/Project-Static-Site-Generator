import re

class TextNode:

    def __init__ (self, text, text_type=None, url=None):

        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__ (self, second_textnode):

        if self.text == second_textnode.text and self.text_type == second_textnode.text_type and self.url == second_textnode.url:
            return True
        return False
        
    def __repr__ (self):

        return f"TextNode({self.text}, {self.text_type}, {self.url})"

##__________Split Markdown Text into Textnodes__________##

def split_nodes_delimiter(sentence, delimiters):
    valid_delim = {
        '`': 'code',
        '*': 'italic',
        '**': 'bold'
    }

    # Ensure delimiters are valid
    for delimiter in delimiters:
        if delimiter not in valid_delim:
            raise Exception(f'{delimiter} is not a valid markdown syntax. Review your input.')

    escaped_delimiters = sorted([re.escape(delim) for delim in delimiters], key=len, reverse=True)
    delim_pattern = '|'.join(escaped_delimiters)
    parts = re.split(f'({delim_pattern})', sentence)  # Split the sentence and keep delimiters

    textnode_list = []
    current_text = ""
    current_type = "text"
    stack = []

    for part in parts:
        if part in valid_delim.keys():  # Check against original delimiters
            if stack and stack[-1] == part:
                # Close the last opened delimiter
                if current_text:
                    textnode_list.append(TextNode(current_text, current_type))
                    current_text = ""
                stack.pop()
                current_type = "text" if not stack else valid_delim[stack[-1]]
            else:
                if current_text:
                    textnode_list.append(TextNode(current_text, current_type))
                    current_text = ""
                stack.append(part)
                current_type = valid_delim[part]
        else:
            current_text += part

    if current_text:
        if stack:
            raise Exception(f"Unmatched delimiter in text: {sentence}")
        textnode_list.append(TextNode(current_text, "text"))

    return textnode_list

##__________Extract Markdown Images__________##

def extract_markdown_images(text):

    pattern = r'!\[(.*?)\]\((.*?)(?:\s*".*?")?\)'

    if not text:
        return []
    return re.findall(pattern, text)

##__________Extract Markdown Links__________##

def extract_markdown_links(text):

    pattern = r'\[(.*?)\]\((.*?)(?:\s*".*?")?\)'

    if not text: 
        return []
    return re.findall(pattern, text)

