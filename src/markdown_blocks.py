from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING  = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    
    blocks = [block.strip()for block in markdown.split("\n\n") if block.strip() != ""]
    stripped = []
    for block in blocks:
        new_block = ""
        for line in block.split("\n"):
            new_block += line.strip() + "\n"
        stripped.append(new_block.strip())
            
    return stripped

def block_to_block_type(block):
    lines = block.split("\n")
    quote = True
    unordered = True
    ordered = True
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    elif block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE
    for i in range(len(lines)):
        line = lines[i]
        if not line.startswith(">"):
            quote = False
        if not line.startswith("- "):
            unordered = False
        if not line.startswith(f"{i+1}. "):
            ordered = False
    if quote == True:
        return BlockType.QUOTE
    elif unordered == True:
        return BlockType.UNORDERED_LIST
    elif ordered == True:
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH

