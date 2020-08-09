#include <stdio.h>
#include <math.h>
#include <cs50.h>

int main(void)
{
    float dollars;
    // Prompts user for input in dollars
    do
    {
        dollars = get_float("Change owed: ");
    }
    while (dollars < 0);

    // Converts dollars to cent and round
    int cents = round(dollars * 100);

    // Counter to count coins used
    int coins = 0;

    // Starts counting num of coins using greedy algorithm
    while (cents != 0)
    {
        if (cents >= 25)
        {
            cents += - 25;
            coins++;
        }
        else if (cents >= 10)
        {
            cents += - 10;
            coins++;
        }
        else if (cents >= 5)
        {
            cents += -5;
            coins++;
        }
        else if (cents >= 1)
        {
            cents += -1;
            coins++;
        }
    }
    printf("%i\n", coins);
}


