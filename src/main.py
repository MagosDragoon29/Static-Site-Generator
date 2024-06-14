import os
import shutil
from textnode import TextNode
from markdown_blocks import markdown_to_html_node
from htmlnode import (HTMLNode, LeafNode, ParentNode)
#page intentionally left blank

#print("hello world")

root_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(root_dir)
static_dir = os.path.join(parent_dir, 'static')
public_dir = os.path.join(parent_dir, 'public')

if not os.path.exists(static_dir):
    print(f"Error: the directory {static_dir} does not exist.")

def main():
    #test_case = TextNode("This is a TextNode", "bold", "https://www.boot.dev/")
    #print(test_case)
    copy_files(static_dir)
    generate_page(os.path.join(parent_dir,'content/index.md'), os.path.join(parent_dir,'template.html'), public_dir)
    pass

def copy_files(source_dir, sub_dir = None):
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)
    os.makedirs(public_dir)
    all_items = os.listdir(source_dir)
    destination_dir = public_dir
    if sub_dir != None:
        destination_dir = os.path.join(public_dir, sub_dir)
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)
    for item in all_items:
        item_path = os.path.join(source_dir, item)
        if os.path.isfile(item_path):
            shutil.copy(item_path, destination_dir)
        elif os.path.isdir(item_path):
            new_sub_dir = os.path.join(sub_dir or '', item)
            copy_files(item_path, new_sub_dir)

def extract_title(markdown):
    contents = markdown.split("\n")
    for line in contents:
        line = line.strip()
        if line and line.startswith("# "):
            return line.lstrip("# ").strip()
    raise Exception ("Document requires a title as Header 1")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}.")
    with open(from_path, 'r', encoding='utf-8') as file:
        contents = file.read()
    with open(template_path, 'r', encoding='utf-8') as temp:
        template = temp.read()
    title = extract_title(contents)
    base_name = os.path.basename(from_path)
    name, ext = os.path.splitext(base_name)
    html_contents = ""
    if ext.lower() == '.md':
        dest_file_name = f"{name}.html"
    else:
        raise ValueError("Source file does not have a .md extension")
    full_dest_path = os.path.join(dest_path, dest_file_name)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    nodes = markdown_to_html_node(contents)
    html_contents += nodes.to_html()
    result = template.replace("{{ Title }}", title).replace("{{ Content }}", html_contents)
    with open(full_dest_path, 'w', encoding='utf-8') as html_file:
        html_file.write(result)
# page intentionally left blank    
main()