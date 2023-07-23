import csv

# class:
class Row:
    def __init__(self, plugin, formid, name):
        self.plugin = plugin
        self.formid = formid
        self.name = name

# parse function:
def parse_csv(filePath):
    objects = []

    try:
        with open(filePath, 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter = ';')
            for row in csv_reader:
                if len(row) == 3:
                    plugin, formid, name = row
                    object = Row(plugin, formid, name)
                    objects.append(object)
                else:
                    print(f"-> Invalid row: {row}")

    except FileNotFoundError:
        print(f"[Error] File '{csv}' not found!")
    except Exception as e:
        print(f"[Fail] Something went wrong: {str(e)}")

    return objects

# function to add biped slots to items from csv (user input):
def add_biped_slots(objects):
    print("[RD_Script] Enter desired biped slot INDEX for each item. INDEX values are >= 0 and <= 43.\nIf in doubt, check CK documentation here: https://www.creationkit.com/fallout4/index.php?title=Biped_Slots")
    

print("X=====================================================X")
print("| Python - Switch Body Biped Slots with RobCo Patcher |")
print("|                   By: Rubber Duck                   |")
print("|                  v1.1 - 02/04/2023                  |")
print("X=====================================================X")
print("[RD_Script] Started!")

# ask for CSV:
csv_in = input("[RD_Script] Enter full path to CSV file:\n> ")

# use:
parsed_csv = parse_csv(csv_in)
add_biped_slots(parsed_csv)
# show:
# print("Plugin       FormID      NAME")
# for obj in parsed_csv:
#    print(f"{obj.plugin}:{obj.formid} -> '{obj.name}'")