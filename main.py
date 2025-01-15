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
    print(f"{execution_time:.3f}s {text}")

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

start_timer()
src_files = get_files_recursively(src_path)
end_timer("To read source files")

start_timer()
dest_files = get_files_recursively(dest_path)
end_timer("To read destination files")

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
    else:
        dest_files.remove(file)
        src_files.pop(0)

        if os.path.isdir(src_file):
            continue

        if filecmp.cmp(src_file, dest_file, shallow=True):
            continue
        else:
            if os.path.isfile(src_file):
                shutil.copy(src_file, dest_file)
            if os.path.isdir(src_file):
                shutil.copytree(src_file, dest_file)
    end_timer(f"To copy \t- {get_size(src_file)} \t-  {len(src_files)} Files Remaining \t- /{file}")

while 0 < len(dest_files):
    dest_file = dest_path + '/' + dest_files[0]
    os.chmod(dest_file, 0o666)
    file_size = get_size(dest_file)
    
    start_timer()
    if os.path.isfile(dest_file):
        os.remove(dest_file)
    elif os.path.isdir(dest_file):
        shutil.rmtree(dest_file)
        dest_files = [file_to_keep for file_to_keep in dest_files if not file_to_keep.startswith(dest_files[0] + '/')]
    end_timer(f"To delete \t- {file_size} \t- {len(dest_files)} Files Remaining \t- /{dest_files[0]}")
    dest_files.remove(dest_files[0])

print("Done")


# file_paths = glob.glob(src_path + '/**/*', recursive=True)


# print(filecmp.DEFAULT_IGNORES)
# def print_diff_files(dcmp):
#     for name in dcmp.diff_files:
#         print("diff_file %s found in %s and %s" % (name, dcmp.left,
#               dcmp.right))
#     for sub_dcmp in dcmp.subdirs.values():
#         print_diff_files(sub_dcmp)

# dcmp = filecmp.dircmp('src', 'des')
# dcmp.report_full_closure()