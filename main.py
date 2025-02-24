# import tkinter as tk
import os
import glob
import filecmp, shutil, time

# from tkinterdnd2 import DND_FILES, TkinterDnD

# root = TkinterDnD.Tk()  # notice - use this instead of tk.Tk()

# lb = tk.Listbox(root, width=100)
# lb.insert(1, "drag files to here")

# # register the listbox as a drop target
# lb.drop_target_register(DND_FILES)
# lb.dnd_bind('<<Drop>>', lambda e: lb.insert(tk.END, e.data))

# lb.pack()
# root.mainloop()

def get_files_recursively(path):
    files = glob.glob(path + '/**/*', recursive=True, include_hidden=True)
    files = [os.path.relpath(file, start=path).replace('\\', '/') for file in files]
    return files

initial_timestamp = 0

def start_timer():
    global initial_timestamp 
    initial_timestamp = time.time()

def end_timer(text=""):
    global initial_timestamp 
    execution_time = time.time() - initial_timestamp
    print(f"{execution_time:.2f}s {text}")

def get_size(path, get_in_Bytes=False):
    """
    Get the total size of all files in given path.

    Args:
        path (str): Path to the directory to get the size of.
        get_in_Bytes (bool, optional): If True, return size in bytes, else return in human readable format. Defaults to False.

    Returns:
        str: The size of the given path in bytes or human readable format.
    """
    try:
        size = 0
        if os.path.isfile(path):
            size = os.path.getsize(path)
        elif os.path.isdir(path):
            for dirpath, dirnames, filenames in os.walk(path):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    # skip if it is symbolic link
                    if not os.path.islink(fp):
                        size += os.path.getsize(fp)

        if get_in_Bytes:
            return f"{size} Bytes"

        for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
            if size < 1024.0:
                return f"{size:.2f} {unit}B"
            size /= 1024.0
    except PermissionError as e:
        print(f"PermissionError: {e}")
        return "N/A"

src_path = 'C:/Users/Liju/Desktop/Folder Sync/des3'
dest_path = 'C:/Users/Liju/Desktop/Folder Sync/des'
files_copied, files_deleted = [0] * 2

start_timer()
src_files = get_files_recursively(src_path)
end_timer(f"To read {format(len(src_files), ',')} source items")

start_timer()
dest_files = get_files_recursively(dest_path)
end_timer(f"To read {format(len(dest_files), ',')} destination items")

while 0 < len(src_files):
    file = src_files[0]
    src_file = src_path + '/' + file
    dest_file = dest_path + '/' + file

    
    start_timer()
    if file not in dest_files:
        if os.path.isfile(src_file):
            shutil.copy(src_file, dest_file)
        elif os.path.isdir(src_file):
            shutil.copytree(src_file, dest_file)
            src_files = [other_file for other_file in src_files if not other_file.startswith(file + '/')]
        src_files.pop(0)
        files_copied += 1
    else:
        src_files.pop(0)
        dest_files.remove(file)

        if os.path.isdir(src_file):
            continue

        if filecmp.cmp(src_file, dest_file, shallow=True):
            continue
        else:
            if os.path.isfile(src_file):
                shutil.copy(src_file, dest_file)
            if os.path.isdir(src_file):
                shutil.copytree(src_file, dest_file)
            files_copied += 1
    end_timer(f"To copy \t- {get_size(src_file)} \t-  {len(src_files)} Files Remaining \t- /{file}")

# Delete files from destination that are not in source
files_deleted = len(dest_files)
while 0 < len(dest_files):
    dest_file = dest_path + '/' + dest_files[0]
    os.chmod(dest_file, 0o666)  # Change permission to delete
    file_size = get_size(dest_file)
    
    start_timer()
    if os.path.isfile(dest_file):
        os.remove(dest_file)
    elif os.path.isdir(dest_file):
        shutil.rmtree(dest_file)
        dest_files = [file_to_keep for file_to_keep in dest_files if not file_to_keep.startswith(dest_files[0] + '/')]
    end_timer(f"To delete \t- {file_size} \t- {len(dest_files)} Files Remaining \t- /{dest_files[0]}")
    dest_files.remove(dest_files[0])

print(f"\n\033[92m{format(files_copied, ',')}\033[0m Items copied\n\033[91m{format(files_deleted, ',')}\033[0m Items deleted From Destination\n Done")

# Check if the size of source and destination are same
if get_size(src_path, get_in_Bytes=True) != get_size(dest_path, get_in_Bytes=True):
    print("\n\033[91m Something went wrong\033[0m")
else:
    print("\n All files are in sync")

