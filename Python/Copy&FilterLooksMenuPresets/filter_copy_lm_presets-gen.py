#? This script filters and copies LooksMenu presets (json) by gender.
#? 0 for M, 1 for F

import os
import sys
import json
import shutil

print("=== LM Presets Filter-Copier ===")
print("       v1.0 (23/04/2024)")

mods_path = input("Enter path to your mods/overwrite directory: ")

if not os.path.isdir(mods_path):
    print("Invalid path! Provided path is not a directory. Exiting...")
    sys.exit(2)
else:
    gender_select = input("Filter and copy all Female (1) or Male (0) presets? [M/F] ").lower()
    if gender_select == 'm':
        gender_code = 0
    elif gender_select == 'f':
        gender_code = 1
    else:
        print(f"'{gender_select}' is not a valid option.")
        sys.exit(21)
    
    
    dir_count = sum(1 for _ in os.listdir(mods_path))
    print(f"Scanning... Total directories to process: {dir_count}")
    try:
        copied_count = 0
        for root, dirs, files in os.walk(mods_path):
            if root.endswith('F4SE\\Plugins\\F4EE\\Presets'):
                print(f" -> Found LooksMenu presets directory: {root}")
                for file in os.listdir(root):
                    if file.endswith('.json'):
                        with open(os.path.join(root, file), 'r') as json_file:
                            data = json.load(json_file)
                            if data.get('Gender') == gender_code:
                                print(f"    -> Found desired preset file: {file}")
                                destination = os.path.join('C:\\Users\\Rubber Duck\\Desktop\\filtered_presets', file)
                                shutil.copy(os.path.join(root, file), destination)
                                copied_count += 1
        
        print(f"Done! {copied_count} presets copied.")
    except Exception as e:
        print(f"Something went wrong: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("Killed by user. Forcefully stopping...")
        sys.exit(3)