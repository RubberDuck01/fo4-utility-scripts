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
                    print(f'-> Invalid row: {row}')

    except FileNotFoundError:
        print(f'[Error] File \'{csv}\' not found!')
    except Exception as e:
        print(f'[Fail] Something went wrong: {str(e)}')

    return objects

# function to add biped slots to items from csv (user input):
def add_biped_slots(objects):
    print('\n[RD_Script] Enter desired biped slot INDEX for each item, and use \'q\' to quit.\n[Tip] INDEX values are >= 0 and <= 43.\n[Tip] Index \'11\' is TORSO ARMOR, index \'6\' is TORSO UNDERARMOR\n-> If in doubt, check CK documentation here: https://www.creationkit.com/fallout4/index.php?title=Biped_Slots\n')
    for obj in objects:
        while True:
            slot_input = input(f'> Enter desired index for "{obj.name}": ')
            if slot_input == 'q':
                return # exit
            elif slot_input == 's':
                break # skip the current object                
            else:
                try:
                    newBipedSlot = int(slot_input)
                    if 0 <= newBipedSlot <= 43:
                        obj.indexNew = newBipedSlot
                        
                        # determine which slots to remove depending on the new value:
                        if newBipedSlot == 6:
                            obj.indexOld = 11
                            obj.oldIndexStr = '[41] Armor Torso'
                            obj.newIndexStr = '[36] Underarmor'
                        elif newBipedSlot == 11:
                            obj.indexOld = 6
                            obj.oldIndexStr = '[36] Underarmor'
                            obj.newIndexStr = '[41] Armor Torso'
                        # continue the logic if needed, but this is it for my needs :P

                        print(f'---> Added index \'{obj.indexNew}\' (was \'{obj.indexOld}\') to "{obj.name}".')
                        break
                    else:
                        print('[Error] Index out of range: Index has to be a number between 0 and 43.')
                except ValueError:
                    print('[Fail] Invalid input! Enter a number between 0 and 43, or enter \'r\' to retry or \'q\' to quit.')
    
# function to create ini file:
def create_ini(objects, path):
    with open(path.strip(), 'w') as ini_file:
        ini_file.write('// INI automatically generated by Rubber Duck\'s script\n')
        ini_file.write('// Check the repo for more info: https://github.com/RubberDuck01/fo4-utility-scripts\n')
        for obj in objects:
            if obj.indexNew is not None:
                ini_file.write(f'\n// "{obj.name}" -> was \'{obj.indexOld}\' (\'{obj.oldIndexStr}\'), now it\'s \'{obj.indexNew}\' (\'{obj.newIndexStr}\')\n')
                ini_file.write(f'filterByArmors={obj.plugin}|{obj.formid}:bipedSlotsToRemove={obj.indexOld}:bipedSlotsToAdd={obj.indexNew}\n')
            else:
                print('\n[Fatal] The snake couldn\'t generate INI!')

print('X=====================================================X')
print('| Python - Switch Body Biped Slots with RobCo Patcher |')
print('|                   By: Rubber Duck                   |')
print('|                  v1.1 - 02/04/2023                  |')
print('X=====================================================X')
print('[RD_Script] Started!')

# ask for CSV:
csv_in = input('[RD_Script] Enter full path to CSV file:\n> ')

# parse that csv:
parsed_csv = parse_csv(csv_in)
add_biped_slots(parsed_csv)

# ask for ini path and create it:
ini_path = input('\n[RD_Script] Enter new INI path (ex: \'Path\'To\'file.ini\'):\n> ')
create_ini(parsed_csv, ini_path)
print(f'\n[Success] INI \'{ini_path}\' created successfully! Script exiting.\n')