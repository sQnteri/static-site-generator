import shutil
import os
from src.textnode import TextType, TextNode
from src.copy_contents import copy_contents
from src.gencontent import generate_pages_recursive

def main():
    
    #remove public if it exists
    if os.path.exists("public"):
        shutil.rmtree("public")
    #copy contents of static to public
    copy_contents("static", "public")
    #generate page using the markdown file and template
    generate_pages_recursive("content", "template.html", "public")


if __name__ == "__main__":
    main()
