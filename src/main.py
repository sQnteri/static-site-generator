import shutil
import os
from textnode import TextType, TextNode
from copy_contents import copy_contents

def main():

    if os.path.exists("public"):
        shutil.rmtree("public")
    copy_contents("static", "public")

if __name__ == "__main__":
    main()
