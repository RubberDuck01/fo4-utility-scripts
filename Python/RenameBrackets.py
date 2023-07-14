import os

# set the directory path
dir_path = 'C:/Users/Rubber Duck/Desktop/looksmenu'

# get all files in the directory
files = os.listdir(dir_path)

# loop through each file in the directory
for filename in files:
    if filename.endswith('.json') and filename.startswith('RD'):
        new_filename = f"({filename[:2]}){filename[2:]}"
        os.rename(os.path.join(dir_path, filename), os.path.join(dir_path, new_filename))
        print(f"File {filename} renamed to {new_filename}")
