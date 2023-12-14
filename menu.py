import dropbox
from rich.prompt import Prompt
from rich import print

import tkinter as tk
from tkinter import filedialog

class UserInputField:
    def __init__(self, root, label_text, example_text, save_variable):
        self.label_text = label_text
        self.example_text = example_text
        self.save_variable = save_variable

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

    def on_entry_click(self, event):
        if self.entry.get() == self.example_text:
            self.entry.delete(0, tk.END)

    def save_input(self):
        # Get the value from the entry field and save to the specified variable
        user_input = self.entry.get().strip()
        self.save_variable.set(user_input)
        print(f"{self.label_text} Input: {user_input}")

class PathSelector:
    def __init__(self, root, label_text, save_variable, select_file=False, filetypes=None, execute_function=None):
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
    selected_path1 = path1.save_variable[0]
    selected_path2 = path2.save_variable[0]
    user_input1 = entry1.save_variable.get()
    user_input2 = entry2.save_variable.get()

    print(f"User Input 1: {user_input1}")
    print(f"User Input 2: {user_input2}")
    print(f"Path 1: {selected_path1}")
    print(f"Path 2: {selected_path2}")

    # If user has entered input and selected paths
    if all([user_input1, user_input2, selected_path1, selected_path2]):
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
user_input1 = tk.StringVar()
user_input2 = tk.StringVar()

# Placeholder variables for file paths
selected_path1 = [""]
selected_path2 = [""]

# Create instances of the UserInputField class
entry1 = UserInputField(root, "User Input 1", "Enter your input here", user_input1)
entry2 = UserInputField(root, "User Input 2", "Enter your input here", user_input2)

# Create instances of the PathSelector class for download paths
path1 = PathSelector(root, "Download Path 1", selected_path1)
path2 = PathSelector(root, "Download Path 2", selected_path2, select_file=True, execute_function=custom_function)

# Create a frame for the verification and run button
frame_bottom = tk.Frame(root)
frame_bottom.pack(side=tk.BOTTOM, pady=20)

# Create and pack a button to verify and run the function
verify_run_button = tk.Button(frame_bottom, text="Verify and Run", command=verify_and_run)
verify_run_button.pack()

# Run the main event loop
root.mainloop()



access_token = None

def authenticate(access_token):
    if access_token == None:
        print("To use this program, you will need to generate a DropBox API Token")
    print("Navigate to https://dropbox.github.io/dropbox-api-v2-explorer/#file_requests_get \nand click 'Get Token.'\nCopy the 'Access Token' field here.")
    access_token = Prompt.ask(prompt='Paste your access token here: ', console=console)
    print(access_token)
    return(access_token)
def get_user_name(access_token):
    try:
        dbx = dropbox.Dropbox(access_token)
        account_info = dbx.users_get_current_account()
        user_name = account_info.name.display_name
        return user_name
    except dropbox.exceptions.AuthError as e:
        print(f"Authentication error: {e}.\nPlease generate a new API token.")

        return None



# Get the user's name
authenticate(access_token)
user_name = get_user_name(access_token)

if user_name is not None:
    print(f"The user's name is: {user_name}")
else:
    print("Failed to retrieve user name.")



