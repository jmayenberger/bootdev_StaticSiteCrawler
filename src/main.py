import os
import shutil
import sys
from functions import copy_directory_recursive, generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./docs"
template_path = "./template.html"
dir_path_content = "./content"

def main():
    if len(sys.argv) < 2:
        basepath = "/"
    else:
        basepath = sys.argv[1]
    print(f"Delete directory {dir_path_public}")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)
    
    copy_directory_recursive(dir_path_static, dir_path_public)

    generate_pages_recursive(dir_path_content, template_path, dir_path_public, basepath)




main()