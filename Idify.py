import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
from PIL import Image, ImageTk
import random
import string

def generate_random_string():
    charset = string.ascii_letters + string.digits + "!@#$%^&*()-_=+[{]}\\|:;\"'<,>.?/"

    # Check the length toggle in the Advanced window
    length = closest_number(string_length.get(), 3, 30) if length_toggle_var.get() else string_length.get()

    random_string = ''.join(random.choice(charset) for _ in range(length))
    result_var.set(random_string)
    center_string()

def regenerate_string(event=None):  # Accepts an event argument for binding
    generate_random_string()

def center_string():
    # Center the string horizontally in the label
    result_label.update_idletasks()
    label_width = result_label.winfo_width()
    text_width = lexend_font.measure(result_var.get())
    padding = (label_width - text_width) // 2
    result_label.configure(padding=(padding, 10))

    # Wrap text onto multiple lines if it exceeds a certain length
    max_chars_per_line = 25
    text = result_var.get()
    wrapped_text = '\n'.join([text[i:i + max_chars_per_line] for i in range(0, len(text), max_chars_per_line)])
    result_var.set(wrapped_text)

def closest_number(value, min_val, max_val):
    # Ensure the value is within the specified range
    value = max(min(value, max_val), min_val)
    # Find the closest number between min_val and max_val
    return min(max_val, max(min_val, value))

def copy_to_clipboard():
    root.clipboard_clear()
    root.clipboard_append(result_var.get())
    root.update()

def update_font_size(event):
    # Update font size based on the window width
    new_font_size = max(int(event.width / 25), 8)  # Adjust the divisor and minimum font size as needed
    lexend_font.configure(size=new_font_size)
    regenerate_button.configure(font=('Lexend', max(int(new_font_size / 1.5), 8)))
    copy_button.configure(font=('Lexend', max(int(new_font_size / 1.5), 8)))
    advanced_button.configure(font=('Lexend', max(int(new_font_size / 1.5), 8)))  # Adjust the divisor as needed

# Create the main window
root = tk.Tk()
root.title("Idify")

# Create and set the result variable
result_var = tk.StringVar()

# Load the "Lexend" font
initial_font_size = 14
lexend_font = tkfont.Font(family='Lexend', size=initial_font_size)

# Create and configure the label to display the random string with the "Lexend" font
result_label = ttk.Label(root, textvariable=result_var, font=lexend_font, padding=(10, 10))
result_label.grid(row=0, column=0, columnspan=2, sticky="nsew")

# Create the "Regenerate String" button with the "Lexend" font
regenerate_button = ttk.Button(root, text="Regenerate String", command=regenerate_string)
regenerate_button.grid(row=1, column=0, columnspan=2, pady=(0, 5), sticky="nsew")

# Create a seed variable
seed_var = tk.IntVar()

# Create the length entry field
string_length = tk.IntVar()
length_entry = ttk.Entry(root, textvariable=string_length, font=('Lexend', max(int(initial_font_size / 1.5), 8)), width=5)
length_entry.grid(row=2, column=0, columnspan=2, pady=(0, 5), sticky="nsew")

# Create the "Copy to Clipboard" button
copy_button = ttk.Button(root, text="Copy to Clipboard", command=copy_to_clipboard)
copy_button.grid(row=3, column=0, columnspan=2, pady=(0, 5), sticky="nsew")

# Create the "Advanced" button with the "Lexend" font
advanced_button = ttk.Button(root, text="Advanced", command=lambda: open_advanced_window())
advanced_button.grid(row=4, column=0, columnspan=2, pady=(0, 5), sticky="nsew")

# Create a toggle variable for the length restriction
length_toggle_var = tk.BooleanVar()
length_toggle_var.set(True)  # Set to True to enable length restriction on startup

# Create a label for the toggle status
toggle_label = ttk.Label(root, text="Length Restriction: ON", font=('Lexend', max(int(initial_font_size / 1.8), 8)))
toggle_label.grid(row=5, column=0, columnspan=2, pady=(0, 5), sticky="nsew")

# Configure row and column weights to make them expand with the window
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_rowconfigure(4, weight=1)
root.grid_rowconfigure(5, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Bind the font size update to window resizing
root.bind("<Configure>", update_font_size)

# Initial string generation
generate_random_string()

# Function to open the Advanced window
def open_advanced_window():
    advanced_window = tk.Toplevel(root)
    advanced_window.title("Advanced Settings")
    advanced_window.resizable(False, False)

    seed_label = ttk.Label(advanced_window, text="Seed:")
    seed_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")

    seed_entry = ttk.Entry(advanced_window, textvariable=seed_var, font=('Lexend', max(int(initial_font_size / 1.5), 8)))
    seed_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

    toggle_frame = ttk.Frame(advanced_window)
    toggle_frame.grid(row=1, column=0, columnspan=2, pady=(5, 10), sticky="nsew")

    length_toggle_button = ttk.Checkbutton(toggle_frame, text="Toggle Length Restriction", variable=length_toggle_var, command=update_toggle_label)
    length_toggle_button.grid(row=0, column=0, pady=5)

    ok_button = ttk.Button(advanced_window, text="OK", command=advanced_window.destroy)
    ok_button.grid(row=2, column=0, columnspan=2, pady=(5, 10), sticky="nsew")

def update_toggle_label():
    toggle_label.config(text=f"Length Restriction: {'ON' if length_toggle_var.get() else 'OFF'}")
    generate_random_string()  # Regenerate string when the toggle changes

# Run the Tkinter event loop
root.mainloop()
