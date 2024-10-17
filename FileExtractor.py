import tkinter as tk
from tkinter import filedialog
from datetime import datetime

def get_current_timestamp():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def select_source_folder():
    """Original functionality for selecting the source folder."""
    folder = filedialog.askdirectory()
    if folder:
        source_folder.set(folder)
        source_label.config(text=folder)
    else:
        source_label.config(text="No folder selected")

def select_target_folder():
    """Original functionality for selecting the target folder."""
    folder = filedialog.askdirectory()
    if folder:
        target_folder.set(folder)
        target_label.config(text=folder)
    else:
        target_label.config(text="No folder selected")

def set_extract_zips_function(func):
    """Set the function for the 'Extract Zips' button."""
    global extract_zips_function
    extract_zips_function = func

def set_extract_files_function(func):
    """Set the function for the 'Extract Files' button."""
    global extract_files_function
    extract_files_function = func

def set_extract_files_from_zips_function(func):
    """Set the function for the 'Extract Files from Zips' button."""
    global extract_files_from_zips_function
    extract_files_from_zips_function = func

def add_to_log(msg):
    """Add a message to the log."""
    log_text.config(state=tk.NORMAL)  # Enable editing
    log_text.insert(tk.END, f"[{get_current_timestamp()}] {msg}\n")  # Add message to the end of the log
    log_text.yview(tk.END)  # Scroll to the latest entry
    log_text.config(state=tk.DISABLED)  # Disable editing

def show_error_message(msg):
    """Display an error message in the message label."""
    message_label.config(text=msg, fg="red")
    add_to_log(f"Error: {msg}")

def show_success_message(msg):
    """Display a success message in the message label."""
    message_label.config(text=msg, fg="green")
    add_to_log(f"Success: {msg}")

def show_message(msg):
    message_label.config(text=msg, fg="black")

def try_except_wrapper(func):
    def wrappedFunc():
        try:
            func()
            show_success_message("Success")
        except:
            show_error_message("Error")
    return wrappedFunc

# Placeholder functions for buttons
def extract_zips():
    if extract_zips_function:
        extract_zips_function()

def extract_files():
    if extract_files_function:
        extract_files_function()

def extract_files_from_zips():
    if extract_files_from_zips_function:
        extract_files_from_zips_function()

# Initialize placeholder functions
extract_zips_function = None
extract_files_function = None
extract_files_from_zips_function = None
source_label = None
target_label = None
message_label = None
extension_entry = None

# Define some global variables
source_folder = None
target_folder = None
log_text = None

def showUI():
    # Create the main window
    root = tk.Tk()
    root.title("File Extractor")
    root.geometry("600x500")  # Adjusted for extra space for the log box

    # Set the window icon (.ico file)
    try:
        root.iconbitmap("favicon.ico")
    except:
        pass

    # Apply a professional style to the window
    root.configure(bg="#e6e6e6")

    # Define font styles
    label_font = ("Helvetica", 10)
    button_font = ("Helvetica", 10, "bold")

    # Create StringVars to store source and target folder paths
    global extract_zips_function
    global extract_files_function
    global extract_files_from_zips_function
    global source_folder
    global target_folder
    global source_label
    global target_label
    global message_label
    global log_text
    global extension_entry
    source_folder = tk.StringVar()
    target_folder = tk.StringVar()

    # Frame for organizing layout
    source_frame = tk.Frame(root, bg="#e6e6e6")
    target_frame = tk.Frame(root, bg="#e6e6e6")
    extension_frame = tk.Frame(root, bg="#e6e6e6")
    button_frame = tk.Frame(root, bg="#e6e6e6")
    message_frame = tk.Frame(root, bg="#e6e6e6")

    # Create the UI elements
    source_button = tk.Button(source_frame, text="Select Source Folder", font=button_font, command=select_source_folder, bg="#d9d9d9", fg="black", padx=10, pady=5, bd=1, relief="solid")
    source_label = tk.Label(source_frame, text="No folder selected", font=label_font, bg="#e6e6e6", anchor="w", wraplength=300)

    target_button = tk.Button(target_frame, text="Select Target Folder", font=button_font, command=select_target_folder, bg="#d9d9d9", fg="black", padx=10, pady=5, bd=1, relief="solid")
    target_label = tk.Label(target_frame, text="No folder selected", font=label_font, bg="#e6e6e6", anchor="w", wraplength=300)

    extension_label = tk.Label(extension_frame, text="File Extensions (e.g. wav, mp3, jpg):", font=label_font, bg="#e6e6e6")
    extension_entry = tk.Entry(extension_frame, font=label_font)

    extract_zips_button = tk.Button(button_frame, text="Extract Compressed Files", font=button_font, command=extract_zips, bg="#f0f0f0", fg="black", padx=10, pady=5, bd=1, relief="solid")
    extract_files_button = tk.Button(button_frame, text="Extract Files by Extensions", font=button_font, command=extract_files, bg="#f0f0f0", fg="black", padx=10, pady=5, bd=1, relief="solid")
    extract_files_from_zips_button = tk.Button(button_frame, text="Extract Files by Extensions from Compressed Files", font=button_font, command=extract_files_from_zips, bg="#f0f0f0", fg="black", padx=10, pady=5, bd=1, relief="solid")

    # Error/Success message label
    message_label = tk.Label(message_frame, text="", fg="red", font=label_font, bg="#e6e6e6", wraplength=450)

    # Log box and header
    log_header_label = tk.Label(root, text="Log", font=("Helvetica", 10), bg="#e6e6e6", anchor="w")  # Removed bold style
    log_frame = tk.Frame(root, bg="#e6e6e6")
    log_text = tk.Text(log_frame, height=10, state=tk.DISABLED, wrap=tk.WORD, font=label_font)
    log_scrollbar = tk.Scrollbar(log_frame, command=log_text.yview)
    log_text.config(yscrollcommand=log_scrollbar.set)

    # Layout the UI elements in a grid
    source_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")
    source_button.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    source_label.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

    target_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")
    target_button.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    target_label.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

    extension_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")
    extension_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    extension_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

    button_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")
    extract_zips_button.grid(row=0, column=0, padx=10, pady=5, sticky="ew")
    extract_files_button.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
    extract_files_from_zips_button.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

    message_frame.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")
    message_label.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

    # Log header and box
    log_header_label.grid(row=5, column=0, columnspan=2, padx=10, pady=5, sticky="w")
    log_frame.grid(row=6, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")
    log_scrollbar.grid(row=0, column=1, sticky="ns")
    log_text.grid(row=0, column=0, sticky="nsew")

    # Make the rows and columns resize dynamically
    root.columnconfigure(0, weight=1)
    root.rowconfigure(6, weight=1)  # Log Frame

    # Ensure elements inside frames scale correctly
    source_frame.columnconfigure(1, weight=1)
    target_frame.columnconfigure(1, weight=1)
    extension_frame.columnconfigure(1, weight=1)
    button_frame.columnconfigure(0, weight=1)
    button_frame.columnconfigure(1, weight=1)
    message_frame.columnconfigure(0, weight=1)
    log_frame.columnconfigure(0, weight=1)
    
    # Run the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    showUI()