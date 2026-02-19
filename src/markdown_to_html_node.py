from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType
from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import LeafNode, ParentNode
from inline_markdown import text_to_textnodes

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


