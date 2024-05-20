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

def split_nodes_image(old_nodes):
    result = []
    for node in old_nodes:
        if not re.search(r"!\[(.*?)\]\((.*?)\)", node.text):
            result.append(node)
        if node.text_type != text_type_text:
            result.append(node)
        images = extract_markdown_images(node.text)
        contents = re.split(r'!|\)', node.text)
        for item in contents:
            if item == '':
                continue
            if '[' in item:
                result.append(TextNode(TEXT=images[0][0], TEXT_TYPE=text_type_image, URL=images[0][1]))
                images.pop(0)
                continue
            if '[' not in item:
                result.append(TextNode(TEXT=item, TEXT_TYPE=text_type_text))
                continue
    return result


def split_nodes_link(old_nodes):
    result = []
    for node in old_nodes: 
        if not re.search(r"\[(.*?)\]\((.*?)\)", node.text):
            result.append(node)
        if node.text_type != text_type_text:
            result.append(node)
        links = extract_markdown_links(node.text)
        contents = re.split(r'\[|\)', node.text)
        for item in contents: 
            if item == '':
                continue
            if "]" in item:
                result.append(TextNode(TEXT=links[0][0],TEXT_TYPE=text_type_link, URL=links[0][1]))
                links.pop(0)
                continue
            if "]" not in item:
                result.append(TextNode(TEXT=item, TEXT_TYPE=text_type_text))
                continue
    return result

def extract_markdown_images(TEXT):
    results = []
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", TEXT)
    for match in matches: 
        results.append(match)
    return results

def extract_markdown_links(TEXT):
    results = []
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", TEXT)
    for match in matches: 
        results.append(match)
    return results

def text_to_textnodes(text):
    start = TextNode(text, text_type_text)
    result = split_nodes_link(split_nodes_image(split_nodes_delimiter(split_nodes_delimiter(split_nodes_delimiter(start, "**", text_type_bold), "*", text_type_italic), "`", text_type_code)))
    return result