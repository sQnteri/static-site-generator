import os
from pathlib import Path
from src.markdown_blocks import markdown_to_html_node

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith('# '):
            return stripped[2:].strip()
    raise Exception("No header found")

def generate_page(from_path, template_path, dest_path):
    
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as f:
        markdown = f.read()
    
    with open(template_path, "r") as f:
        template = f.read()

    html_node = markdown_to_html_node(markdown)
    title = extract_title(markdown)
    content = html_node.to_html()

    page = template.replace("{{ Title }}", title).replace("{{ Content }}", content)  

    dest_dir = os.path.dirname(dest_path)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)
    
    with open(dest_path, "w") as f:
        f.write(page)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for entry in os.listdir(dir_path_content):
        entry_path = os.path.join(dir_path_content, entry)
        if os.path.isdir(entry_path):
            generate_pages_recursive(entry_path, template_path, os.path.join(dest_dir_path, entry))
        elif entry.endswith(".md"):
            dest_path = os.path.join(dest_dir_path, Path(entry).with_suffix(".html").name)
            generate_page(entry_path, template_path, dest_path)

    
