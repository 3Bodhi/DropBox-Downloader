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
from dropbox.exceptions import AuthError
import os
import webbrowser
import json
import zipfile
import shutil
from rich import print




APP_KEY = 'at5epqggtx1gfrh'
APP_SECRET = '03xtulcqj0bcie7'
OAUTH_SCOPE = ['account_info.read','files.metadata.read', 'files.content.read','fil_requests.read','Team_data.member','team_data.governance.write','team_data.governance.read','team_data.content.read']


def get_oauth2_authorize_url():
    flow = dropbox.DropboxOAuth2FlowNoRedirect(APP_KEY, OAUTH_SCOPE)
    authorize_url = flow.start()
    return authorize_url

def get_access_token(code):
    try:
        flow = dropbox.DropboxOAuth2FlowNoRedirect(APP_KEY, OAUTH_SCOPE) 
        oauth_result = flow.finish(code)
        return oauth_result.access_token
    except Exception as e:
        print('Error in get_access_token', e)
        return None
    
def Oauth():
    # Get the authorization URL and show it to the user, asking them to visit it in the browser
    auth_url = get_oauth2_authorize_url()
    webbrowser.open(auth_url)
    print('Please authorize the app by visiting this URL: %s\n' % auth_url)

    # After the user completes the authorization, Dropbox will provide a code
    auth_code = input("Enter the authorization code here: ").strip()

    # The script uses the authorization code to request an access token
    access_token = get_access_token(auth_code)
    print("Your access token: ", access_token)

    if access_token is not None:
        dbx = dropbox.Dropbox(access_token)
        print(dbx)
        print("Success!")
        return dbx
        # your existing code here ...
#Oauth()




# ToDOs:
# import rich for cleaner output
#from rich.traceback import install
#install(show_locals=True)
#from datetime import datetime as date
#add OAUTH catch dropbox.exceptions.AuthError

access_token = 'uat.ADjlUNFbRx3S7e6YH0n6O0xwr_5HGgDYUFxMbxyXItLjXUF8ZzitOEesPOzsCLKU8ZPo0rn9vJxtMDiXoR5sckblS0eLBFQQLE56mC0MV87uIiWbPncLUDYfBpJVWjs2YvevbwW2UQ8nMwuExEucd3HlVF34mzseU7DBfBrPZXg1cNtBxODeJFxjWL_gA1aYP58kRC0KZfG33y1qY4nn0Irx7gLOae69Me2he3h87UOKzvBE9HZmz4qLRgM7zBf6ZGNsAytvXnD0kqDrKILACnA5Ova-e401AI4BTPr0ZdX65NQGcee8gi6UpuCxvXcSfsEU4AcH3FmQLH3Ywi9DefcOQ_BEsU_CrDR4q90PYLa0TzQUzeGN97mRtLYp_Ddju0XD-GRoSV09XZBNmjWFFMrW178r5iFHVTJobZMeQM-LYv0pAerbtcAOiBeZdXijyl7uPUkJo5VQGIaiU2wxGw6YUVfAAOUXv5YKtG_fvM1LFZ4LK0dFdxxQobdgmvTIaaGBOHUxKAx1EbMKYqJMw38ZW8bP8aYCC2OietIY_KldtVxAGfK_qN73YP-XN42Q-KcCtV8mHumU4MnsFOTopUbJ6ekIARyemgiJm9JP34cbu2B91pL_rNgK5PR7F0WAXOJyBbZch2nhUrVMEO0EgvwLE0twwBT6hU0qJ8HPJDlzm0W9ZmeBU2q2q9qOEv63nOMT9uyMWyTJoD6iEtk0QLR_f1HaDwjk2JB76CGqYwMrlOpQpCA_Hg1j6DNV7W5z4ASO1vLdIIKhQPXRq7Y9_SQPI51ll9--JMPV8zQsiA8Ho-soV7-I_uoGiANKpt5J09hj3cT2TYv8MUPsQnOdUqhWequ8z657-zUqd5Gifq8DIKY_8mRue1IOC3QBJAZhvIqk0rys4UJgCyMLqUgjkvIA-aBAJAeDv8aC9MPPm7tstC8eHPKo4q1i0geMjugNxfXXlyXbloAxJaen5V1W-L2vs6kTsx1SLbT21kSHSd8hHHlPlviSMo90oqKchGafIaOrMea8AdS-dvy8djcEBW3LvZkJzltMpCKMPgyFHRXgzAibmQ3IYnlFRvPCzC4l7iwTw9pa83usa9X7j6OFjZ9WI4BDgaJR2NLxuoj2-uMJCYkbLfC5DlATYXiheaPUnL2oBuBGiGFtoahyh_25aOgXX9OCdDlmbFhb5C7ASLBaNZbOVG7y_cqIg-49Btb5I4KsS7RvNBawwcJoYcnYjuS_MP1wahRZEVV84CKNuy7mTWPxrQLu2_hCoIGukgaQsA5FdexCdagWR547gwQtrLNzYdHPdvLPQ3AD70KXsiEAuFW_pED0mE_0Nsuu2pO90FA'
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
        print(f"Copying Dropbox Folder {self.path}\nto {destination_path}")
        # If the folder is less than 20GB, less than 10,000 files and doesn't already exist, download as a .zip.
        # NOTE zip fails with internal server error if restricted files are in the zipped folder. Except error, copy folder as if it was a normal folder.
        # NOTE zip fails with internal server error if restricted files are in the zipped folder. Except error, copy folder as if it was a normal folder.
        if self.file_count < 10000 and self.file_count > 0 and self.size < 20 * 1024 * 1024 * 1024:
            zip_path = destination_path + ".zip"
            flag_file_path = zip_path + ".incomplete" # flag file for incomplete downloads Maybe try modifying JSON?
            if os.path.exists(flag_file_path):
                os.remove(zip_path)  # delete incomplete file
            if (not os.path.exists(zip_path)) and (not os.path.exists(destination_path)):  
                print(f"    downloading Folder {self.path} as .zip file")
                try:
                    with open(flag_file_path, 'w') as flag_file:  # create a flag file
                        pass
                    with open(zip_path, "wb") as f:
                        metadata, response = dbx.files_download_zip(self.path) #chunk downloads
                        for chunk in response.iter_content(chunk_size=8* 1024 * 1024):  # chunk size is 8MB
                            if chunk:
                                f.write(chunk)
                    os.remove(flag_file_path)
                     # Extract the .zip file
                     # to-do ADD option to run or not run this
                    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                        print(f"        extracting {self.path}")
                        subdirectory = destination_path + '/' + zip_ref.namelist()[0]
                        zip_ref.extractall(destination_path)
                        shutil.copytree(subdirectory, destination_path, dirs_exist_ok=True)
                        shutil.rmtree(subdirectory)
                    os.remove(zip_path)
                except  dropbox.exceptions.InternalServerError as s:
                    print(f"{s}. Does {self.path} contain restricted files?" )
                    #TODO when donwload_files is refactored into several functions, add logic to redirected zip 500 exceptions to try to download individual files.
                except dropbox.exceptions.AuthError as a:
                    print(f"{a}.Please Generate a new API Token and run the program again.")
                print(f"    Skipped. {self.name} already zipped  at {zip_path}")
        else:
             # If the folder is too large, Copy its files and subfolders
            if not os.path.exists(destination_path):
                os.makedirs(destination_path) 
            for child in self.children: #traverse down to children i.e. subfolders and files
                file_path = os.path.join(destination_path, child.name)
                # if it's a file, check if it exists then download
                if child.file_count == 0:  # It's a file
                    flag_file_path = file_path + ".incomplete" # flag file for incomplete downloads Maybe try modifying JSON?
                    if os.path.exists(flag_file_path):
                        os.remove(file_path)  # delete incomplete file
                    if not os.path.exists(file_path):
                        print(f"    Downloading file {child.path}")
                        with open(flag_file_path, 'w') as flag_file:  # create a flag file
                            pass
                        with open(file_path, "wb") as f:
                            metadata, response = dbx.files_download(child.path)
                            for chunk in response.iter_content(chunk_size=8* 1024 * 1024):  # chunk size is 8MB
                                if chunk:
                                    f.write(chunk)
                        os.remove(flag_file_path)
                    else: 
                        print(f"    Skipped. File {child.name} already exists at {file_path}")
                else:  # It's a directory; recurse function
                    child.download_files(dbx, destination_path) 

                    ##### SLATED TO DELETE
                     #If folder or zipped folder doesn't exist, make directory. 
                    '''folder_path = os.path.join(destination_path, child.name)
                    zipped_folder = folder_path + ".zip"
                    if not os.path.exists(folder_path) and not os.path.exists(zipped_folder): 
                        print(folder_path)
                        print(zipped_folder)   
                        print(f"    Creating Folder {child.path}")
                        os.makedirs(folder_path)                  
                    else: 
                         print(f"    Skipped. Folder already exists at {folder_path}") '''
                    #child.download_files(dbx, destination_path) #traverse into subfolders and restart function                     
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
'''
#root = create_tree('/WLMS & Izzy Build Steps')
root = create_tree('/CEG 1 - All Lab Members')
root.print_tree()
print(errorlist)
save_tree_to_file(root, 'CEG_1.json')
'''