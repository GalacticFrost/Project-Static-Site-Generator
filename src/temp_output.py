from textnode import *

sentence = '''This is **text** with an *italic* word and a `code block` and an 
    ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) 
    and a [link](https://boot.dev)'''

test_output = '''[
    TextNode("This is ", 'text'),
    TextNode("text", 'bold'),
    TextNode(" with an ", 'text'),
    TextNode("italic", 'italic'),
    TextNode(" word and a ", 'text'),
    TextNode("code block", 'code'),
    TextNode(" and an ", 'text'),
    TextNode("image", 'image', "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
    TextNode(" and a ", 'text'),
    TextNode("link", 'link', "https://boot.dev"),
]'''


delim_split = split_nodes_delimiter(sentence,['`', '*', '**'])

# print(f'A: {delim_split}\n')

image_split = split_nodes_images([delim_split[-1]])

# print(f'B: {image_split}\n')

link_split = split_nodes_links([image_split[-1]])

# print(f'C: {link_split}\n')

list = []

# print(f'{delim_split[:len(delim_split)-1]}\n')
# print(f'{image_split[:len(image_split)-1]}\n')

list.extend(delim_split[:len(delim_split)-1])
list.extend(image_split[:len(image_split)-1])
list.extend(link_split)

print(f'{list}\n')
print(test_output)
# print(list == test_output)