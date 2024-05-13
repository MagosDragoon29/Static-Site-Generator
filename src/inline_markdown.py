import copy
import re
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
   result = []
   for node in old_nodes:
        new_nodes = []
        node_text = copy.copy(node.text).split(delimiter)

        if node.text_type != text_type_text: 
            result.append(node)
            continue
        
        if len(node_text) % 2 == 0:
            raise ValueError("Invalid MarkDown, formatted section not closed!")

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
   return result

def EXTRACT_MARKDOWN_IMAGES(TEXT):
    results = []
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", TEXT)
    alt_text = []
    links = []
    for match in matches[::2]:
        alt_text.append(match)
    for match in matches[1::2]:
        links.append(match)
    for i in range(0, len(links)):
        results.append((alt_text[i], links[i]))
    return results

def EXTRACT_MARKDOWN_LINKS(TEXT):
    results = []
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", TEXT)
    alt_text = []
    links = []
    for match in matches[::2]:
        alt_text.append(match)
    for match in matches[1::2]:
        links.append(match)
    for i in range(0, len(links)):
        results.append((alt_text[i], links[i]))
    return results