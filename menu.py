import dropbox
from rich.prompt import Prompt
from rich import print

import tkinter as tk
from tkinter import filedialog

class UserInputField:
    def __init__(self, root, label_text, example_text, save_variable,execute_function=None):
        self.label_text = label_text
        self.example_text = example_text
        self.save_variable = save_variable
        self.execute_function = execute_function

        self.frame = tk.Frame(root)
        self.frame.pack(side=tk.TOP, pady=10)

        self.label = tk.Label(self.frame, text=f"{self.label_text}:")
        self.label.pack(side=tk.LEFT, padx=10)

        self.entry = tk.Entry(self.frame, width=30)
        self.entry.insert(0, self.example_text)
        self.entry.pack(side=tk.LEFT, padx=10)

        # When the entry field is clicked, remove the example text
        self.entry.bind("<FocusIn>", self.on_entry_click)

        self.submit_button = tk.Button(self.frame, text="Submit", command=self.save_input)
        self.submit_button.pack(side=tk.LEFT, padx=10)
        # Optionally create a button to execute the function
        if self.execute_function is not None:
            self.execute_button = tk.Button(
                self.frame, 
                text="Verify", 
                command=self.execute_and_save_input
            )
            self.execute_button.pack(side=tk.LEFT, padx=10)

    def on_entry_click(self, event):
        if self.entry.get() == self.example_text:
            self.entry.delete(0, tk.END)

    def save_input(self):
        # Get the value from the entry field and save to the specified variable
        user_input = self.entry.get().strip()
        self.save_variable.set(user_input)
        print(f"{self.label_text} Input: {user_input}")

    def execute_and_save_input(self):
        # Save the input to the variable
        self.save_input()
        # Then execute the function with the input
        self.execute_function(self.save_variable.get())

class PathSelector:
    def __init__(self, root, label_text, save_variable, select_file=False, filetypes=[("Text files", "*.txt"), ("All files", "*.*")], execute_function=None):
        self.label_text = label_text
        self.save_variable = save_variable
        self.select_file = select_file
        self.filetypes = filetypes
        self.execute_function = execute_function

        self.frame = tk.Frame(root)
        self.frame.pack(side=tk.TOP, pady=10)

        self.label = tk.Label(self.frame, text=f"{self.label_text}: Not Selected")
        self.label.pack(side=tk.LEFT, padx=10)

        self.select_button_text = "Select File" if self.select_file else "Select Folder"
        self.select_button = tk.Button(self.frame, text=self.select_button_text, command=self.select_path)
        self.select_button.pack(side=tk.LEFT, padx=10)

        self.execute_button = tk.Button(self.frame, text="Execute", command=self.execute_function) if self.execute_function else None
        if self.execute_button:
            self.execute_button.pack(side=tk.LEFT, padx=10)

    def select_path(self):
        # Configure filetypes for file selection
        if self.select_file and self.filetypes:
            filetypes = self.filetypes
        else:
            filetypes = ()

        # Open a file dialog for the user to select a file or directory
        selected_path = filedialog.askopenfilename(filetypes=filetypes) if self.select_file else filedialog.askdirectory()

        # Check if a file or directory was selected
        if selected_path:
            # Update the label with the selected path
            self.label.config(text=f"{self.label_text}: {selected_path}")

            # Save the path to the specified variable
            self.save_variable[0] = selected_path
            #setattr(self.save_variable, 'value', selected_path)
            print(f"{self.label_text} Path: {selected_path}")

def verify_and_run(*args):
    json_tree = json_loader.save_variable[0]
    download_location = loc_loader.save_variable[0]
    access_token = api_entry.save_variable.get()
    user_input2 = entry2.save_variable.get()

    print(f"User Input 1: {access_token}")
    print(f"User Input 2: {user_input2}")
    print(f"Path 1: {json_tree}")
    print(f"Path 2: {download_location}")

    # If user has entered input and selected paths
    if all([access_token, user_input2, download_location]):
        # Close the window
        root.destroy()

        # Run your custom function
        custom_function()
    else:
        # Show an error message
        tk.messagebox.showerror("Error", "Please select download paths and enter user inputs.")

def custom_function():
    # Replace this with your actual function logic
    print("Running custom function!")

def authenticate(access_token):
    try:
        dbx = dropbox.Dropbox(access_token)
        account_info = dbx.users_get_current_account()
        user_name = account_info.name.display_name
        tk.messagebox.showinfo("User Authenticated", f"Welcome {user_name}.")
    except dropbox.exceptions.AuthError as e:
        tk.messagebox.showerror("Error", f"Authentication error: Bad or expried token.\nPlease generate a new token or try again.")
    except dropbox.exceptions.InternalServerError as e:
        tk.messagebox.showerror("Error", f"Server Error: Check Dropbox status or try again shortly")

        return None

    

# Create the main window
root = tk.Tk()
root.title("Download Path Selector")

# Calculate the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set the window size and position it at the center
window_width = 500
window_height = 300
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2

root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# Placeholder variables for entry input
access_token = tk.StringVar()
user_input2 = tk.StringVar()

# Placeholder variables for file paths
json_tree = [""]
download_location = [""]

# Create instances of the UserInputField class
json_loader = PathSelector(root, "(optional) Load File Tree .json File", json_tree,select_file=True,filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
api_entry = UserInputField(root, "Dropbox API Token", "Paste Access Token Here", access_token,authenticate)

entry2 = UserInputField(root, "User Input 2", "Enter your input here", user_input2) # Dropbox path

# Create instances of the PathSelector class for download paths

loc_loader = PathSelector(root, "Download Path 2", download_location)

# Create a frame for the verification and run button
frame_bottom = tk.Frame(root)
frame_bottom.pack(side=tk.BOTTOM, pady=20)

# Create and pack a button to verify and run the function
verify_run_button = tk.Button(frame_bottom, text="Verify and Run", command=verify_and_run)
verify_run_button.pack()

# Run the main event loop
root.mainloop()





'''
def get_user_name(access_token):
    try:
        dbx = dropbox.Dropbox(access_token)
        account_info = dbx.users_get_current_account()
        user_name = account_info.name.display_name
        return user_name
    except dropbox.exceptions.AuthError as e:
        tk.messagebox.showerror("Error", f"Authentication error: {e}.\nPlease generate a new API token or try again.")

        return None
def authenticate(access_token):
    tk.messagebox.showinfo("User Authenticated", f"Welcome {user_name}.") if user_name = get_user_name(access_token) else None


# Get the user's name
authenticate(access_token)
user_name = get_user_name(access_token)

if user_name is not None:
    print(f"The user's name is: {user_name}")
else:
    print("Failed to retrieve user name.")

'''

