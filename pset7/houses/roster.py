from sys import argv, exit
from cs50 import SQL

# Check len of CLI
if len(argv) != 2:
    print("Usage: roster.py house_name")
    exit(1)

# Get house name
house = argv[1]

# Get access to sqlite database students.db
db = SQL("sqlite:///students.db")

# Query for student roster
roster = db.execute("SELECT * FROM students WHERE house = ? ORDER BY last, first", house)

# Iterate over each student (is dictionary)
for student in roster:
    if student['middle'] is None:
        names = [student['first'], student['last']]
    else:
        names = [student['first'], student['middle'], student['last']]

    # Get full name
    full_name = " ".join(names)
    # Get birth date
    birth = student['birth']
    # Print the name and birth date
    print(f"{full_name}, born {birth}")

