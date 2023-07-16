# fo4-utility-scripts
These are the scripts I use on a day-to-day basis.

## Python stuff
These scripts are primarily used to automate certain processes on a day-to-day basis. I use them whenever the need arises.

### Contents:
#### RobCo_SwitchBipedSlots
This script will switch ARMO biped slots.
Before running it, you need to export the ARMO items from xEdit to CSV (you can use my SAKR Pascal script for this). Then, run the script and load the newly exported CSV. The script will <i>extract</i> all the data required and you will need to tell the script which item(s) should have which biped slot(s).

#### rd_sakr_simplify
Script used to read data from one CSV and export it to the other with some differences. It was heavily used in early stages of my SAKR/RCPGen tool development, but is proven useful for manipulating other CSVs as well.

#### RenameBrackets
Small and simple script used to rename files. I used this script to rename a bunch of LM JSONs by adding '(RD)' in front of the names. <i> For better sorting, obviously. </i>

### Requirements
To run these, you (obviously) need Python 3.  
I'm personally running Python v3.10, but any v3 should suffice.

#### This README file is being continously updated as I add more stuff.

