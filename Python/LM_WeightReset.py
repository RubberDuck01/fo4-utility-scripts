import os
import json

#* Info:
#* Script will modify the JSONs in current directory (where this script is)
#* and attempt to set the "Weight" to certain value.

#? Note:
#? The new value is clostest to dead-center of the weight triangle
#? which is recommended for use with CBBE/TWB bodies with 3BBB physics.

try:
    print("Initializing...")
    #? closest values to dead-center of the weight triangle:
    new_weight = [ 0.333299994468689, 0.333299994468689, 0.333299994468689 ]
    json_files = [file for file in os.listdir() if file.endswith(".json")]
    json_cntr = 0

    for json_file in json_files:
        with open(json_file, "r") as file:
            data = json.load(file)

        if "Weight" in data:
            data["Weight"] = new_weight
            print(f"Modified weight for '{json_file}'")
            json_cntr += 1
        else:
            print(f"Couldn't modify '{json_file}' as it doesn't contain 'Weight' field. Skipping it...")

        #* write new json:
        with open(json_file, "w") as file:
            json.dump(data, file, indent = 4)

    print(f"\nFinished!\nSuccessfully modified {json_cntr} of {len(json_files)} files.")
    input("Press any key to continue...")

except Exception as e:
    print(f"Something went wrong.\nStack:\n{e}")
    input("Press any key to exit...")