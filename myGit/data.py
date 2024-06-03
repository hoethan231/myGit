import os
import hashlib

GIT_DIR = ".mygit"

def init():
    os.makedirs(GIT_DIR)
    os.makedirs(f'{GIT_DIR}/objects')
    
def hash_object(data):
    objectID = hashlib.sha1(data).hexdigest()
    with open(f'{GIT_DIR}/objects/{objectID}', "wb") as out:
        out.write(data)
    return objectID

def get_object(objectID):
    with open(f'{GIT_DIR}/objects/{objectID}', "rb") as f:
        return f.read()