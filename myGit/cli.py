import argparse
import textwarp
import sys
import os
from . import data
from . import base

def main():
    args = parse_args()
    args.func(args)
    
def parse_args():
    parser = argparse.ArgumentParser()
    
    commands = parser.add_subparsers(dest="command")
    commands.required = True
    
    init_parser = commands.add_parser("init")
    init_parser.set_defaults(func=init)
    
    hash_object_parser = commands.add_parser("hash-object")
    hash_object_parser.set_defaults(func=hash_object)
    hash_object_parser.add_argument("file")
    
    cat_file_parser = commands.add_parser("cat-file")
    cat_file_parser.set_defaults(func=cat_file)
    cat_file_parser.add_argument("object")
    
    write_tree_parser = commands.add_parser("write-tree")
    write_tree_parser.set_defaults(func=write_tree)
    
    read_tree_parser = commands.add_parser("read-tree")
    read_tree_parser.set_defaults(func=read_tree)
    read_tree_parser.add_argument("tree")
    
    commit_parser = commands.add_parser("commit")
    commit_parser.set_defaults(func=commit)
    commit_parser.add_argument("message")
    
    log_parser = commands.add_parser("log")
    log_parser.set_defaults(func=log)
    
    return parser.parse_args()

def init(args):
    data.init()
    print(f'Initialized empty mygit repository in {os.getcwd()}\{data.GIT_DIR}')
    
def hash_object(args):
    with open(args.file, "rb") as f:
        print(data.hash_object(f.read()))
        
def cat_file(args):
    sys.stdout.flush()
    sys.stdout.buffer.write(data.get_object(args.object, expected=None))

def write_tree(args):
    print(base.write_tree())
    
def read_tree(args):
    base.read_tree(args.tree)
    
def commit(args):
    print(base.commit(args.message))
    
def log(args):
    objectID = data.get_HEAD()
    while objectID:
        commit = base.get_commit(objectID)
        print(f'commit {objectID}\n')
        print(textwarp.indent(commit.message, "    "))
        print("")
        objectID = commit.parent