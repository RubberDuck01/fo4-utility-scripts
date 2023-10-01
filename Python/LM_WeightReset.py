import os
import json

#* Info:
#* Script will modify the JSONs in current directory (where this script is)
#* and attempt to set the "Weight" to certain value.

#? Note:
#? The new value is clostest to dead-center of the weight triangle
#? which is recommended for use with CBBE/TWB bodies with 3BBB physics.

try:
    #? closest values to dead-center of the weight triangle:
    new_weight = [ 0.333299994468689, 0.333299994468689, 0.333299994468689 ]
    json_files = [file for file in os.listdir() if file.endswith(".json")]

    for json_file in json_files:
        with open(json_file, "r") as file:
            data = json.load(file)

        if "Weight" in data:
            data["Weight"] = new_weight
        else:
            print(f"The file '{json_file.title}' doesn't contain 'Weight' field! Skipping it...")

        #* write new json:
        with open(json_file, "w") as file:
            json.dump(data, file, indent = 4)

    print("JSONs successfully modified!")

except Exception as e:
    print(f"Something went wrong.\nStack:\n{e}")