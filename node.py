import dropboxtree as tree
from dropboxtree import dbx
from datetime import datetime as date

# Create tree block
#root = create_tree('/WLMS & Izzy Build Steps')
#root = create_tree('/CEG 1 - All Lab Members')


# Tree load block
root,errorlist = tree.load_tree_from_file("CEG_1.json")
#root.print_tree()
#print(f" Errors {errorlist}")


#download block
download_path = "\\\\lsa-rosati-win.turbo.storage.umich.edu\lsa-rosati\Google-Drive-Backup\\"  
final_path = download_path + date.now().strftime("%Y") + "\\" + date.now().strftime("%B %Y")
root.download_files(dbx,final_path)

### TODO - import rich to improve readability of console output. Use rich to create download bars. Multi-thread downloads. queue for .zips vs files? 
# separate Download function from Tree class. 
#  If connection error, delete most recent download, retry after x
# implement expotential back off:

# Make a request to the API
# Receive an error response that has a retry-able error code
# Wait 1s + random_number_milliseconds seconds
# Retry request
# Receive an error response that has a retry-able error code
# Wait 2s + random_number_milliseconds seconds
# Retry request
# Receive an error response that has a retry-able error code
# Wait 4s + random_number_milliseconds seconds
# Retry request
# Receive an error response that has a retry-able error code
# Wait 8s + random_number_milliseconds seconds
# Retry request
# Receive an error response that has a retry-able error code
# Wait 16s + random_number_milliseconds seconds
# Retry request
# If you still get an error, stop and log the error.
