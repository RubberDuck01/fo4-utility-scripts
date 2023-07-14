print("=====================================")
print("Python script - CSV for SAKR patching")
print("           By: Rubber Duck           ")
print("          v1.1 - 02/04/2023          ")
print("=====================================")
print("RD_Script: Started")

# Ask for csv file:
print("RD_Script: Enter CSV file:")
csv_in = input("> ")
#csv_in = "list.csv"

# Create copy of csv file with rdmod_ prefix for name
csv_out = f"rdmod_{csv_in}"

with open(csv_in, 'r') as f_in, open(csv_out, 'w') as f_out:
    print(f"RD_Script: Processing {csv_in} ...")

    for row in f_in:
        # print("DEBUG: ", row[0])
        
        # Split the line into two using ';' as delimiter
        new_row = row.replace(';', '\n')

        # Add '//' at the beginning row:
        if row.startswith('"'): row = ''.join(['// ', row])
        new_row = ''.join(['// ', new_row])

        # print('DEBUG: ', new_row)
        
        # Write the two new rows to the output csv file        
        f_out.writelines(new_row)

    print(f"RD_Script: Finished! New file is '{csv_out}'")

# Another file:
while True:
    print("RD_Script: Another one? (y/n)")
    another = input("> ").lower()
    # if y, ask for csv again
    if another == 'y':
        print("RD_Script: Enter CSV file:")
        csv_in = input("> ")
        csv_out = f"rdmod_{csv_in}"

        with open(csv_in, 'r') as f_in, open(csv_out, 'w') as f_out:
            print(f"RD_Script: Processing {csv_in} ...")

            for row in f_in:
                # print("DEBUG: ", row[0])
        
                # Split the line into two using ';' as delimiter
                new_row = row.replace(';', '\n')

                # Add '//' at the beginning row:
                if row.startswith('"'): row = ''.join(['// ', row])
                new_row = ''.join(['// ', new_row])

                # print('DEBUG: ', new_row)
        
                # Write the two new rows to the output csv file        
                f_out.writelines(new_row)

            print(f"RD_Script: Finished! New file is '{csv_out}'")
    # if n, break
    elif another == 'n':
        print("RD_Script: Bye!")
        break;
    else:
        print("RD_Script: Invalid input! Enter 'y' or 'n'.")