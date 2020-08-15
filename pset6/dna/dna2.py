import csv
from sys import argv, exit

# Check usage is correct
if len(argv) != 3:
    print("Usage: dna.py data.csv sequence.txt")
    exit(1)

# Open the CSV file and read
csvfile = open(argv[1], "r")
reader = csv.DictReader(csvfile)
str_NAMES = reader.fieldnames[1:]

# Open text file and read
with open(argv[2], "r") as txtfile:
    dna = txtfile.read()

# Initialize empty dict
mapping = {}

# Map STR sequence onto indices
# and replace all occurences of such STR
# with mapped index
for i, name in enumerate(str_NAMES):
    mapping[name] = str(i)
    dna = dna.replace(name, str(i))

# Initiliaze count dict which will
# contain longest run of a sequence
dna_max_run = {}

# Computing STR counts
for seq in str_NAMES:
    seq_idx = mapping[seq]
    # Max consecutive count of seq
    max_str_COUNT = 0
    for i, c in enumerate(dna):
        # Current consecutive count of seq
        current_count = 0
        # Checks if char matches seq_idx
        if c == seq_idx:
            current_count += 1
            # Iff first_time traversing
            if current_count == 1:
                j = i
                # Loop through each char after original tracked char
                while j < (len(dna) - 1):
                    # Add to current consective count if match
                    if dna[j + 1] == seq_idx:
                        current_count += 1
                        j += 1
                    else:
                        # Break at the first instance the next char
                        # is not of same char as original
                        break
            # Update maximum consecutive count if necessary
            if current_count > max_str_COUNT:
                max_str_COUNT = current_count

    # Add max count to resp. seq
    dna_max_run[seq] = max_str_COUNT

# Initialize match count
match_count = 0

# Loop through each candidate in database (csv)
for odict in reader:
    items = list(odict.items())
    name = items[0][1]
    for i, item in enumerate(items[1:]):
        str_name = item[0]
        if dna_max_run[str_name] == int(item[1]):
            match_count += 1
    # Since we can assume uniqueness of DNA sequence,
    # we can immediate print once we have an exact match
    if match_count == len(str_NAMES):
        print(name)
        # Close CSV file!
        csvfile.close()
        # Exit with success
        exit(0)
    else:
        # Reset match counter
        match_count = 0

# Iff after looping, we don't have any single match
print("No match")
exit(1)
