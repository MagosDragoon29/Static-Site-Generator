# reserved
# for
# imports

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered = "unordered list"
block_type_ordered = "ordered list"

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
    
