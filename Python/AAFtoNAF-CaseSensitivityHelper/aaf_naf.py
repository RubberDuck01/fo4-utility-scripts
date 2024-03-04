import os
import re

# D:\Games\MO2\Games\Fallout 4\mods\Naf XMLs - Case Sensitive\NAF

print("RD's AAF to NAF XML Helper")
print(" -> This script fixes Race IDs from AAF XMLs for NAF.\n> Why?\n -> NAF's XML handler is case sensitive and that can cause problems when playing animations.")
print("Ver 1.0 // By: Rubber Duck")

try:
    found_cntr = 0
    fix_cntr = 0
    source_path = input("Enter the path to your NAF dir:\n> ")
    input_str = input("What are we searching for (lowercase)?\n> ")
    input_correct = input("What's the correct input (case-sensitive)?\n> ")
    
    for file in os.listdir(source_path):
        try:
            if file.endswith('.xml'):
                with open(os.path.join(source_path, file), 'r', encoding='utf-8') as f:
                    for line_no, line in enumerate(f, start=1):
                        matches = re.findall(fr'\b{input_str}\b', line, re.IGNORECASE)
                        for match in matches:
                            print(f" -> Found {match} in {file} at line {line_no}")
            
        except Exception as e:
            print(f"Error while reading file {file}: {e}")
    
    fix_input = input(f"\nFix potential problems for '{input_str}'? (y/N) ")
    if fix_input.lower() == 'n' or fix_input == '':
        print("Roger that, not fixing any problems...")
        exit()
    else:
        print("Fixing potential issues...")
        for file in os.listdir(source_path):
            try:
                if file.endswith('.xml'):
                    with open(os.path.join(source_path, file), 'r+', encoding='utf-8') as f:
                        content = f.read()
                        new_content = re.sub(fr'\b{input_str}\b', f'{input_correct}', content, flags=re.IGNORECASE)
                        
                        if new_content != content:
                            fix_cntr += 1
                            print(f" -> Found and fixed potential problem in: {file}")
                            f.seek(0)
                            f.write(new_content)
                            f.truncate()
                
                print(f"Total files fixed: {fix_cntr}")
            except Exception as e:
                print(f"Error while processing file {file}: {e}")    
    
except Exception as e:
    print(f"\nError: {e}")
    input("\nPress any key to exit...") 
    exit()
    
except KeyboardInterrupt:
    print("\nC-c detected, exiting...")
    exit()
