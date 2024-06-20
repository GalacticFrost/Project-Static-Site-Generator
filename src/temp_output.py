from textnode import *

text = '''# This is a heading
This is a paragraph of text. It has some **bold** and *italic* words inside of it.
* This is a list item
* This is another list item'''

text1 =  '''This is a code block:
```

code code
code code

```
This is a comment'''

text_split = text.split('\n')
text1_split = text1.split(' ')

print(text.replace('\n', '|\n'))
print('\n')
print(text_split)
print('\n')
print(text1.replace('\n', '|\n'))
print(text1_split)

combined = ['This is a code block:', '```code code code code```', 'This is a comment']
