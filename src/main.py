import shutil
import os
import sys
from textnode import TextType, TextNode
from copy_contents import copy_contents
from gencontent import generate_pages_recursive

def main():
    
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    #remove public if it exists
    if os.path.exists("docs"):
        shutil.rmtree("docs")
    #copy contents of static to public
    copy_contents("static", "docs")
    #generate page using the markdown file and template
    generate_pages_recursive("content", "template.html", "docs", basepath)


if __name__ == "__main__":
    main()
