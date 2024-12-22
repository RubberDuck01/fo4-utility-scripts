import os
import sys

def main():
    # 1) Ask for path to templates.ini
    ini_path = input("Enter path to templates.ini: ").strip()
    if not os.path.isfile(ini_path):
        print("Error: Not a valid file path.")
        sys.exit(1)
    
    # 2) Ask for target slider name
    target_slider = input("Enter the target slider name: ").strip()
    
    # 3) Ask for search value (the number to compare against)
    #    e.g., if user types "74", we compare slider_value * 100 to 74
    try:
        search_value = float(input("Enter the search value (e.g. 74 for 0.74): "))
    except ValueError:
        print("Error: Please enter a valid numeric value.")
        sys.exit(2)
    
    # 4) Read the templates.ini file
    with open(ini_path, 'r') as file:
        for line in file:
            line = line.strip()
            if '=' in line:
                preset_name, sliders_str = line.split('=', 1)
                # Split individual sliders by comma
                sliders = sliders_str.split(',')
                for slider_entry in sliders:
                    slider_entry = slider_entry.strip()
                    if '@' in slider_entry:
                        s_name, s_value_str = slider_entry.split('@', 1)
                        s_name = s_name.strip()
                        try:
                            s_value = float(s_value_str.strip())
                        except ValueError:
                            continue
                        
                        # Check if this slider matches the user’s target slider
                        if s_name.lower() == target_slider.lower():
                            # Multiply by 100 so 0.74 becomes 74.0
                            display_value = s_value * 100
                            
                            # Compare with the user-provided search_value
                            if abs(display_value - search_value) < 1e-9:
                                comparison = "="
                            elif display_value > search_value:
                                comparison = ">"
                            else:
                                comparison = "<"
                            
                            print(f"-> {s_name}: {display_value:.2f} {comparison} {search_value:.2f} (Preset: {preset_name.strip()})")

if __name__ == "__main__":
    main()