from enum import Enum
from src.textnode import TextNode, TextType, text_node_to_html_node
from src.htmlnode import LeafNode, ParentNode
from src.inline_markdown import text_to_textnodes

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

def markdown_to_html_node(markdown):
    nodes = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.HEADING:
                head = block.split(" ")[0]
                level = len(head)
                nodes.append(ParentNode(f"h{level}", text_to_children(block[level+1:])))
            case BlockType.CODE:
                nodes.append(ParentNode("pre", [LeafNode("code", block[4:-3])]))
            case BlockType.QUOTE:
                lines = block.split("\n")
                quote_text = " ".join(line[2:] for line in lines)
                nodes.append(ParentNode("blockquote", text_to_children(quote_text)))
            case BlockType.UNORDERED_LIST:
                nodes.append(ParentNode("ul", [ParentNode("li", text_to_children(line[2:])) for line in block.split("\n")]))
            case BlockType.ORDERED_LIST:
                nodes.append(ParentNode("ol", [ParentNode("li", text_to_children(line.split(". ", 1)[1])) for line in block.split("\n")]))
            case BlockType.PARAGRAPH:
                nodes.append(ParentNode("p", text_to_children(block.replace("\n", " "))))
            case _:
                raise Exception("Not a supported block type")
    
    return ParentNode("div", nodes)
                
            

def text_to_children(text):
    nodes = text_to_textnodes(text)
    html_nodes = [text_node_to_html_node(node) for node in nodes]
    return html_nodes

