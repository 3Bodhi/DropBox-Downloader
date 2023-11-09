import dropboxtree as tree
from dropboxtree import dbx
from datetime import datetime as date

root,errorlist = tree.load_tree_from_file("CEG_1.json")
#root.print_tree()
#print(f" Errors {errorlist}")


#download function
download_path = "\\\\lsa-rosati-win.turbo.storage.umich.edu\lsa-rosati\Google-Drive-Backup\\"  
final_path = download_path + date.now().strftime("%Y") + "\\" + date.now().strftime("%B %Y")
root.download_files(dbx,final_path)


