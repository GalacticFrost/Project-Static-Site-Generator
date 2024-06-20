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

    # If the sentence is empty, return an empty list
    if not sentence:
        return []

    # Define valid markdown delimiters
    valid_delimiters = {"`", "*", "**", "_"}

    # Sort delimiters by length in descending order to avoid partial matches
    delimiters = sorted(delimiters, key=len, reverse=True)
    
    # Check if each provided delimiter is valid
    for delimiter in delimiters:
        if delimiter not in valid_delimiters:
            raise Exception(f"Delimiter '{delimiter}' is not a valid markdown syntax")

    # Process escaped delimiters first
    escaped_delimiters = [re.escape(d) for d in delimiters]
    escape_pattern = re.compile(r'\\(' + '|'.join(escaped_delimiters) + ')')

    def replace_escaped(match):
        return match.group(0)  # Keep the escape sequence intact for now

    escaped_sentence = escape_pattern.sub(replace_escaped, sentence)

    # Escape delimiters for regex and create a regex pattern to match any of the delimiters
    pattern = '|'.join([f'({re.escape(d)}.*?{re.escape(d)})' for d in delimiters])

    # Initialize variables
    nodes = []
    last_pos = 0
    pos = 0

    # Helper function to add a text node
    def add_text_node(start, end, node_type):
        if start < end:
            text = sentence[start:end]
            nodes.append(TextNode(text, node_type))

    # Process the sentence to split it into nodes based on the delimiters
    while pos < len(escaped_sentence):
        match = re.search(pattern, escaped_sentence[pos:])
        if match:
            start, end = match.span()
            start += pos
            end += pos
            delimiter = next((d for d in delimiters if escaped_sentence[start:start+len(d)] == d), None)
            if delimiter:
                add_text_node(last_pos, start, "text")  # Add preceding text as a text node
                inner_text = sentence[start+len(delimiter):end-len(delimiter)]
                # Determine the node type based on the delimiter
                node_type = {
                    "`": "code",
                    "*": "italic" if delimiter in ("*", "_") else "bold",
                    "**": "bold",
                    "_": "italic"
                }.get(delimiter, "unknown")
                nodes.append(TextNode(inner_text, node_type))  # Add the inner text as a formatted node
                last_pos = end
            pos = end
        else:
            break

    # Add any remaining text after the last match as a text node
    if last_pos < len(sentence):
        add_text_node(last_pos, len(sentence), "text")

    # Re-insert escaped delimiters back into the nodes
    new_nodes = []
    for node in nodes:
        parts = escape_pattern.split(node.text)
        for part in parts:
            if escape_pattern.match(part):
                new_nodes.append(TextNode(part, "text"))
            else:
                new_nodes.append(TextNode(part, node.text_type))
    
    return new_nodes

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
    # Initialize an empty list to hold the processed text and image nodes
    textnode_list = []

    # Iterate over each node in the old_nodes list
    for node in old_nodes:
        # Check if the current node is of type "text"
        if node.text_type == "text":
            # Extract all markdown images from the text of the current node
            images_extracted = extract_markdown_images(node.text)

            # If no images are found in the text, add the entire node to the textnode_list
            if not images_extracted:
                textnode_list.append(node)
                continue

            # Initialize split_text with the entire text of the current node
            split_text = node.text

            # Iterate over each extracted image (tuple of alt text and URL)
            for image_alt, image_url in images_extracted:
                # Split the text at the first occurrence of the markdown image
                parts = split_text.split(f"![{image_alt}]({image_url})", 1)
                
                # If the text before the image is not empty, create a new text node and add it to the list
                if parts[0]:
                    textnode_list.append(TextNode(parts[0], "text"))
                
                # Create a new image node with the alt text and URL, and add it to the list
                textnode_list.append(TextNode(image_alt, "image", image_url))
                
                # Update split_text to the remaining part after the first image
                split_text = parts[1] if len(parts) > 1 else ""
            
            # If there is any remaining text after the last image, create a new text node and add it to the list
            if split_text:
                textnode_list.append(TextNode(split_text, "text"))
        else:
            # If the current node is not of type "text", add it directly to the textnode_list
            textnode_list.append(node)
    
    # Return the list of processed text and image nodes
    return textnode_list

##__________Split Markdown Link into Textnodes__________##

def split_nodes_links(old_nodes):
    # Initialize an empty list to hold the processed text and link nodes
    textnode_list = []

    # Iterate over each node in the old_nodes list
    for node in old_nodes:
        # Check if the current node is of type "text"
        if node.text_type == "text":
            # Extract all markdown links from the text of the current node
            links_extracted = extract_markdown_links(node.text)

            # If no links are found in the text, add the entire node to the textnode_list
            if not links_extracted:
                textnode_list.append(node)
                continue

            # Initialize split_text with the entire text of the current node
            split_text = node.text

            # Iterate over each extracted link (tuple of link text and URL)
            for link_text, link_url in links_extracted:
                # Split the text at the first occurrence of the markdown link
                parts = split_text.split(f"[{link_text}]({link_url})", 1)
                
                # If the text before the link is not empty, create a new text node and add it to the list
                if parts[0]:
                    textnode_list.append(TextNode(parts[0], "text"))
                
                # Create a new link node with the link text and URL, and add it to the list
                textnode_list.append(TextNode(link_text, "link", link_url))
                
                # Update split_text to the remaining part after the first link
                split_text = parts[1] if len(parts) > 1 else ""
            
            # If there is any remaining text after the last link, create a new text node and add it to the list
            if split_text:
                textnode_list.append(TextNode(split_text, "text"))
        else:
            # If the current node is not of type "text", add it directly to the textnode_list
            textnode_list.append(node)
    
    # Return the list of processed text and link nodes
    return textnode_list

##__________Split Markdown Heading into Textnodes__________##

def split_nodes_heading(text):

    # Regular expression pattern to match markdown-style headings (e.g., ## Heading)
    heading_pattern = re.compile(r'^(#{1,6})\s(.*)$')

    # Split the input text into lines while keeping line endings intact
    lines = text.splitlines(keepends=True)
    
    # Initialize an empty list to hold the processed text and heading nodes
    textnode_list = []
    
    # Initialize variables to accumulate text and determine its type
    current_text = ""
    current_type = "text"

    # Iterate over each line in the lines list
    for line in lines:
        # Attempt to match the current line against the heading pattern
        heading_match = heading_pattern.match(line)

        if heading_match:
            # If the line matches the heading pattern
            if current_text:
                # Append the accumulated text as a text node if there is any
                textnode_list.append(TextNode(current_text, current_type))
            
            # Determine the level of the heading (number of '#' characters)
            level = len(heading_match.group(1))
            
            # Add the matched heading text as a heading node with appropriate level
            textnode_list.append(TextNode(heading_match.group(2), f"heading{level}"))
            
            # Reset current_text and current_type for new accumulation
            current_text = ""
            current_type = "text"
        else:
            # If the line does not match the heading pattern, accumulate it into current_text
            current_text += line

    # Append any remaining accumulated text as a text node at the end
    if current_text:
        textnode_list.append(TextNode(current_text, current_type))

    # Return the list of processed text and heading nodes
    return textnode_list

##__________Split Markdown Blockqoute into Textnodes__________##

def split_nodes_blockquote(text_nodes):

    # Regular expression pattern to match blockquotes (lines starting with "> ")
    blockquote_pattern = re.compile(r'^> (.*)$')
    
    # List to hold the resulting TextNode objects
    textnode_list = []
    
    # Variables to accumulate text and track the current type ("text" or "quote")
    current_text = ""
    current_type = "text"

    # Iterate through each TextNode object in text_nodes
    for node in text_nodes:
        # Split the text of the current node into lines
        lines = node.text.splitlines()
        
        # Iterate through each line of the current node's text
        for line in lines:
            # Check if the line matches the blockquote pattern
            blockquote_match = blockquote_pattern.match(line)
            
            if blockquote_match:
                # If the line matches the blockquote pattern
                if current_text:
                    # If there's accumulated text, create a TextNode for it
                    textnode_list.append(TextNode(current_text, current_type))
                    current_text = ""  # Reset accumulated text
                # Create a new TextNode for the blockquote line
                textnode_list.append(TextNode(blockquote_match.group(1), "quote"))
                current_type = "quote"  # Update current type to "quote"
            else:
                # If the line does not match the blockquote pattern (normal text)
                if current_text:
                    current_text += "\n" + line  # Accumulate with newline
                else:
                    current_text = line  # Start accumulating text
                current_type = "text"  # Update current type to "text"

    # After processing all lines, append any remaining accumulated text
    if current_text:
        textnode_list.append(TextNode(current_text, current_type))

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






def text_to_textnodes(text):

    # Check if input is already a list of TextNode objects
    if isinstance(text, list) and all(isinstance(item, TextNode) for item in text):
        return text

    # Ensure text is a string
    if not isinstance(text, str):
        raise TypeError("Input must be a string or a list of TextNode objects")

    # Split text into initial nodes based on markdown delimiters
    initial_nodes = split_nodes_delimiter(text, ["`", "*", "**"])

    # Initialize an empty list to collect processed nodes
    nodes = []

    # Process each initial node one by one
    for node in initial_nodes:
        # Split nodes further based on images
        nodes_images = split_nodes_images([node])
        
        # Process each image node
        for node_images in nodes_images:
            # Split nodes further based on links
            nodes_links = split_nodes_links([node_images])
            
            # Process each link node
            for node_links in nodes_links:
                # Handle headings and blockquotes for text nodes
                if node_links.text_type == "text":
                    nodes_headings = split_nodes_heading(node_links.text)
                    for node_headings in nodes_headings:
                        nodes_blockquote = split_nodes_blockquote([node_headings])
                        nodes.extend(nodes_blockquote)
                else:
                    nodes.extend([node_links])

    # Flatten the list of nodes
    nodes = flatten_list(nodes)

    return nodes




##__________Split Markdown into Block__________##

def markdown_to_blocks(markdown_document):

    raw_text_blocks = markdown_document.split('\n')
    final_text_blocks = []
    temp_block = []

    for line in raw_text_blocks:
        new_line =  line.strip()
        if new_line:  # Non-empty line (with whitespace stripped out)
            temp_block.append(new_line)
        else:
            if temp_block:  # If there's anything in temp_block
                final_text_blocks.append("\n".join(temp_block).strip())
                temp_block = []
    
    # Add any remaining temp_block as a last block if it exists
    if temp_block:
        final_text_blocks.append("\n".join(temp_block).strip())
    
    return final_text_blocks

##__________Identify the Block Type__________##

def block_to_block_type(block):

    heading_pattern = re.compile(r'^(#{1,6})\s(.*)$', re.MULTILINE)
    blockquote_pattern = re.compile(r'^> (.*)$', re.MULTILINE)
    code_block_pattern = re.compile(r'^```[\s\S]*?```$', re.MULTILINE)
    unordered_list_pattern = re.compile(r'^( *[\*\-] .+)$', re.MULTILINE)
    ordered_list_pattern = re.compile(r'^( *\d+(\.\d+)*\. .+)$', re.MULTILINE)

    if not isinstance(block, str):
        raise TypeError("Input must be a string")

    if heading_pattern.match(block):
        return 'heading'
    if blockquote_pattern.match(block):
        return 'quote'
    if code_block_pattern.match(block):
        return 'code'
    if unordered_list_pattern.match(block):
        return 'ulist'
    if ordered_list_pattern.match(block):
        return 'olist'
    
    return 'paragraph'