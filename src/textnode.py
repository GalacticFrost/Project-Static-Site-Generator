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

##__________Split Markdown Delimiters into Textnodes__________##

def split_nodes_delimiter(sentence, delimiters):
    valid_delim = {
        '`': 'code',
        '*': 'italic',
        '**': 'bold'
    }

    # Adjust the regex pattern to properly split the sentence
    pattern = r'(\\.|`|\*\*|\*)'
    parts = re.split(pattern, sentence)
    textnode_list = []
    current_text = ""
    current_type = "text"
    stack = []

    for part in parts:
        if part == '':  # Skip empty parts
            continue

        if part.startswith('\\'):  # Handle escaped characters
            current_text += part[1]
            continue

        if part in delimiters:  # Check for valid delimiters
            if stack and stack[-1] == part:
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
            current_text += part + " "  # Preserve white space

    # Handle any remaining unmatched delimiters as text
    while stack:
        current_text = stack.pop() + current_text
        current_type = "text"

    if current_text:
        textnode_list.append(TextNode(current_text.strip(), current_type))

    return textnode_list

##__________Extract Markdown Images - Helper Function__________##

def extract_markdown_images(text):

    pattern = r'!\[(.*?)\]\((.*?)(?:\s*".*?")?\)'

    if not text:
        return []
    return re.findall(pattern, text)

##__________Extract Markdown Links - Helper Function__________##

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
    
    heading_pattern = re.compile(r'^(#{1,6})\s(.*)$')
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
                textnode_list.append(TextNode(current_text.strip(), current_type))
                current_text = ""
            level = len(heading_match.group(1))
            current_text = heading_match.group(2) + "\n"
            current_type = f"heading{level}"
        elif blockquote_match:
            if current_text and current_type != "blockquote":  # Handle text before a blockquote
                textnode_list.append(TextNode(current_text.strip(), current_type))
                current_text = ""
            current_text += blockquote_match.group(1) + "\n"
            current_type = "blockquote"
        else:
            if current_type == "blockquote":  # If we switch back to text from blockquote, append blockquote first
                textnode_list.append(TextNode(current_text.strip(), current_type))
                current_text = ""
                current_type = "text"
            current_text += line

    if current_text:  # Append any remaining text
        textnode_list.append(TextNode(current_text.strip(), current_type))

    return textnode_list

##__________Split Markdown List into Textnodes__________##

# def split_nodes_lists(text):


##__________Flatten Nested Lists - Helper Function__________##

def flatten_list (list):

    flat_list = []

    for part in list:

        if not isinstance(part, type([])):
            flat_list.append(part)
        
        else:
            flat_list.extend(flatten_list(part))
    
    return flat_list

##__________Process Nested Segments - Helper Function__________##

def process_segment(segment):
    
    patterns = [
        r'(!\[.*?\]\(.*?\))',  # Images
        r'(\[.*?\]\(.*?\))',   # Links
        r'(\*\*.*?\*\*)',      # Bold
        r'(\*.*?\*)',          # Italics
        r'(`.*?`)'             # Code
    ]
    
    if not segment:
        return []

    temp_list = []

    for pattern in patterns:
        if re.search(pattern, segment):
            segs = re.split(pattern, segment)
            for seg in segs:
                if re.match(pattern, seg):
                    if pattern == patterns[0]:  # Image
                        temp_list.extend(split_nodes_images([TextNode(seg, 'text')]))
                    elif pattern == patterns[1]:  # Link
                        temp_list.extend(split_nodes_links([TextNode(seg, 'text')]))
                    elif pattern == patterns[2]:  # Bold
                        bold_text = seg[2:-2]  # Remove '**'
                        nested_segments = process_segment(bold_text)
                        for nested_segment in nested_segments:
                            if nested_segment.text_type == 'text':
                                temp_list.append(TextNode(nested_segment.text, 'bold'))
                            else:
                                temp_list.append(nested_segment)
                    elif pattern == patterns[3]:  # Italics
                        italic_text = seg[1:-1]  # Remove '*'
                        nested_segments = process_segment(italic_text)
                        for nested_segment in nested_segments:
                            if nested_segment.text_type == 'text':
                                temp_list.append(TextNode(nested_segment.text, 'italic'))
                            else:
                                temp_list.append(nested_segment)
                    elif pattern == patterns[4]:  # Code
                        code_text = seg[1:-1]  # Remove '`'
                        temp_list.append(TextNode(code_text, 'code'))
                elif seg:
                    temp_list.append(TextNode(seg, 'text'))  # Append text segment directly
            break
    else:
        if segment.startswith('>'):  # Blockquote
            temp_list.append(TextNode(segment[2:], 'blockquote'))
        else:
            temp_list.append(TextNode(segment, 'text'))  # Handle unformatted text

    return temp_list


##__________Text into Textnodes Through Above Functions__________##

def text_to_textnodes(text):

    pattern = r'(\[.*?\]\(.*?\)|!\[.*?\]\(.*?\)|\*\*.*?\*\*|\*.*?\*|`.*?`)'
    
    # Split the raw input into basic blocks, like headings and blockquotes
    heading_split_list = split_nodes_heading_and_blockquote(text)

    result_list = []

    for head_list_textnode in heading_split_list:
        head_text = head_list_textnode.text

        # First, split based on the main pattern to identify segments
        segments = re.split(pattern, head_text)
        temp_list = []

        for segment in segments:
            # Skip empty segments
            if not segment:
                continue

            # Handle nested segments using process_segment function
            if re.match(pattern, segment):
                temp_list.extend(process_segment(segment))
            else:
                temp_list.append(TextNode(segment, head_list_textnode.text_type))

        # Extend the result list with the processed segments
        result_list.extend(temp_list)
    
    # Flatten the list before returning it
    return flatten_list(result_list)

