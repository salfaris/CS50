// includes
#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

// funcs declaration
char letter_shifting(int key, char c, bool uppercase);

// main func
int main(int argc, string argv[])
{
    // Checks if there are only two inputs (including filename)
    if (argc != 2)
    {
        // Prints error message if argc is not 2
        printf("Usage: %s key\n", argv[0]);
        return 1;
    }

    // Checks if argument is purely digits
    int checker = 0;

    for (int i = 0, arg_len = strlen(argv[1]); i < arg_len; i++)
    {
        // isdigit returns integers > 0 for digits
        if (isdigit(argv[1][i]) == 0)
        {
            checker++;
            break;
        }
    }

    if (checker != 0)
    {
        printf("Usage: %s key\n", argv[0]);
        return 1;
    }
    else
    {
        // Converts string to int
        int key = atoi(argv[1]);

        // Prompts user for plaintext
        string plaintext = get_string("plaintext: ");

        // Prints ciphertext
        printf("ciphertext: ");
        for (int i = 0, text_len = strlen(plaintext); i < text_len; i++)
        {
            // Checks if char is lowercase
            if (islower(plaintext[i]) != 0)
            {
                printf("%c", letter_shifting(key, plaintext[i], 0));
            }
            // Checks if char is uppercase
            else if (isupper(plaintext[i]) != 0)
            {
                printf("%c", letter_shifting(key, plaintext[i], 1));
            }
            // Else prints the char itself
            else
            {
                printf("%c", plaintext[i]);
            }
        }
        printf("\n");
    }
}

char letter_shifting(int key, char c, bool uppercase)
{
    // Initiate int variables
    int shifted, uppernum = 65, lowernum = 97;
    if (uppercase == 1)
    {
        // Shifts uppercase char to 0
        shifted = c - uppernum;
        // Add key and reduce mod 26
        shifted = (shifted + key) % 26;
        // Shifts char back to 65
        shifted += uppernum;
        return shifted;
    }
    else if (uppercase == 0)
    {
        // Shifts lowercase char to 0
        shifted = c - lowernum;
        // Add key and reduce mod 26
        shifted = (shifted + key) % 26;
        // Shifts char back to 97
        shifted += lowernum;
        return shifted;
    }
    else
    {
        // Throw an error and exits program
        printf("Error!");
        return 1;
    }
}