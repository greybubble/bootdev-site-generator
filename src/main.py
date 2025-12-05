from textnode import TextNode, TextType
from leafnode import LeafNode
from parentnode import ParentNode
from enum import Enum
from utilities import *
import os
import shutil
import sys

def main():
    basepath = '/'
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    copy_static_to_public("static", "docs")
    c_dir = "content"
    t_path = "template.html"
    d_dir = "docs"
    generate_pages_recursive(c_dir, t_path, d_dir, basepath)



def rm_folder(path):
    contents = os.listdir(path)
    if not contents:
        print(f"removing empty folder: {path}")
        os.rmdir(path)
        return 
    
    for item in contents:
        item_path = f"{path}/{item}"
        if os.path.isfile(item_path):
            print(f"removing file: {item_path}")
            os.remove(item_path)
        elif os.path.isdir(item_path):
            rm_folder(item_path)
        else:
            print()
            raise Exception(f"Exceptional Confusion: This is not a file or folder?: {item_path}")
    print(f"removing folder: {path}")
    os.rmdir(path)
        
def copy_folder_to_dest(o_path, d_path):
    if not os.path.exists(o_path):
        raise Exception(f"Error: Origin folder {o_path} doesn't exist to copy files from!")

    if not os.path.exists(d_path):
        print(f"Creating destination folder: {d_path}")
        os.mkdir(d_path)

    contents = os.listdir(o_path)

    if not contents:
        print(f"Folder at path {o_path} is empty.")
        return 
    
    for item in contents:
        item_path = f"{o_path}/{item}"
        dest_path = f"{d_path}/{item}"
        if os.path.isfile(item_path):
            print(f"copying {item_path} to {dest_path}")
            shutil.copy(item_path, dest_path)
        elif os.path.isdir(item_path):
            copy_folder_to_dest(item_path, dest_path)
        else:
            raise Exception(f"Error: not sure what {item_path} is, but it ain't a file or folder!") 

def copy_static_to_public(source, dest):
    
    print(f"Copying files from {source} to {dest}")
    if os.path.exists(dest):
        rm_folder(dest)

    copy_folder_to_dest(source, dest)
    
def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    if not os.path.exists(from_path):
        raise Exception("Error: web page source file is missing or path is incorrect")
    if not os.path.exists(template_path):
        raise Exception("Error: Template file is missing or path is incorrect")
    
    markdown = ''
    template = ''
    
    with open(from_path) as f:
        markdown = f.read()

    with open(template_path) as f:
        template = f.read()

    title = extract_title(markdown) 
    h_node = markdown_to_html_node(markdown)
    page = template.replace("{{ Title }}", title).replace("{{ Content }}", h_node.to_html())
    page = page.replace('href="/', f'href="{basepath}')
    page = page.replace('src="/', f'src="{basepath}')
    with open(dest_path, "w") as f:
        f.write(page)
    
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    

    print(f"Generating pages from directory {dir_path_content} to {dest_dir_path} using {template_path}")
    if not os.path.isdir(dir_path_content):
        raise Exception(f"Error: Content folder not found at {dir_path_content}")
    
    if not os.path.isfile(template_path):
        raise Exception(f"Error: Template not found at {template_path}")
    
    if not os.path.isdir(dest_dir_path):
        os.mkdir(dest_dir_path)

    contents = os.listdir(dir_path_content)

    if not contents:
        print(f"Caution: Content folder is empty at {dir_path_content}")

    for item in contents:
        c_path = f"{dir_path_content}/{item}"
        d_path = f"{dest_dir_path}/{item}"

        if os.path.isdir(c_path):
            generate_pages_recursive(c_path, template_path, d_path, basepath)
        elif item.endswith('.md'):
            generate_page(c_path, template_path, d_path.replace('.md', '.html'), basepath)
        else:
            shutil.copy(c_path, d_path)
    




if __name__ == "__main__":
    main()
