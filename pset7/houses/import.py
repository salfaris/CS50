from sys import argv, exit
from cs50 import SQL
import csv

# Check len of CLI
if len(argv) != 2:
    print("Usage: import.py [file.csv]")
    exit(1)

# Get access to sqlite database students.db
db = SQL("sqlite:///students.db")

# Open the CSV file
with open(argv[1], "r") as file:
    # Create DictReader object
    reader = csv.DictReader(file)

    # Iterate over CSV file
    for row in reader:
        # Parse name into list
        full_name = row["name"].split()

        # Get first name
        first_name = full_name[0]

        # Check length of name and assign middle, last
        if len(full_name) == 2:
            middle_name = None
            last_name = full_name[1]
        else:
            middle_name = full_name[1]
            last_name = full_name[2]

        # Insert the row into table
        db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES(?, ?, ?, ?, ?)",
                   first_name, middle_name, last_name, row["house"], row["birth"])