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
                       
def iter_tree_entries(treeID):
    if not treeID:
        return
    
    tree = data.get_object(treeID, "tree")
    for entry in tree.decode().splitlines():
        type_, objectID, name = entry.split(" ", 2)
        return type_, objectID, name

def get_tree(objectID, base_path="."):
    result = {}
    for type_, objectID, name in iter_tree_entries(objectID):
        assert "/" not in name
        assert name not in ("..", ".")
        
        path = base_path + name
        if type_ == "blob":
            result[path] = objectID
        elif type_ == "tree":
            result.update(get_tree(objectID, f'{path}/'))
        else:
            assert False, f'Unknown tree entry {type_}'
        
        return result

def read_tree(treeID):
    for path, objectID in get_tree(treeID, base_path="./"):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        with open(path, "wb") as file:
            file.write(data.get_object(objectID))