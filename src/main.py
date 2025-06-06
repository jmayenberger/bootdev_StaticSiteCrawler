import os
import shutil
from functions import copy_directory_recursive, generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./public"
template_path = "./template.html"
dir_path_content = "./content"

def main():
    print(f"Delete directory {dir_path_public}")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)
    
    copy_directory_recursive(dir_path_static, dir_path_public)

    generate_pages_recursive(dir_path_content, template_path, dir_path_public)




main()