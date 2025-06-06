import re
import os
import shutil
from my_types import TextType, BlockType
from nodes import TextNode, LeafNode, ParentNode

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    dir_list = os.listdir(dir_path_content)
    for file in dir_list:
        filepath = os.path.join(dir_path_content, file)
        if os.path.isfile(filepath) and file.endswith(".md"):
            dest_filepath = os.path.join(dest_dir_path, file[:-3] + ".html")
            generate_page(filepath, template_path, dest_filepath, basepath)
        if os.path.isdir(filepath):
            new_dest_dir_path = os.path.join(dest_dir_path, file)
            os.mkdir(new_dest_dir_path)
            generate_pages_recursive(filepath, template_path, new_dest_dir_path, basepath)

def generate_page(from_path, template_path, dest_path, basepath): 
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, encoding="utf-8") as file_markdown:
        markdown = file_markdown.read()
    with open(template_path, encoding="utf-8") as file_template:
        template = file_template.read()

    title = extract_title(markdown)
    html_node = markdown_to_html_node(markdown)
    html_string = html_node.to_html()

    output_string = template.replace("{{ Title }}", title, 1)
    output_string = output_string.replace("{{ Content }}", html_string, 1)
    output_string = output_string.replace("href=\"/", f"href=\"{basepath}")
    output_string = output_string.replace("src=\"/", f"src=\"{basepath}")
    
    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    with open(dest_path, 'w') as dest_file:
        dest_file.write(output_string)

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError(f"no markdown title found")

def copy_directory_recursive(source, destination):
    if not os.path.exists(destination):
        print(f"create directory {destination}")
        os.mkdir(destination)

    files = os.listdir(source)
    for filename in files:
        filepath = os.path.join(source, filename)
        if os.path.isfile(filepath):
            print(f"copy {filepath} to path {destination}")
            shutil.copy(filepath, destination)
        elif os.path.isdir(filepath):
            new_destination = os.path.join(destination, filename)
            copy_directory_recursive(filepath, new_destination)
        else:
            raise Exception(f"unexpected file type {filepath}")

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    parent = ParentNode("div", [])
    for block in blocks:
        block_type = block_to_blocktype(block)
        match block_type:
            case BlockType.PARAGRAPH:
                block_parent = ParentNode("p", [])
                textnodes = block_to_textnodes(block)
                for textnode in textnodes:
                    block_parent.children.append(text_node_to_html_node(textnode)) # type: ignore
                parent.children.append(block_parent) # type: ignore
            case BlockType.HEADING:
                count_sharp = len(block[:6].split(" ")[0])
                block = block[count_sharp+1:]
                block_parent = ParentNode(f"h{count_sharp}", [])
                textnodes = block_to_textnodes(block)
                for textnode in textnodes:
                    block_parent.children.append(text_node_to_html_node(textnode)) # type: ignore
                parent.children.append(block_parent) # type: ignore
            case BlockType.CODE:
                block = block[4:-4]
                block_parent = ParentNode("pre", [LeafNode("code", block)])
                parent.children.append(block_parent) # type: ignore
            case BlockType.QUOTE:
                block_parent = ParentNode("blockquote", [])
                lines = block.split("\n")
                for (i, line) in enumerate(lines):
                    line = line[1:]
                    line = line.strip()
                    if i != 0:
                        line = " " + line
                    textnodes = text_to_textnodes(line)
                    for textnode in textnodes:
                        block_parent.children.append(text_node_to_html_node(textnode)) # type: ignore
                parent.children.append(block_parent) # type: ignore
            case BlockType.UNORDERED_LIST:
                block_parent = ParentNode("ul", [])
                lines = block.split("\n")
                for (i, line) in enumerate(lines):
                    line = line[2:]
                    textnodes = text_to_textnodes(line)
                    line_parent = ParentNode("li", [])
                    for textnode in textnodes:
                        line_parent.children.append(text_node_to_html_node(textnode)) # type: ignore
                    block_parent.children.append(line_parent) # type: ignore
                parent.children.append(block_parent) # type: ignore
            case BlockType.ORDERED_LIST:
                block_parent = ParentNode("ol", [])
                lines = block.split("\n")
                for (i, line) in enumerate(lines):
                    line = line[3:]
                    textnodes = text_to_textnodes(line)
                    line_parent = ParentNode("li", [])
                    for textnode in textnodes:
                        line_parent.children.append(text_node_to_html_node(textnode)) # type: ignore
                    block_parent.children.append(line_parent) # type: ignore
                parent.children.append(block_parent) # type: ignore
            case _:
                raise ValueError(f"unexpected BlockType {block_type.value}")
    return parent

def block_to_textnodes(block):
    textnodes = []
    lines = block.split("\n")
    for (i, line) in enumerate(lines):
        line = line.strip()
        if i != 0 and len(line) != 0:
            line = " " + line #replaces single \n with whitespaces
        textnodes += text_to_textnodes(line)
    return textnodes

def block_to_blocktype(block):
    if block == "":
        return BlockType.PARAGRAPH
    lines = block.split("\n")
    match block[0]:
        case "#":
            for letter in block[:min(7, len(block))]:
                if letter == "#":
                    continue
                elif letter == " ":
                    return BlockType.HEADING
                else:
                    return BlockType.PARAGRAPH
            return BlockType.PARAGRAPH
        case "`":
            if len(block) < 6:
                return BlockType.PARAGRAPH
            if all(x == "`" for x in block[:3] + block[-3:]):
                return BlockType.CODE
            else:
                return BlockType.PARAGRAPH
        case ">":
            if all(len(line) > 0 for line in lines) and all(line[0] == ">" for line in lines):
                return BlockType.QUOTE
            else:
                return BlockType.PARAGRAPH
        case "-":
            if all(len(line) > 1 for line in lines) and all(line[:2] == "- " for line in lines):
                return BlockType.UNORDERED_LIST
            else:
                return BlockType.PARAGRAPH
        case "1":
            if any(len(line) <= 2 for line in lines):
                return BlockType.PARAGRAPH
            for (i, line) in enumerate(lines):
                if line[:3] != f"{i+1}. ":
                    return BlockType.PARAGRAPH
            return BlockType.ORDERED_LIST
        case _:
            return BlockType.PARAGRAPH

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    blocks = map(lambda string: string.strip(" \n"), blocks)
    return list(filter(
        lambda string: string != "", blocks
    ))

def text_to_textnodes(text):
    textnodes = [TextNode(text, TextType.TEXT)]
    textnodes = split_nodes_delimiter(textnodes, "**", TextType.BOLD)
    textnodes = split_nodes_delimiter(textnodes, "_", TextType.ITALIC)
    textnodes = split_nodes_delimiter(textnodes, "`", TextType.CODE)
    textnodes = split_nodes_image(textnodes)
    textnodes = split_nodes_link(textnodes)
    return textnodes

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href" : text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src" : text_node.url, "alt" : text_node.text})
        case _:
            raise ValueError(f"invalid text type for TextNode: {text_node.text_type}")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    match text_type:
        case TextType.TEXT:
            if delimiter != "":
                raise ValueError(f"delimiter \"{delimiter}\" does not match text_type \"{text_type.value}\"")
        case TextType.BOLD:
            if delimiter != "**":
                raise ValueError(f"delimiter \"{delimiter}\" does not match text_type \"{text_type.value}\"")
        case TextType.ITALIC:
            if delimiter != "_":
                raise ValueError(f"delimiter \"{delimiter}\" does not match text_type \"{text_type.value}\"")
        case TextType.CODE:
            if delimiter != "`":
                raise ValueError(f"delimiter \"{delimiter}\" does not match text_type \"{text_type.value}\"")
        case _:
            raise NotImplementedError(f"{text_type} not implemented")
    
    if text_type == TextType.TEXT:
        return old_nodes
    
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        split_lst = node.text.split(delimiter)
        if len(split_lst) % 2 == 0:
            raise ValueError(f"Wrong number of delimiter \"{delimiter}\" in \"{node.text}\"")
        for i in range(0, len(split_lst)):
                if split_lst[i] == "":
                    continue
                elif i % 2 == 0:
                    new_nodes.append(TextNode(split_lst[i], TextType.TEXT))
                else:
                    new_nodes.append(TextNode(split_lst[i], text_type))
    return new_nodes

def split_nodes_image(old_nodes):
        new_nodes = []
        for node in old_nodes:
            if node.text_type != TextType.TEXT:
                new_nodes.append(node)
                continue
            text = node.text
            images = extract_markdown_images(text)
            for image in images:
                text_split = text.split(f"![{image[0]}]({image[1]})")
                if text_split[0] != "":
                    new_nodes.append(TextNode(text_split[0], node.text_type))
                new_nodes.append(TextNode(image[0],TextType.IMAGE, image[1]))
                text = "".join(text_split[1:])
            if text != "":
                new_nodes.append(TextNode(text, node.text_type))

        return new_nodes

def split_nodes_link(old_nodes):
        new_nodes = []
        for node in old_nodes:
            if node.text_type != TextType.TEXT:
                new_nodes.append(node)
                continue
            text = node.text
            links = extract_markdown_links(text)
            for link in links:
                text_split = text.split(f"[{link[0]}]({link[1]})")
                if text_split[0] != "":
                    new_nodes.append(TextNode(text_split[0], node.text_type))
                new_nodes.append(TextNode(link[0],TextType.LINK, link[1]))
                text = "".join(text_split[1:])
            if text != "":
                new_nodes.append(TextNode(text, node.text_type))

        return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
