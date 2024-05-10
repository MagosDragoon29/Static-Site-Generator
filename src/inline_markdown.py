import copy
from textnode import (
    TextNode, 
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_link,
    text_type_image
)


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    # going to use a lot of if lines like above, each if line will need an "if 'delimiter' in X, then call the delimiter with
    # that specific delimiter and text_type variable. the result needs to return a list of TextNodes. the .extend() method will be good here. 
   result = []
   for node in old_nodes:
        new_nodes = []
        node_text = copy.copy(node.text).split(delimiter)
        if node.text.startswith(delimiter):
            new_nodes.append(TextNode(node_text[0], node.text_type))
        for i in range (0, len(node_text)):
            if i % 2 == 0:
                new_nodes.append(TextNode(node_text[i], node.text_type))
            else:
                new_nodes.append(TextNode(node_text[i], text_type))
        if node.text.endswith(delimiter):
            new_nodes.pop()
        result.extend(new_nodes)
   print(result)
   return result