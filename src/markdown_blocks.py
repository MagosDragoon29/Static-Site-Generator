from htmlnode import (HTMLNode, LeafNode, ParentNode)
from textnode import (TextNode, text_node_to_html_node)
from inline_markdown import (text_to_textnodes)

#block types
block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered = "unordered list"
block_type_ordered = "ordered list"
#tags
tag_div ='div'
tag_quote = 'blockquote'
tag_unordered = 'ul'
tag_ordered = 'ol'
tag_list_item = 'li'
tag_code = 'code'
tag_preformatted = 'pre'
tag_heading = 'h'
tag_paragraph = 'p'

def markdown_to_blocks(markdown):
    blocks = []
    contents = markdown.split("\n\n")
    for content in contents: 
        if content == "":
            continue
        else:
            blocks.append(content.strip())
    return blocks

def block_to_block_type(block):
    header = ("#","##","###","####","#####","######")
    code = '```'
    quote = ">"
    unordered = ("*","-")
    def test_unordered(item):
        contents = item.split("\n")
        for line in contents:
            line = line.strip()
            if not line:
                continue
            if not line.startswith(unordered):
                return False
        return True
    def test_ordered(item):
        contents = item.split("\n")
        counter = 1
        for line in contents:
            if line.startswith(f"{counter}. "):
                counter += 1
            else:
                return False
        return True
    if block.startswith(header):
        return block_type_heading
    # code
    elif block.startswith(code) and block.endswith(code):
        return block_type_code
    # quote
    elif block.startswith(quote):
        return block_type_quote
    # unordered list
    elif test_unordered(block):
        return block_type_unordered
    # ordered list
    elif test_ordered(block):
        return block_type_ordered
    # paragraph
    else:
        return block_type_paragraph
    
    
def markdown_to_html_node(markdown):
    finale = ParentNode(tag=f"{tag_div}", children=[], props=None)
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == block_type_heading:
            level = block.count("#")
            content = block.lstrip("#").strip()
            content_node = text_to_textnodes(content)
            if len(content_node) == 1:
                finale.children.append(LeafNode(tag = f"{tag_heading}{level}",value = content))
            else:
                content_node = [text_node_to_html_node(item) for item in content_node]
                finale.children.append(ParentNode(tag = f"{tag_heading}{level}", children = content_node))
        elif block_type == block_type_paragraph:
            content = " ".join(block.split("\n")).strip()
            content_node = text_to_textnodes(content)
            if len(content_node) == 1:
                finale.children.append(LeafNode(tag = f"{tag_paragraph}", value = content))
            else:
                content_node = [text_node_to_html_node(item) for item in content_node]
                finale.children.append(ParentNode(tag = f"{tag_paragraph}", children = content_node))
        elif block_type == block_type_code:
            content = block.strip('`').strip()
            finale.children.append(ParentNode(tag = f"{tag_preformatted}", children = [LeafNode(tag = f"{tag_code}", value = content)]))
        elif block_type == block_type_quote:
            content = " ".join([line.lstrip('> ').strip() for line in block.split("\n")])
            #quote_content = markdown_to_html_node(content)
            finale.children.append(LeafNode(tag = f"{tag_quote}",value = content))
        elif block_type == block_type_unordered:
            items = block.split("\n")
            list_items = []
            for item in items:
                item_content = item.lstrip("*- ")
                item_nodes = text_to_textnodes(item_content)
                line = []
                for thing in item_nodes:
                    thing = text_node_to_html_node(thing)
                    if thing.tag == None:
                        line.append(thing.value.strip())
                    else:
                        line.append(thing.to_html())
                html_item = " ".join(line)
                list_items.append(LeafNode(tag = f"{tag_list_item}", value = html_item))
            finale.children.append(ParentNode(tag=f"{tag_unordered}", children=list_items))
        elif block_type == block_type_ordered:
            items = block.split("\n")
            list_items = []
            for item in items:
                item_content = item.lstrip("0123456789. ").strip()
                item_nodes = text_to_textnodes(item_content)
                line = []
                for thing in item_nodes:
                    thing = text_node_to_html_node(thing)
                    if thing.tag == None:
                        line.append(thing.value.strip())
                    else:
                        line.append(thing.to_html())
                html_item = " ".join(line)
                list_items.append(LeafNode(tag = f"{tag_list_item}", value = html_item))
            finale.children.append(ParentNode(tag=f"{tag_ordered}", children = list_items))
        else:
            raise ValueError("Invalid Markldown format: Please ensure the Markdown text is correctly formatted.")
    return finale