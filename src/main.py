import os
import shutil
from functions import copy_directory_recursive, generate_page

dir_path_static = "./static"
dir_path_public = "./public"
path_template = "./template.html"
path_index = "./content/index.md"
path_dest = "./public/index.html"

def main():
    print(f"Delete directory {dir_path_public}")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)
    
    copy_directory_recursive(dir_path_static, dir_path_public)

    generate_page(path_index, path_template, path_dest)




main()