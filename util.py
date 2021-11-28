import tkinter as tk
from tkinter import ttk, filedialog
from ttkthemes import ThemedTk
from os import path
from PyPDF2 import PdfFileMerger, PdfFileReader

import glob

###################################################################################
def add_files_to_listbox(listbox, files):
    for file in files:
        listbox.insert(tk.END, file)


def delete_files_from_listbox(listbox, lo, hi):
    listbox.delete(lo, hi)


def browse_button():
    global chosen_directory_textbox, directory_files_listbox, directory_files
    dir = filedialog.askdirectory()

    # Update the chosen directory
    chosen_directory_textbox.config(state="normal")
    chosen_directory_textbox.delete("1.0", tk.END)
    chosen_directory_textbox.insert("1.0", dir)
    chosen_directory_textbox.config(state="disabled")

    # Get the files that are in the chosen directory and show them
    pdf_files = glob.glob(dir + "/*.pdf")
    pdf_files = [file_path.split("\\")[1] for file_path in pdf_files]
    add_files_to_listbox(directory_files_listbox, pdf_files)

    # Update the list that holds the directories files
    directory_files = pdf_files


def move_up():
    global directory_files_listbox, selected_files_listbox, directory_files, selected_files

    # Get the indexes of the selected items
    selected_elements = selected_files_listbox.curselection()
    if len(selected_elements) == 0:
        return

    # remove the selected items from the directory_files
    sfs = []
    for i in range(0, selected_files_listbox.size()):
        if i not in selected_elements:
            # Non-selected elements should remain in the directory files list
            sfs.append(selected_files_listbox.get(i))
        else:
            # Selected elements should be added to the selected files list
            directory_files.append(selected_files_listbox.get(i))
    selected_files = sfs

    # Update the directory files listbox
    delete_files_from_listbox(directory_files_listbox, 0, tk.END)
    add_files_to_listbox(directory_files_listbox, directory_files)

    # Update the selected files listbox
    delete_files_from_listbox(selected_files_listbox, 0, tk.END)
    add_files_to_listbox(selected_files_listbox, selected_files)


def move_down():
    global directory_files_listbox, selected_files_listbox, directory_files, selected_files

    # Get the indexes of the selected items
    selected_elements = directory_files_listbox.curselection()
    if len(selected_elements) == 0:
        return

    # remove the selected items from the directory_files
    dfs = []
    for i in range(0, directory_files_listbox.size()):
        if i not in selected_elements:
            # Non-selected elements should remain in the directory files list
            dfs.append(directory_files_listbox.get(i))
        else:
            # Selected elements should be added to the selected files list
            selected_files.append(directory_files_listbox.get(i))
    directory_files = dfs

    # Update the directory files listbox
    delete_files_from_listbox(directory_files_listbox, 0, tk.END)
    add_files_to_listbox(directory_files_listbox, directory_files)

    # Update the selected files listbox
    delete_files_from_listbox(selected_files_listbox, 0, tk.END)
    add_files_to_listbox(selected_files_listbox, selected_files)


def merge_selected_files():
    global merge_state_label_text

    file_merger = PdfFileMerger()
    dir = chosen_directory_textbox.get("1.0", tk.END)[:-1]
    if not path.isdir(dir):
        return

    for file in selected_files:
        file_merger.append(PdfFileReader(dir + "\\" + file), "rb")

    # Merge the PDF-files
    merged_files = glob.glob("output\\*.pdf")
    file_merger.write("output\\NewMergedFile" + str(len(merged_files) + 1) + ".pdf")
    if path.isfile("output\\NewMergedFile" + str(len(merged_files) + 1) + ".pdf"):
        merge_state_label_text.set("Successfully merged PDF-files!")
    else:
        merge_state_label_text.set("Something went wrong...")
    merge_state_label.grid()


###################################################################################

# Create the GUI
root = ThemedTk(theme="yaru")
root.title("PDF Utility")
root.resizable(0, 0)
root_frame = ttk.Frame(root, padding=10)
root_frame.grid()

###################################################################################

# Chosen directory and browse
chosen_directory_label = ttk.Label(root_frame, text="Chosen directory")
chosen_directory_label.grid(column=0, row=0, sticky="W", pady=1)

chosen_directory_textbox = tk.Text(root_frame, state="disabled", height=1)
chosen_directory_textbox.grid(
    column=0, row=1, columnspan=3, sticky="W", pady=5, ipadx=3, ipady=3
)

browse_btn = ttk.Button(root_frame, text="Browse", command=browse_button)
browse_btn.grid(column=3, row=1, sticky="E")

###################################################################################

# Directory files
directory_files_label = ttk.Label(root_frame, text="Directory files")
directory_files_label.grid(column=0, row=2, sticky="W", pady=1)

dir_files_frame = tk.Frame(root_frame)
dir_files_frame.grid(column=0, row=3, columnspan=4, sticky="EW", pady=10)
dir_files_frame.columnconfigure(0, weight=1)

scrollbar_1 = tk.Scrollbar(dir_files_frame, orient="vertical")
scrollbar_1.grid(column=1, row=3, sticky="ns")

directory_files_listbox = tk.Listbox(
    dir_files_frame,
    height=15,
    activestyle="none",
    selectmode="extended",
    yscrollcommand=scrollbar_1.set,
)
directory_files_listbox.grid(column=0, row=3, sticky="EW")

scrollbar_1.config(command=directory_files_listbox.yview)

###################################################################################

# Selected files
selected_files_label = ttk.Label(root_frame, text="Selected files")
selected_files_label.grid(column=0, row=4, sticky="W", pady=1)

# Options for selected files
up_btn = ttk.Button(root_frame, text="Up", command=move_up)
up_btn.grid(column=2, row=4, sticky="E")

down_btn = ttk.Button(root_frame, text="Down", command=move_down)
down_btn.grid(column=3, row=4, sticky="E")

# Display for the selected files
selected_files_frame = tk.Frame(root_frame)
selected_files_frame.grid(column=0, row=5, columnspan=4, sticky="EW", pady=10)
selected_files_frame.columnconfigure(0, weight=1)

scrollbar_2 = tk.Scrollbar(selected_files_frame, orient="vertical")
scrollbar_2.grid(column=1, row=5, sticky="ns")

selected_files_listbox = tk.Listbox(
    selected_files_frame,
    height=15,
    activestyle="none",
    selectmode="extended",
    yscrollcommand=scrollbar_2.set,
)
selected_files_listbox.grid(column=0, row=5, sticky="EW")

scrollbar_2.config(command=selected_files_listbox.yview)

###################################################################################

# Options regarding what one wants to do with the selected files (eg. merge, split)
buttons_frame = ttk.Frame(root_frame)
buttons_frame.grid(column=0, row=6, sticky="W")

# Merge button
merge_btn = ttk.Button(buttons_frame, text="Merge", command=merge_selected_files)
merge_btn.grid(column=0, row=6, sticky="W")

merge_state_label_text = tk.StringVar()
merge_state_label = tk.Label(buttons_frame, textvariable=merge_state_label_text)
merge_state_label.grid(column=1, row=6, sticky="W")
merge_state_label.grid_remove()

# Split button
# merge_btn = ttk.Button(buttons_frame, text="Split", command=None)
# merge_btn.grid(column=1, row=6, sticky="W")

# Close button
close_btn = ttk.Button(root_frame, text="Close", command=root.destroy)
close_btn.grid(column=3, row=6)

directory_files = []
selected_files = []

root.mainloop()
