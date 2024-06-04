import os
import hashlib

GIT_DIR = ".mygit"

def init():
    os.makedirs(GIT_DIR)
    os.makedirs(f'{GIT_DIR}/objects')
    
def hash_object(data, type_="blob"):
    
    object = type_.encode() + b'\x00' + data
    objectID = hashlib.sha1(object).hexdigest()
    
    with open(f'{GIT_DIR}/objects/{objectID}', "wb") as out:
        out.write(object)
    return objectID

def get_object(objectID, expected="blob"):
    
    with open(f'{GIT_DIR}/objects/{objectID}', "rb") as f:
        object = f.read()
        
    type_, nullByte, data = object.partition(b'\x00')
    
    if expected is not None:
        assert type_ == expected, f'Expected {expected}, got {type_}'
    return data