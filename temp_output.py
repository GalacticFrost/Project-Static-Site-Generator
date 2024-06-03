import re

image = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)"
link = "[GitHub](https://github.com \"GitHub Homepage\")"

pattern = r'!\[.*?\]\(.*?\)'


split_image = re.split(pattern, image)

print(split_image)
print(split_image[2])
print(len(split_image[2]))