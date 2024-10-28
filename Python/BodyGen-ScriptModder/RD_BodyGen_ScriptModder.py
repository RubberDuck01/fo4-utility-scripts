import os
import shutil
import xml.etree.ElementTree as ET

def main_menu():
    print("X=======================================================X")
    print("|========= Rubber Duck's BodyGen Script Modder =========|")
    print("X=======================================================X")
    print("\nPlease select desired option: ")
    print("1) Find and copy XML files (presets)") #? Copies XML files from Mods and Overwrite directories to copied_presets_bodygen directory (where script is)
    print("2) Modify XML files (presets)") #? Reads templates.ini file and updates sliders based on default provided body preset XML
    print("3) Rename and fix XML files") #? Personal issue - a few XML files have '#_' prefix in their names, need to remove it (QoL)
    choice = input("\nSelect option (1, 2 or 3): ")
    return choice

def copy_files(src, dest):
    if not os.path.exists(dest):
        os.makedirs(dest)
    total_files = 0

    for root, dirs, files in os.walk(src):
        for file in files:
            if file.endswith('.xml') and not file.startswith('BT3'):
                src_file = os.path.join(root, file)
                dest_file = os.path.join(dest, file)
                
                #? Handle duplicates:
                base, ext = os.path.splitext(dest_file)
                counter = 1
                while os.path.exists(dest_file):
                    dest_file = f"{base}_{counter}{ext}"
                    counter += 1

                shutil.copy2(src_file, dest_file)
                total_files += 1
    return total_files

def parse_xml_preset(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    preset = root.find('Preset')
    preset_name = preset.get('name')
    preset_set = preset.get('set')

    sliders = {}
    for slider in preset.findall('SetSlider'):
        slider_name = slider.get('name')
        slider_value = float(slider.get('value'))
        sliders[slider_name] = slider_value
    
    return preset_name, preset_set, sliders

def parse_ini_file(ini_path):
    presets = {}
    with open(ini_path, 'r') as file:
        for line in file:
            if '=' in line:
                preset_name, sliders_str = line.strip().split('=', 1)
                sliders = {}
                for slider_str in sliders_str.split(','):
                    slider_name, slider_value = slider_str.split('@')
                    sliders[slider_name.strip()] = float(slider_value.strip())
                presets[preset_name.strip()] = sliders
    return presets

#? Update presets based on base body sliders:
def update_presets(presets, base_sliders):
    updated_presets = {}
    base_slider_names = set(base_sliders.keys())
    for preset_name, sliders in presets.items():
        updated_sliders = {}
        used_sliders = set()
        changes = []
        for slider_name, slider_value in sliders.items():
            base_value = base_sliders.get(slider_name, 0)
            if slider_value < 0:
                updated_value = slider_value + (abs(base_value) / 100)
            else:
                updated_value = slider_value - (base_value / 100)
            
            if updated_value != slider_value:
                updated_sliders[slider_name] = updated_value
                changes.append(f" --> {slider_name} was {slider_value}, now {updated_value:.2f}")
            else:
                updated_sliders[slider_name] = slider_value
                changes.append(f" --> {slider_name} values are the same")
            used_sliders.add(slider_name)

        #? Check for unused sliders:
        unused_sliders = base_slider_names - used_sliders
        if unused_sliders:
            changes.append(" ==> Unused sliders:")
            for unused_slider in unused_sliders:
                changes.append(f"     -> {unused_slider}")
            print("\n")
        
        if changes:
            print(f"Updated '{preset_name}':")
        for change in changes:
            print(change)
        
        updated_presets[preset_name] = updated_sliders
    return updated_presets

def write_ini_file(ini_path, presets):
    with open(ini_path, 'w') as file:
        for preset_name, sliders in presets.items():
            sliders_str = ', '.join(f"{name}@{value:.2f}" for name, value in sliders.items())
            file.write(f"{preset_name}={sliders_str}\n")

def rename_and_fix_xml(xmls_path):
    for root, dirs, files in os.walk(xmls_path):
        for file in files:
            if file.startswith('#_') and file.endswith('.xml'):
                old_file_path = os.path.join(root, file)
                new_file_name = file[2:]  # Remove '#_' prefix
                new_file_path = os.path.join(root, new_file_name)

                # Rename the file
                os.rename(old_file_path, new_file_path)
                print(f"Renamed: {old_file_path} to {new_file_path}")

                # Update the <Preset> name attribute inside the XML file
                tree = ET.parse(new_file_path)
                root_element = tree.getroot()
                preset = root_element.find('Preset')
                if preset is not None:
                    old_name = preset.get('name')
                    if old_name.startswith('#_'):
                        new_name = old_name[2:]  # Remove '#_' prefix
                        preset.set('name', new_name)
                        tree.write(new_file_path)
                        print(f" --> Updated name in {new_file_path}: {old_name} to {new_name}")

def main():
    choice = main_menu()

    if choice == '1':
        #? Copy XML files:
        mods_path = input("Enter the path to the Mods directory: ")
        overwrite_path = input("Enter the path to the Overwrite directory: ")

        print("\nCopying XML files, hang on...")

        script_dir = os.path.dirname(os.path.abspath(__file__))
        copied_presets_dir = os.path.join(script_dir, 'copied_presets_bodygen')

        #- Copy from overwrite:
        overwrite_src = os.path.join(overwrite_path, 'tools', 'bodyslide', 'SliderPresets')
        overwrite_dest = os.path.join(copied_presets_dir, 'overwrite', 'SliderPresets')
        total_files_overwrite = copy_files(overwrite_src, overwrite_dest)

        #- Copy from mods:
        total_files_mods = 0
        for mod_dir in os.listdir(mods_path):
            mod_path = os.path.join(mods_path, mod_dir)
            if os.path.isdir(mod_path):
                mod_src = os.path.join(mod_path, 'tools', 'bodyslide', 'SliderPresets')
                if os.path.exists(mod_src):
                    mod_dest = os.path.join(copied_presets_dir, 'mods', 'SliderPresets')
                    total_files_mods += copy_files(mod_src, mod_dest)
        
        print("Done!")
        print(f"Total files copied from overwrite: {total_files_overwrite}")
        print(f"Total files copied from mods: {total_files_mods}")
        print("Copy operation completed successfully!\nScript exiting...")
    
    elif choice == '2':
        #* Modify XML files:
        bodygen_files_path = input("Enter the path to the BodyGen INI files (morphs & templates): ")
        base_body_preset = input("Enter the path to the base body preset XML file: ")
        print("Reading base body preset XML file...")

        preset_name, preset_set, base_sliders = parse_xml_preset(base_body_preset)
        print(f"Ok! Selected base body preset '{preset_name}' (set: '{preset_set}')\n")
        # print(f"Body preset '{preset_name}' (set: '{preset_set}')")
        # print("Sliders:")
        # for slider in sliders:
        #     print(f"  - Name: {slider['name']}, Size: {slider['size']}, Value: {slider['value']}")
        
        print("Reading templates.ini file...")
        templates_ini_path = os.path.join(bodygen_files_path, 'templates.ini')
        presets = parse_ini_file(templates_ini_path)

        print(f"Updating BodyGen presets based on base body ({preset_name})...")
        updated_presets = update_presets(presets, base_sliders)

        print("\nWriting updated presets back to templates.ini file...")
        write_ini_file(templates_ini_path, updated_presets)

        print("Done! Presets have been adjusted and saved.\nScript exiting...")

    elif choice == '3':
        xmls_path = input("Enter the path to the XML files: ")
        rename_and_fix_xml(xmls_path)
        print("Done! XML files have been renamed and fixed.\nScript exiting...")

    else:
        print("Invalid choice. Please try again with a valid option.\nExiting...")

if __name__ == "__main__":
    main()