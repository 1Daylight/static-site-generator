from textnode import TextNode
from htmlnode import LeafNode, ParentNode
import re, os, shutil
from enum import Enum

def main():
    copy_files_to_public()
    generate_pages_recursive("content", "template.html", "public")

class Blocks(Enum):
    Paragraph = 1
    Heading = 2
    Code = 3
    Quote = 4
    Unordered_List = 5
    Ordered_List = 6


def text_node_to_html_node(text_node): 
    if text_node.text_type == "text":
        return LeafNode(None, text_node.text)
    if text_node.text_type == "bold":
        return LeafNode("b", text_node.text)
    if text_node.text_type == "italic":
        return LeafNode("i", text_node.text)
    if text_node.text_type == "code":
        return LeafNode("code", text_node.text)
    if text_node.text_type == "link":
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.text_type == "image":
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    
def split_nodes_delimiter(old_nodes, delimiter, text_type): 
    new_nodes = []
    for node in old_nodes: 
        if node.text_type != "text":
            new_nodes.append(node)
        else: 
            subnodes = node.text.split(delimiter)
            if len(subnodes) % 2 != 1:
                raise Exception("Missing closing delimiter")
            for i in range(0, len(subnodes)):
                type = ""
                if i % 2 == 0: 
                    type = "text"
                else: 
                    type = text_type
                new_nodes.append(TextNode(subnodes[i], type))
    return new_nodes

def extract_markdown_images(text):
    extracted = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return extracted

def extract_markdown_links(text):
    extracted = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return extracted

def split_nodes_images(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != "text":
            new_nodes.append(node)
        else:
            images = extract_markdown_images(node.text)    
            node_text = ""       
            if len(images) == 0: 
                new_nodes.append(node)         
            else: 
                node_text = node.text
                for image in images:                    
                    split_text = node_text.split(f"![{image[0]}]({image[1]})", 1)
                    if len(split_text[0]) != 0: 
                        new_nodes.append(TextNode(split_text[0], "text"))
                    new_nodes.append(TextNode(image[0], "image", image[1]))
                    if len(split_text) > 1: 
                        node_text = split_text[1]
                    else:
                        node_text == ""
            if len(node_text) != 0:
                new_nodes.append(TextNode(node_text, "text"))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != "text":
            new_nodes.append(node)
        else:
            links = extract_markdown_links(node.text)    
            node_text = ""     
            if len(links) == 0: 
                new_nodes.append(node)         
            else: 
                node_text = node.text
                for link in links:                    
                    split_text = node_text.split(f"[{link[0]}]({link[1]})", 1)
                    if len(split_text[0]) != 0: 
                        new_nodes.append(TextNode(split_text[0], "text"))
                    new_nodes.append(TextNode(link[0], "link", link[1]))
                    if len(split_text) > 1: 
                        node_text = split_text[1]
                    else:
                        node_text == ""
            if len(node_text) != 0:
                new_nodes.append(TextNode(node_text, "text"))
    return new_nodes
    
def text_to_textnodes(text): 
    nodes = [TextNode(text, "text")]
    nodes = split_nodes_images(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", "bold")
    nodes = split_nodes_delimiter(nodes, "*", "italic")
    nodes = split_nodes_delimiter(nodes, "`", "code")
    return nodes

def textnodes_to_html(text_nodes):
    html_nodes = []
    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    blocks = list(map(lambda x: x.strip(), blocks))
    return blocks

def block_to_block_type(block):
    if len(block) == 0:
        raise Exception("Empty Block detected!")
    if block.startswith("# ") or block.startswith("## ") or block.startswith("### ") or block.startswith("#### ") or block.startswith("##### ") or block.startswith("###### "):
        return Blocks.Heading
    if block.startswith("```") and block.endswith("```"):
        return Blocks.Code
    lines = block.split("\n")
    if check_if_all_lines_start_with(lines, ">"):
        return Blocks.Quote
    if check_if_all_lines_start_with(lines, "* ") or check_if_all_lines_start_with(lines, "- "):
        return Blocks.Unordered_List
    for i in range (0, len(lines)):
        index = i+1
        if not lines[i].startswith(f"{index}. "):
            return Blocks.Paragraph
    return Blocks.Ordered_List
    
def check_if_all_lines_start_with(lines, delimiter):
    for line in lines:
        if not line.startswith(delimiter):
            return False
    return True

def code_block_to_html(block): 
    return ParentNode("pre", [ParentNode("code", textnodes_to_html(text_to_textnodes(block[3:-3].strip())))])

def quote_block_to_html(block):
    return ParentNode("blockquote", textnodes_to_html(text_to_textnodes("\n".join(map(lambda x: x[1:], block.split("\n"))))))

def ulist_block_to_html(block):
    parent = ParentNode("ul", [])
    lines = block.split("\n")
    for line in lines:
        parent.children.append(ParentNode("li", textnodes_to_html(text_to_textnodes(line[2:]))))
    return parent

def olist_block_to_html(block):
    parent = ParentNode("ol", [])
    lines = block.split("\n")
    for line in lines:
        parent.children.append(ParentNode("li", textnodes_to_html(text_to_textnodes(line[3:]))))
    return parent

def heading_block_to_html(block):
    heading = block.split(" ", 1)
    return ParentNode("h" + str(len(heading[0])), textnodes_to_html(text_to_textnodes(heading[1])))

def paragraph_block_to_html(block):
    return ParentNode("p", textnodes_to_html(text_to_textnodes(block)))

def markdown_to_html_node(markdown):

    block_functions = {
        Blocks.Code: code_block_to_html,
        Blocks.Heading: heading_block_to_html,
        Blocks.Ordered_List: olist_block_to_html,
        Blocks.Paragraph: paragraph_block_to_html,
        Blocks.Unordered_List: ulist_block_to_html,
        Blocks.Quote: quote_block_to_html
    }
    root = ParentNode("div", [])
    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        type = block_to_block_type(block)
        html = block_functions[type](block)
        root.children.append(html)
    
    return root

def extract_title(markdown):
    for line in markdown.split("\n"):
        if line.startswith("# "):
            return line[2:]
    raise Exception("Missing title")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown = ""
    with open(from_path) as f: 
        markdown = f.read()
    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    template = ""
    with open(template_path) as f:
        template = f.read()
    text = html.join(template.split(r"{{ Content }}"))
    text = title.join(text.split(r"{{ Title }}"))
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w+") as f:
        f.write(text)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for file in os.listdir(dir_path_content):
        if os.path.isfile(dir_path_content + "/" + file):
            generate_page(dir_path_content + "/" + file, template_path, dest_dir_path + "/" + file[:-2] + "html")
        else: 
            os.mkdir(dest_dir_path + "/" + file)
            generate_pages_recursive(dir_path_content + "/" + file, template_path, dest_dir_path + "/" + file)

def copy_files_to_public():
    try:
        shutil.rmtree("public/")
    except: 
        pass
    os.mkdir("public")
    copy_files("static", "public")

def copy_files(src, dst):
    for file in os.listdir(src):
        if os.path.isfile(src + "/" + file):
            shutil.copy(src + "/" + file, dst)
        else: 
            os.mkdir(dst + "/" + file)
            copy_files(src + "/" + file, dst + "/" + file)

main()
