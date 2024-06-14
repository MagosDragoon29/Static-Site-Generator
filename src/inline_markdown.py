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
            raise ValueError(f"Invalid MarkDown, formatted section not closed in node: {node}")

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
        if node.text_type != text_type_text:
            result.append(node)
            continue

        if not re.search(r"!\[(.*?)\]\((.*?)\)", node.text):
            result.append(node)
            continue

        images = extract_markdown_images(node.text)
        if not images:
            continue

        contents = re.split(r'(!\[[^\]]*\]\([^\)]*\))', node.text)

        for content in contents:
            if content == '':
                continue

            img_match = re.match(r'!\[(.*?)\]\((.*?)\)', content)
            if img_match:
                alt_text = img_match.group(1)
                url = img_match.group(2)
                result.append(TextNode(TEXT=alt_text, TEXT_TYPE= text_type_image, URL= url))
            else:
                result.append(TextNode(TEXT=content, TEXT_TYPE=text_type_text))

    return result


def split_nodes_link(old_nodes):
    result = []
    for node in old_nodes: 
        if node.text_type != text_type_text:
            result.append(node)
            continue

        if not re.search(r"\[(.*?)\]\((.*?)\)", node.text):
            result.append(node)
            continue


        contents = re.split(r'(\[[^\]]*\]\([^\)]*\))', node.text)
        for content in contents: 
            if content == '':
                continue

            link_match = re.match(r'\[(.*?)\]\((.*?)\)', content)
            if link_match:
                link_text = link_match.group(1)
                url = link_match.group(2)
                result.append(TextNode(TEXT=link_text, TEXT_TYPE=text_type_link, URL=url))
            else:
                result.append(TextNode(TEXT=content, TEXT_TYPE=text_type_text))
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
    bold = split_nodes_delimiter([start], "**", text_type_bold)
    italic = split_nodes_delimiter(bold, "*", text_type_italic)
    code = split_nodes_delimiter(italic,"`", text_type_code)
    images = split_nodes_image(code)
    links = split_nodes_link(images)
    return links

