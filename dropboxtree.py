# A Class to build a tree from a DropBox folder 
'''
This module implements a Node class that is aimed to represent a node in a file tree of a Dropbox account. Each Node object consists of the following properties:

name: The name of the folder or file,
path: The file path in Dropbox,
size: The size of the folder or file in bytes (default is 0),
file_count: The number of files in this folder (default is 0),
children: A list of children nodes (other Node objects).

The Node class also provides a to_dict method to transform the Node object into a dictionary for serialization and a class method from_dict to construct a Node object from a dictionary object. These two methods allow for the Node objects to be converted into JSON format for easy storage and retrieval.
Furthermore, the Node object can also visualize itself and its children nodes in a tree structure using the print_tree method. Another method, download_files, is used for downloading the files represented by the Node object according to certain conditions. Please note that this Node class can be used as a part of a more comprehensive Dropbox account management application and can be utilized to perform operations like downloading folders and files, observing folder sizes and file counts, and visualizing folder structures.
'''
import dropbox
import os
import json
#from datetime import datetime as date

access_token = 'uat.ABXsvuqLawhOU5jC0okO_Axl0-e5KNLJkbkwaVf7zhok_eJg8PY-vM11_Ixxtz1sp2uhoy288_NWGWB7O3LwI4_YHmtah6Lk1YTvG6IVJeKbzy_d8Hdizogt8E5gEXrAxKfPcXV5kU4cri8fkOlqh1HgUV2_j2OQJerfiNrp3QVWwfAiQaaq5Z5wq3-zRxNd50m7rv8uq5kUbHghX_xo4xZ1Hf1rJC7KtTEdNaekEvMFK8J1SpFLE8XRy0uU0_Jixarz1uJY4a0Z_84hQnMCifVBmUbvjCHrN4lZ2WalHMW3pwyZo1qpPwddIBYmWVwmFaGiAThV0FBqiaIXfvigMXdFvUoaiZVLBPQ7yGCtGDn2KgSg0tkTzMl7jRTCG_8AtL5WrERnWcgy3jYeCStsaRBAxHrbNlcgMo9nt3vJBkYeWknm6ErOx4IKXXp4RbqcoGEwK0ZUyslCUFoEkSxLNRZRh1Dkmyc8rMUdGyVem-ys2itTRySe_HRxx2nimd3HafMW4tnQKYe5Qbmq673a33ra-_rj1fQhfU6ZvEFKf2CPhMg-YZQMLpIgMLf4XCtUVNAIve1-KQjMqD1TQrJPnciisJn3BQN_M71pvUUWzgOl52mQLaqXQqeplTPmHTtMx7I31oPn_ahw6WjBF3BNsr4I-cowKVJVYYTuAhBNr2hlrPfztrp17EoTur4Q2b-lCrMkIJZpbp2B8lDHjXy5vmpD4v-b_Fz4Kez8ozapeOuZ4cJwSi6u9q48Odih4lKg_m30GJJyIA5k_iNuhj1Iqrt0DP2VTZKQHtotIKOXQma2RyPMPnZoWHOn3y394ksp8169V1VxD8Zmlw3y7XeKxozOy5qOpsbeAfDsVqLlzQ7LRVg4PCJgXXaW89df9zROATp6QtbXUnwN32vAFw4euRHCxKLV2GUyTOulhk7RyaZA-oqNja_zvhZuOBbOP4oPNxWh4UCFfjSohLfvHgZjzHzxZER-OFA_AaF8OoJRRTrKEhQLwzkBhCj_QzNsXqXkLyi4--ecWtqS4_EKXm3_JcvZkLo0sQenNlR8onBZcZ8ZYZTCQ-pPzc3ynWtY1SV687OOTlKKWjtjQyCCKhjXgknuV1yxj2IIfSQPTVhGwGvMbcbXy1jzLd4rNBmD8XU2MsLaN3VbsnhaeUWpYOTZBXqR3yqwXPtyCzLvnetWzwMXK8X-akVTmdKPiT7iryMJAXPPqGG60z8BnpKQU2W8s1DUf--7_0FGUcEx_da-zyaKHQkO7brZapun2FoFETEgDP3LALq1WeCRFIhwLm2DFmOGNTOPYquL3Bf7RgVrXZNET9vUsOsbYTkVXYYikQYHVDM'
dbx = dropbox.Dropbox(access_token)

class Node:

    def __init__(self, name, path, size=0,file_count=0, children=None, errors=None,errorlist=None):
        self.name = name  # folder or file name
        self.path = path  # path in dropbox
        self.size = size  # size of folder or file
        self.file_count = file_count  # number of files in this folder
        self.children = [Node.from_dict(child) for child in children] if children else []
        self.errors = [Node.from_dict(error) for error in errors] if errors else [] # list of filepaths that errored during the creation of the tree. 
        errorlist = errorlist
    def add_child(self, child):
        self.children.append(child)

    def print_tree(self, prefix=""):
        print(f"{prefix}|-- {self.name}, {(self.size/1024/1024/104)} gigabytes, {self.file_count} files")
        prefix += " "
        for child in self.children:
            child.print_tree(prefix)
    
    def download_files(self, dbx, destination_folder):
        destination_path = os.path.join(destination_folder, self.name)
        print(destination_path)
        if self.file_count < 10000 and self.file_count > 0 and self.size < 20 * 1024 * 1024 * 1024:
            # If the folder is small enough, download it as a zip
            with open(destination_path + ".zip", "wb") as f:
                metadata, response = dbx.files_download_zip(self.path) #chunk downloads
                f.write(response.content)
        else:
            # If the folder is too large, download file by file and recursively check sub-folders
            for child in self.children:
                if child.file_count == 0:  # It's a file
                    with open(os.path.join(destination_path, child.name), "wb") as f:
                        metadata, response = dbx.files_download(child.path)
                        f.write(response.content)
                else:  # It's a directory
                    if not os.path.exists(destination_path): 
                    os.makedirs(destination_path)
                    child.download_files(dbx, destination_path)
       
            
        
    def to_dict(self):
        return {
            "name": self.name,
            "path": self.path,
            "size": self.size,
            "file_count": self.file_count,
            "children": [child.to_dict() for child in self.children],
            "errors": self.errors,
            "total_errors": errorlist
        }
    @classmethod
    def from_dict(cls, dict):
        return cls(dict.get("name", ""), dict.get("path", ""), dict.get("size", 0), dict.get("file_count", 0), dict.get("children", None), dict.get("errors", None))  
        
def get_folder_size(node):
    total_size = 0
    try:
        res = dbx.files_list_folder(node.path, recursive=True)
        while True:
            total_size += sum(entry.size for entry in res.entries if isinstance(entry, dropbox.files.FileMetadata))
            node.file_count += sum(1 for entry in res.entries if isinstance(entry, dropbox.files.FileMetadata))
            res = dbx.files_list_folder_continue(res.cursor) if res.has_more else None
            if res is None:
                break
    except dropbox.exceptions.ApiError as e:
        print(f"[WARNING] Failed to list files for folder {node.path} due to API error: {e}")
        errorlist.append(node.path)
        node.errors.append(node.path)
    node.size = total_size
    return total_size

def create_tree(path):
    root_node = Node("", path)
    get_folder_size(root_node)
    map_children(root_node)
    return root_node

def map_children(node):
    res = dbx.files_list_folder(node.path, recursive=False)
    try:
        while True:
            for entry in res.entries:
                if isinstance(entry, dropbox.files.FileMetadata):
                    node.add_child(Node(entry.name, entry.path_display, entry.size))
                    node.file_count += 1
                if isinstance(entry, dropbox.files.FolderMetadata):
                    child_node = Node(entry.name, entry.path_lower)
                    get_folder_size(child_node)
                    map_children(child_node)
                    node.add_child(child_node)
            res = dbx.files_list_folder_continue(res.cursor) if res.has_more else None
            if res is None:
                break
    except dropbox.exceptions.ApiError as e:
        print(f"[WARNING] Failed to list children for folder {node.path} due to API error: {e}")

def save_tree_to_file(root, filename):
    with open(filename, 'w') as file:
        json.dump(root.to_dict(), file)

def load_tree_from_file(filename):
    with open(filename, 'r') as f:
        tree_dict = json.load(f)
        errorlist = tree_dict.get("total_errors",None)
    return Node.from_dict(tree_dict),errorlist



errorlist = []
#root = create_tree('/WLMS & Izzy Build Steps')
#root = create_tree('/CEG 1 - All Lab Members')
#root.print_tree()
#print(errorlist)
#save_tree_to_file(root, 'CEG_1.json')
''' download function
download_path = "\\\\lsa-rosati-win.turbo.storage.umich.edu\lsa-rosati\Google-Drive-Backup\\"  
final_path = download_path + date.now().strftime("%Y") + "\\" + date.now().strftime("%B %Y")
root.download_files(dbx,final_path)
'''