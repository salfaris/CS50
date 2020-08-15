from cs50 import get_float

while True:
    dollars = get_float("Change owed: ")
    if dollars >= 0:
        break

# Converts dollars to cent and round
cents = round(dollars * 100, 2)

# Counter to count coins used
coins = 0

# Starts counting num of coins using greedy algorithm
while cents != 0:
    if cents >= 25:
        cents += -25
        coins += 1

    elif cents >= 10:
        cents += -10
        coins += 1

    elif cents >= 5:
        cents += -5
        coins += 1

    elif cents >= 1:
        cents += -1
        coins += 1

print(coins)