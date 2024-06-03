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

##__________Split Markdown Image into Textnodes__________##

def split_nodes_images(old_nodes):

    textnode_list = []

    for node in old_nodes:
        if node.text_type == "text":
            images_extracted = extract_markdown_images(node.text)

            if not images_extracted:
                textnode_list.append(node)
                continue

            split_text = node.text
            for image_alt, image_url in images_extracted:
                parts = split_text.split(f"![{image_alt}]({image_url})", 1)
                if parts[0].strip():
                    textnode_list.append(TextNode(parts[0], "text"))
                textnode_list.append(TextNode(image_alt, "image", image_url))
                split_text = parts[1] if len(parts) > 1 else ""
            
            if split_text.strip():
                textnode_list.append(TextNode(split_text, "text"))
        else:
            textnode_list.append(node)
    
    return textnode_list

##__________Split Markdown Link into Textnodes__________##

def split_nodes_links(old_nodes):

    textnode_list = []

    for node in old_nodes:
        if node.text_type == "text":
            links_extracted = extract_markdown_links(node.text)

            if not links_extracted:
                textnode_list.append(node)
                continue

            split_text = node.text
            for link_text, link_url in links_extracted:
                parts = split_text.split(f"[{link_text}]({link_url})", 1)
                if parts[0].strip():
                    textnode_list.append(TextNode(parts[0], "text"))
                textnode_list.append(TextNode(link_text, "link", link_url))
                split_text = parts[1] if len(parts) > 1 else ""
            
            if split_text.strip():
                textnode_list.append(TextNode(split_text, "text"))
        else:
            textnode_list.append(node)
    
    return textnode_list

##__________Split Markdown Headings and Blockqoute into Textnodes__________##

def split_nodes_heading_and_blockquote(text):
    
    heading_pattern = re.compile(r'^(\#{1,6}) (.*)$')
    blockquote_pattern = re.compile(r'^> (.*)$')

    lines = text.splitlines(keepends=True)  # keepends=True preserves newline characters
    textnode_list = []
    current_text = ""
    current_type = "text"

    for line in lines:
        heading_match = heading_pattern.match(line)
        blockquote_match = blockquote_pattern.match(line)

        if heading_match:
            if current_text:  # Add any accumulated text before switching to heading
                textnode_list.append(TextNode(current_text, current_type))
                current_text = ""
            level = len(heading_match.group(1))
            current_text = heading_match.group(2) + "\n"
            current_type = f"heading{level}"
            textnode_list.append(TextNode(current_text, current_type))
            current_text = ""
            current_type = "text"
        elif blockquote_match:
            if current_text and current_type != "blockquote":  # Handle text before a blockquote
                textnode_list.append(TextNode(current_text, current_type))
                current_text = ""
            current_text += blockquote_match.group(1) + "\n"
            current_type = "blockquote"
        else:
            if current_type == "blockquote":  # If we switch back to text from blockquote, append blockquote first
                textnode_list.append(TextNode(current_text, current_type))
                current_text = ""
                current_type = "text"
            current_text += line

    if current_text:  # Append any remaining text
        textnode_list.append(TextNode(current_text, current_type))

    return textnode_list

##__________Split Markdown List into Textnodes__________##

# def split_nodes_lists(text):


##__________Text into Textnodes Through Above Functions__________##

def text_to_textnodes(text):

    textnode_list = []




    return textnode_list
