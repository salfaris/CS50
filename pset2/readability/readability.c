// includes
#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <string.h>
#include <math.h>

// func declarations
int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

// main func
int main(void)
{
    // Prompt users for text
    string text = get_string("Text: ");

    // Compute # of letters, words and sentences
    int letters = count_letters(text);
    int words = count_words(text);
    int sentences = count_sentences(text);

    // Avg # of letters per 100 words rounded two 2 decimal places
    float letter_avg = round((float) letters / words * 10000) / 100;

    // Avg # of sentences per 100 words rounded two 2 decimal places
    float sentence_avg = round((float) sentences / words * 10000) / 100;

    // Compute the Coleman-Liau index
    int index = round(0.0588 * letter_avg - 0.296 * sentence_avg - 15.8);

    // Checks Before Grade 1 condition
    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    // Checks Grade 16+ condition
    else if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    // If all special cond. fails, print Grade X
    else
    {
        printf("Grade %i\n", index);
    }
}

int count_letters(string text)
{
    // Initialize # of letters
    int letters = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        // Check if char is alphabetical
        if (isalpha(text[i]) != 0)
        {
            letters++;
        }
    }
    return letters;
}

int count_words(string text)
{
    // Initialize # of words to 1 (we'll count spaces)
    int words = 1;
    for (int i = 0; i < strlen(text); i++)
    {
        // Count spaces
        if ((text[i] == ' ') && (text[i + 1] != ' '))
        {
            words++;
        }
    }
    return words;
}

int count_sentences(string text)
{
    // Initialize # of sentences
    int sentences = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        // Scans for sentence boundary
        if ((text[i] == '.') || (text[i] == '!') || (text[i] == '?'))
        {
            sentences++;
        }
    }
    return sentences;
}