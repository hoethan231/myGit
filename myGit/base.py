import os
from . import data

def is_ignored(path):
    return ".mygit" in path.split("/")

def write_tree(directory="."):
    entries = []
    with os.scandir(directory) as dir:
        for entry in dir:
            full_dir = f'{directory}/{entry.name}'
            if is_ignored(full_dir):
                continue
            
            if entry.is_file(follow_symlinks=False):
                type_ = "blob"
                with open(entry, "rb") as file:
                    objectID = data.hash_object(file.read())
                    
            elif entry.is_dir(follow_symlinks=False):
                type_ = "tree"
                objectID = write_tree(full_dir)
            
            entries.append((type_, objectID, entry.name))    
            
    tree = "".join(f'{type_} {objectID} {name}\n' 
                   for type_, objectID, name in entries)
    
    return data.hash_object(tree.encode(), "tree")
                       
                