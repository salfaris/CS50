#include <stdio.h>
#include <cs50.h>

int main(void)
{
    int height;
    do
    {
        height = get_int("Height: ");
    }
    while (height < 1 || height > 8);

    for (int i = 0; i < height; i++)
    {
        // Create spaces to push the hashes
        for (int k = 0; k < height - i - 1; k++)
        {
            printf(" ");
        }
        // Create the hashes
        for (int j = 0; j < i + 1; j++)
        {
            printf("#");
        }
        // Print a newline
        printf("\n");
    }
}