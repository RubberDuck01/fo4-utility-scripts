import os
import shutil
import sys
import xml.etree.ElementTree as ET

def calculate_insane_value(nude_diff, outfit_diff):
    if nude_diff < 0 or outfit_diff < 0:
        sign = -1
    else:
        sign = 1
    insane_value = sign * (abs(nude_diff) + abs(outfit_diff))
    return insane_value

def determine_final_value(nude_diff, outfit_diff, insane_value):
    # Both negative
    if nude_diff < 0 and outfit_diff < 0:
        return min(nude_diff, outfit_diff)
    # Both positive
    elif nude_diff > 0 and outfit_diff > 0:
        return min(nude_diff, outfit_diff)
    # Mixed signs (one positive, one negative)
    else:
        return insane_value

def modify_templates_ini(ini_path, calculated_presets, target_slider):
    backup_path = ini_path.replace(".ini", "_backup.ini")
    shutil.copy2(ini_path, backup_path)
    print(f"Backup created: {backup_path}")

    modified_lines = []
    with open(ini_path, "r") as ini_file:
        for line in ini_file:
            if '=' in line:
                preset, slider = line.split('=', 1)
                preset = preset.strip()

                if preset in calculated_presets:
                    new_value = calculated_presets[preset]
                    slider_parts = slider.split(', ')

                    for i, part in enumerate(slider_parts):
                        if f"{target_slider}@" in part:
                            name, _ = part.strip().split('@')
                            slider_parts[i] = f"{name}@{new_value / 100:.2f}"
                    
                    new_line = f"{preset} = {', '.join(slider_parts)}"
                    modified_lines.append(new_line)
                else:
                    modified_lines.append(line)
            else:
                modified_lines.append(line)
    
    with open(ini_path, "w") as ini_file:
        ini_file.writelines(modified_lines)

    print("Changes applied successfully!")

def main():
    ini_path = input("Enter path to templates.ini: ").strip()
    if not os.path.isfile(ini_path):
        print("Error: Not a valid file path.")
        sys.exit(1)
    
    xmls_path = input("Enter path to your XML presets directory: ").strip()
    if not os.path.isdir(xmls_path):
        print("Error: Not a valid directory path.")
        sys.exit(1)
    
    target_slider = input("Enter the target slider name: ").strip()
    
    try:
        nude_value = int(input("Enter the nude value: ").strip())
        outfit_value = int(input("Enter the outfit value: ").strip())
    except ValueError:
        print("Error: Please enter a valid numeric value.")
        sys.exit(2)

    calculated_presets = {}
    
    for root, dirs, files in os.walk(xmls_path):
        for file in files:
            if file.lower().endswith('.xml'):
                file_path = os.path.join(root, file)
                try:
                    tree = ET.parse(file_path)
                    root_el = tree.getroot()
                except ET.ParseError:
                    print(f"Error: Invalid XML: '{file_path}', skipping...")
                    continue

                preset_el = root_el.find('Preset')
                if preset_el is None:
                    continue

                preset_name = preset_el.get('name', 'Unknown')

                for slider_el in preset_el.findall('SetSlider'):
                    if slider_el.get('name', '').lower() == target_slider.lower():
                        try:
                            preset_value = int(slider_el.get('value', '0'))
                        except ValueError:
                            preset_value = 0
                        
                        nude_calc = preset_value - nude_value
                        outfit_calc = preset_value - outfit_value
                        avg_diff = round((nude_calc + outfit_calc) / 2.0)  # Rounded to nearest integer
                        insane_value = calculate_insane_value(nude_calc, outfit_calc)
                        final_value = determine_final_value(nude_calc, outfit_calc, insane_value)
                        
                        calculated_presets[preset_name] = final_value
                        
                        print(f"\n{preset_name}")
                        print(f"  {target_slider}: {preset_value}")
                        print(f"    Nude Diff:   {nude_calc}")
                        print(f"    Outfit Diff: {outfit_calc}")
                        print(f"    Average Diff: {avg_diff}")
                        print(f"    Insane Diff: {insane_value}")
                        print(f"    F I N A L: {final_value}")

    apply_changes = input("\nDo you want to apply these changes to templates.ini? (Y/n): ").strip().lower()
    if apply_changes in ('y', 'yes', ''):
        modify_templates_ini(ini_path, calculated_presets, target_slider)
    else:
        print("No changes applied.")

if __name__ == "__main__":
    main()