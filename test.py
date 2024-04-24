# # 导入spaCy
# import spacy
#
# # 加载预训练模型
# nlp = spacy.load("en_core_web_sm")
#
# # 定义要识别的实体类别
# entity_categories = ["PRODUCT", "PROFESSION", "EVENT"]
#
# # 对文本进行标记
# text = "- Python as a versatile programming language"
# doc = nlp(text)
#
# # 提取和分类命名实体
# entities = []
# for ent in doc.ents:
#     if ent.label_ in entity_categories:
#         entities.append((ent.text, ent.label_))
#
# # 打印命名实体及其类别
# for entity in entities:
#     print(entity)
#
# from transformers import pipeline
#
# # 加载实体识别模型
# nlp = pipeline("ner", model="dslim/bert-base-NER")
#
# # 输入文本
# text = """
# - The tutorial covers basic Python concepts like variables, strings, booleans, and type conversion."""
#
# # 进行实体识别
# entities = nlp(text)
#
# # 打印识别到的实体
# for entity in entities:
#     print(f"Entity: {entity['word']}, Label: {entity['entity']}, Score: {entity['score']}")
#
# """
# - The video introduces Python as a versatile programming language suitable for various tasks such as data science, machine learning, and web development.
# - It guides on how to download and install Python, set up a code editor like PyCharm, and create a new Python project.
# - The tutorial covers basic Python concepts like variables, strings, booleans, and type conversion.
# - It explains the usage of input function to receive user input, arithmetic operators for mathematical operations, and comparison operators for comparisons.
# - The video demonstrates the use of logical operators for building complex conditions and if statements for decision-making in Python programs.
# - It showcases the usage of lists and tuples in Python for storing sequences of objects, iterating over them, and accessing individual elements.
# - The tutorial also introduces the range function for generating sequences of numbers and highlights the immutability of tuples compared to lists in Python.
# """



#
# # 假设我们有两个列表
# list1 = ["Python programming basics", "Variables, data types, and type conversion",
#          "Decision-making with if statements", "Working with strings and lists",
#          "Iteration with for loops and range function", "Understanding tuples"]
# list2 = ["Python basics and syntax", "Variables and data types", "Control structures (if-else statements, loops)",
#          "Functions and modular code", "Object-oriented programming (classes, objects, inheritance)",
#          "File handling", "Exception handling"]
#
# a = {"Python programming basics": ["xxxx", "yyyy"], }

import json

# 假设你的JSON字符串存储在名为'video_info.txt'的文件中
file_path = 'Data/Intermediary/search_video_match.txt'

d = {'kqtD5dpn9C8': 'Python for Beginners - Learn Python in 1 Hour', 'Gm72cIo9_58': 'Perceiving Python Programming Paradigms - Jigyasa Grover'}

json_data = json.dumps(d)

# # 将JSON字符串写入到文本文件中
# with open(file_path, 'w') as file:
#     file.write(json_data)

# 打开文件并读取JSON字符串
with open(file_path, 'r') as file:
    json_string = file.read()

# 解析JSON字符串为Python字典
data = json.loads(json_string)

# 打印读取的数据
print(data)