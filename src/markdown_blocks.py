#
#
#

def markdown_to_blocks(markdown):
    blocks = []
    contents = markdown.split("\n\n")
    for content in contents: 
        if content == "":
            continue
        else:
            blocks.append(content.strip())
    return blocks