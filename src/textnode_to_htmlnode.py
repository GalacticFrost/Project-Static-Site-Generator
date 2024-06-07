from leafnode import LeafNode

def textnode_to_htmlnode (text_node):

    valid_text_type_tags = {

        'text' : None,
        'bold' : 'b',
        'italic' : 'i',
        'code' : 'code',
        'link' : 'a',
        'image' : 'img',
        'heading1':'h1',
        'heading2':'h2',
        'heading3':'h3',
        'heading4':'h4',
        'heading5':'h5',
        'heading6':'h6',

    }
    
    if text_node.text_type.lower() not in valid_text_type_tags:
        raise Exception('Unsupport text type provided')

    if text_node.text_type.lower() == 'image':
        return LeafNode(tag=valid_text_type_tags[text_node.text_type.lower()],
                        props={'src': text_node.url, 'alt': text_node.text})

    if text_node.text_type.lower() == 'link':
        return LeafNode(tag=valid_text_type_tags[text_node.text_type.lower()], 
                    value=text_node.text, 
                    props={'href': text_node.url})
    
    return LeafNode(tag=valid_text_type_tags[text_node.text_type.lower()], 
                    value=text_node.text)
