import os
import shutil
from textnode import TextNode
#page intentionally left blank

#print("hello world")

root_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(root_dir, 'static')
public_dir = os.path.join(root_dir, 'public')

def main():
    #test_case = TextNode("This is a TextNode", "bold", "https://www.boot.dev/")
    #print(test_case)
    pass

def copy_files(source_dir, sub_dir = None):
    public_list = os.listdir(public_dir)
    if not public_list:
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


# page intentionally left blank    
main()