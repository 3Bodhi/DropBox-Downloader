import dropbox
import os
from datetime import datetime as date
import json


class Node:
    def __init__(self, name, path, size=0):
        self.name = name  # folder or file name
        self.path = path  # path in dropbox
        self.size = size  # size of folder or file
        self.file_count = 0  # number of files in this folder
        self.children = []  # list of children nodes
        self.errors = [] # list of filepaths that errored during the creation of the tree. 

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
        if not os.path.exists(destination_path):
            os.makedirs(destination_path)

        if self.file_count < 10000 and self.size < 20 * 1024 * 1024 * 1024:
            # If the folder is small enough, download it as a zip
            with open(destination_path + ".zip", "wb") as f:
                metadata, response = dbx.files_download_zip(self.path)
                f.write(response.content)
        else:
            # If the folder is too large, download file by file and recursively check sub-folders
            for child in self.children:
                if child.file_count == 0:  # It's a file
                    with open(os.path.join(destination_path, child.name), "wb") as f:
                        metadata, response = dbx.files_download(child.path)
                        f.write(response.content)
                else:  # It's a directory
                    child.download_files(dbx, destination_path)
    
    def to_dict(self):
        return {
            "name": self.name,
            "path": self.path,
            "size": self.size,
            "file_count": self.file_count,
            "children": [child.to_dict() for child in self.children],
            "errors": self.errors
        }

access_token = 'uat.AA6pcHUNDu5gkjE_ToaUCArlgeDboICLmpkosUHJ8TF69htr6bMlozfJV2Gj1jlvAfcXgr_RzyImRCUIqYiELdvHoLwZ29dA99nMwALwVtKlaj-vI0beYgswHknOsUe1df4jaV0D3aLR_vHHhbc_TFJ-MvRtPPC9y7DNeMOAuhzYbr8AZQPDUDjmSU0EQbcbLO-V59Wz7r_0if8z9jiUT8SHw_LCW8uGavH1pMBcd2bfLAOSTp784pKxASfmFi5Gxe8DxG5cy60Ec5FrIg0J_rsz04aOsfXCRfOD0k7MBu_7cPRTSSxhcoDHYYuwqgccC2b74xxv5mZVSk3Pbdc_82KjXB0cObNSoS6MRg4P3FIyOashHbDLUIcvWX6nBhgmzxtdk5ue2rvhliUfiTS_WycYNuEbc7PxEvbmzXg75XlyXQWiK4fu0L5af6SY26xHdFWy5k5tfkkGbSVIFiO5kXYmMpH5kiLdq6A-kRZRhB5SZkStGWOfGdPASCwPFAdZo31b-meIAsjRBE5NomERHTcLX3z4hQgU9biXrx6E2Lfqv4EPk3kRVDjXdv71NLTWRK7LAsquZk63HcieJU-d-Lz-SFGfKjGazc5-fW2hOOyW2JMaeRTzeglx2K-MqbrFAxrcFi5qqtIXY-9RCSMTgC8wp04kwdpe4eO1_BpVHvaF8wRF8ohfK0TG6LfZ0ZMI5HsLF51CWfZU3XoNGGBmd0YaH7RREPB6HKHZLc9m1hxHHehJy3wIoRnpVDOHDh2WEpiq3k43Snt2NuZScOajMuNkTUn709AXxiyCjC5OnpSXAYI3zPfDJhFInrAcsg_580MRO7iK2gnQbTPXfvSMheglqH7W7kCy4jhBOESfu9zjG-FosrpRtg-051JIMYqKwbuA8_ml39gIspZShADon7G55n91sz0yGucMqXWwIefTXFXL2gFnh_C2ho3ZhC3OsraU7h3dU2egiik1pZQniwrXH647ZhdInoygvVkovPbEutaaQTNwAEphQCzWhNFOBbImB-HCAi2cLamsAJyI1r3LUe6G3t0UEltLDZ2dFZgCps0IJ3bAaNwajHYu9GZREj4YXWvfkEa60Sdo8hBEWWGEHXYqs4I8L4JRq7lLEFohU5wLXHan_xL2dLE7_xHr7_FoFpGi8X41NVC5kEXHvnYMPPGxhUuiuxQnQNCb4rrqEl9gsvBnxNDVMiReakb2ptbcHHGJA12TZFnx97eNcZamTbk5PrDGcAMwpGqHTZenb_29RM-cGZSzoLLbezxm-B0My1BLmHBXjEL1rMJP3C6XUYYmzFdv3oUXTWB8AY4dbMKbwebbGLR6j1g7iKoBZeg'
dbx = dropbox.Dropbox(access_token)

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
        root.errors.append(node.path)
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





errorlist = []
root = create_tree('/CEG 1 - All Lab Members')
root.print_tree()
print(errorlist)
''' download function
download_path = "\\\\lsa-rosati-win.turbo.storage.umich.edu\lsa-rosati\Google-Drive-Backup\\"  
final_path = download_path + date.now().strftime("%Y") + "\\" + date.now().strftime("%B %Y")
root.download_files(dbx,final_path)
'''