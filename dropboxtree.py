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


# import rich for cleaner output
#from rich.traceback import install
#install(show_locals=True)
#from datetime import datetime as date
#add OAUTH
access_token = 'uat.ABbDbpLiqMwyuDkYtBdTUrYjm-gP36LH5o0KYuw2ihkSDqV_7EZLwNw5oE3oyEgU6SNfUu5WeZD077GYmBS9_6qgZ88IN1-OcO05PGtb1OgHdemnEJeKlYbxt7Aota_AVKlfpdbM5cDqeKYi5lOoQVHqno0aNh0Qf-3vTSZncYpntFekcpb-idNhD1S8OGBEkoYComntr43sBx1KjR-0St6lbBN_YYVmDOngz_7z-9KKuPFQeU_jDlbyvvtSmXBfxxuGbORSbcv5LhtNl8q8Xs_SJPIN6n3UpdMmTDDgxhM2taBJdmzaCmB6R-s9qOdgG-R2ZIiAk3oXp0rddZClgz-QbkZ8n7dzIJsRTO-qiwdv2Bq7dTVLpTBTpYstGglc2ouazPZsu5uLsXutQfKLa-P8NhsR4JnZPbVT4B4cYcMMsq4RF5_Kw9fVpmgS3fbZCFAH4m4TEEB83_ezJzcxVqyZpTNDL7oqM5jene05XWDVSYnt0oEEEq0PrA0BzSCQYD0uBaE9Oy0J4T3p046m23eUZlf2nm4MbcBQbRH2g3P-qZRo53d6zy5lCdcBUBZsjS3x4rP40sebOOxTz6R9mB6-YMUrZkhoeH1Cl_ntJ1dn0IW6IVRsJKkj8W-o4i7E2ByETUNNammCiAMbW8NAyFDhytv2E2gmh7FDzkpiy_ROykSe8LsTFPwlkk27k5tfu2j84OhCGHyEruaCWj-XIK4Q970k6ikMmnMmelAIHOJqe1C0tsWR3iPDoGmU6GQawYO6OJqlMo5JSYjEB8N68z7bLivoc7SoY_L5hbW8hj57qgCYGj26nKQksEy2_pJGzJHPbwLjsKKDq8vy4Qpjvlcq4u4h8G2jswpEtkW0CYiQuGTa5WjxAsJiwijEEoG0OZI7lTmwqboB-acSiW54PL51Skdt7M9OktH0RcLd6tciax5IQu1sKgjkcndpJwVDciUcuzYJD0d3CKEs1seQdiP5enpEf-l4-NTEsFEgvTa19d7TnHMPfJnHYu8MFtYDY6E6Q00DLSceYTB3JvMQoUPb2betqmtjC1XfW71QDNpc_OIRWbcWR44yVQ1GPSbMAtImWFnjVm3__oUW3pLP2eNfO0bEWmQMd6VqqvMLOlBOIbx4qiYGG7q-VUanM0nJb5AzoEKL-1SiCJZXdNLhrNo7anBdEYz8Vqrd2uxIFt7tFTwPGELeWJxp4X7Lay4Jq47ZI_euiP2XLDRkA13xAxtG8WDaVzh2zH-AocriTpc-AAbYgL6NhAWVcxwmf2VeExG2rcdH14RTrS9G_PgmiCbD4kME8WZPjk05DLCUT9UOWMVSogpEuXJmqGW4UvW6IXM'
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
    
    def download_files(self, dbx, destination_folder): # Download tree to destination folder
        destination_path = os.path.join(destination_folder, self.name)
        print(f"Copying Dropbox Folder {self.path} to {destination_path}")
        # If the folder is less than 20GB, less than 10,000 files and doesn't already exist, download as a .zip.
        if self.file_count < 10000 and self.file_count > 0 and self.size < 20 * 1024 * 1024 * 1024:
            zip_path = destination_path + ".zip"
            if not os.path.exists(zip_path):  
                print(f"downloading Directory {zip_path} as .zip file")
                with open(zip_path, "wb") as f:
                    metadata, response = dbx.files_download_zip(self.path) #chunk downloads
                    for chunk in response.iter_content(chunk_size=8* 1024 * 1024):  # chunk size is 8MB
                        if chunk:
                            f.write(chunk)
            else:
                print(f"    Skipped. {self.name} already zipped  at {zip_path}")
        else:
            # If the folder is too large, Copy its files and subfolders
            for child in self.children:
                file_path = os.path.join(destination_path, child.name)
                # if it's a file, check if it exists then copy
                if child.file_count == 0:  # It's a file   
                    if not os.path.exists(file_path):
                        print(f"    Downloading file {child.path}")
                        with open(file_path, "wb") as f:
                            metadata, response = dbx.files_download(child.path)
                            for chunk in response.iter_content(chunk_size=8* 1024 * 1024):  # chunk size is 8MB
                                if chunk:
                                    f.write(chunk)
                    else: 
                        print(f"    Skipped. File {child.name} already exists at {file_path}")
                else:  # It's a directory
                    # If folder or zipped folder doesn't exist, make directory. 
                    #folder_path = os.path.join(destination_path, child.name)
                    #zipped_folder = folder_path + ".zip"
                    #if not os.path.exists(folder_path) and not os.path.exists(zipped_folder): 
                        #print(folder_path)
                        #print(zipped_folder)   
                        #print(f"    Creating Folder {child.path}") 
                    os.makedirs(file_path)
                    #else: 
                         #print(f"    Skipped. Folder already exists at {folder_path}")
                    child.download_files(dbx, destination_path) #traverse into subfolders and restart function
                    
                        
                        
       
            
        
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