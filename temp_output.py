import re

text = "![alt text](https://example.com/image.jpg \"Image Title\")"
text1 = "[GitHub](https://github.com \"GitHub Homepage\")"

match =  re.findall(r"!\[(.*)\]\(([^\"\s]*)\)", text)
match1 = re.findall(r"\[(.*)\]\(([^\"\s]*)\)", text1)

print (f'{match}\n')
print(match1)
